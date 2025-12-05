# Core libraries
import os
import json
from io import BytesIO
from datetime import datetime

# AWS SDK
import boto3
from botocore.exceptions import ClientError

# PDF handling
from pypdf import PdfReader

# Markdown to PDF conversion
import markdown2
from weasyprint import HTML, CSS

# AWS Configuration
# Required secrets (set in your environment or secrets console):
# - AWS_ACCESS_KEY_ID
# - AWS_SECRET_ACCESS_KEY
# - AWS_BEARER_TOKEN_BEDROCK (for Bedrock API)

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

# Initialize clients
s3_client = boto3.client('s3')
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Bucket configuration
REFERENCE_BUCKET = 'your-reference-bucket-name'  # stores master resume, context, job reqs
OUTPUT_BUCKET = 'your-output-bucket-name'        # stores generated PDFs

# Personal configuration
USER_INITIALS = 'VECP'  # Change this to your own initials (e.g., 'JD' for John Doe)

# ============================================================================
# S3 FILE READING FUNCTIONS
# ============================================================================
# Context: We need to read three types of files from S3:
# 1. Master resume (markdown) - your baseline resume
# 2. Career context (markdown) - philosophy, stories, and instructions
# 3. Job requirements (PDF) - the job posting you're applying to

def read_from_s3(bucket_name, file_key):
    """
    Read a text/markdown file from S3.

    Args:
        bucket_name: S3 bucket name
        file_key: File path/key in the bucket

    Returns:
        String content of the file
    """
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    content = response['Body'].read().decode('utf-8')
    return content


def s3_extract_pdf(bucket_name, file_key):
    """
    Extract text content from a PDF stored in S3.

    Context: Job requirements come as PDFs. We need to extract the text
    to send to Claude for processing.

    Args:
        bucket_name: S3 bucket name
        file_key: PDF file path/key in the bucket

    Returns:
        Extracted text from all pages of the PDF
    """
    pdf_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    body = pdf_response['Body'].read()
    content = BytesIO(body)
    reader = PdfReader(content)

    # Extract text from all pages
    text = []
    for page in reader.pages:
        text.append(page.extract_text())

    return '\n'.join(text)


# ============================================================================
# CLAUDE AI GENERATION FUNCTION
# ============================================================================
# Context: This is the core function that reads your master resume, career
# context, and job req, then uses Claude to generate tailored materials.
# The prompt structure is: context + master resume + job requirements.
# Claude outputs both a tailored resume and cover letter in one response.

def generate_application_materials(job_req_filename):
    """
    Generate tailored resume and cover letter using Claude AI.

    Context: This function orchestrates the entire AI generation process.
    It reads three files from S3:
    - Master resume (your baseline)
    - Career context (philosophy, stories, instructions)
    - Job requirements (the specific job posting)

    Then sends them to Claude via AWS Bedrock to generate customized materials.

    Args:
        job_req_filename: Filename of the job req PDF in the reference bucket

    Returns:
        Claude's response containing both tailored resume and cover letter
    """
    # Read all required files
    master_resume = read_from_s3(REFERENCE_BUCKET, '${USER_INITIALS}_112025_Master.md')
    career_context = read_from_s3(REFERENCE_BUCKET, '${USER_INITIALS}_career_context.md')
    variable_req = s3_extract_pdf(REFERENCE_BUCKET, job_req_filename)

    # Build the prompt
    prompt_string = f"""{career_context}

    MASTER RESUME:
    {master_resume}

    JOB REQUIREMENTS:
    {variable_req}
    """

    # Call Claude via Bedrock
    try:
        response = bedrock_client.converse(
            modelId='us.anthropic.claude-3-5-sonnet-20241022-v2:0',
            system=[{"text": "You are a professional resume writer. Output only the final documents with no explanation or preamble."}],
            messages=[{"role": "user", "content": [{"text": prompt_string}]}]
        )
        return response['output']['message']['content'][0]['text']
    except ClientError as e:
        print(f"Claude API Error: {e}")
        return None


# ============================================================================
# PDF CONVERSION AND S3 UPLOAD
# ============================================================================
# Context: We convert markdown to PDF in-memory and upload directly to S3.
# This avoids cluttering your local directory with files.

def upload_md_as_pdf_to_s3(markdown_text, bucket, key):
    """
    Convert markdown to PDF and upload directly to S3.

    Context: Instead of saving PDFs locally, we convert markdown to PDF
    in memory using WeasyPrint, then upload directly to S3. This keeps
    your workspace clean and automates the entire pipeline.

    Args:
        markdown_text: The markdown content to convert
        bucket: Destination S3 bucket
        key: Destination file path/key in S3
    """
    html = markdown2.markdown(markdown_text)
    pdf_buffer = BytesIO()
    HTML(string=html).write_pdf(pdf_buffer, stylesheets=[CSS('resume_style.css')])

    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=pdf_buffer.getvalue()
    )


def push_output_to_s3(job_req):
    """
    Main workflow function: Generate materials and upload to S3.

    Context: This is your main entry point. It:
    1. Calls Claude to generate tailored materials
    2. Parses the response to separate resume and cover letter
    3. Extracts company name from the job req filename
    4. Uploads both PDFs to S3 with proper naming

    File naming convention: [INITIALS]_[CompanyName]_R.pdf and [INITIALS]_[CompanyName]_CL.pdf

    Args:
        job_req: Filename of the job req PDF (e.g., 'VECP_JobReq_NBCU.pdf')

    Returns:
        Tuple of (resume_result, cover_letter_result)
    """
    # Generate materials with Claude
    ai_output = generate_application_materials(job_req)

    if ai_output is None:
        print(f"Failed to generate materials for {job_req}")
        return None, None

    # Parse the response
    parts = ai_output.split('### COVER LETTER')
    resume = parts[0].replace('### TAILORED RESUME', '').strip()
    cover_letter = parts[1].strip()

    # Extract company name from filename (format: [INITIALS]_JobReq_CompanyName.pdf)
    company_name = job_req.split('_')[2].replace('.pdf', '')

    # Upload to S3 with user's initials
    r = upload_md_as_pdf_to_s3(resume, OUTPUT_BUCKET, f"{USER_INITIALS}_{company_name}_R.pdf")
    c = upload_md_as_pdf_to_s3(cover_letter, OUTPUT_BUCKET, f"{USER_INITIALS}_{company_name}_CL.pdf")

    return r, c


def batch_process_today():
    """
    Batch process all job requirements uploaded today.

    Context: Instead of processing one job at a time, this function
    automatically finds all job req PDFs uploaded today and processes
    them in a batch. It filters by:
    - Filename pattern: [INITIALS]_JobReq_*.pdf
    - Upload date: Today's date

    Cost consideration: Each application costs ~$0.05-0.07 in Claude API calls.
    """
    response = s3_client.list_objects(Bucket=REFERENCE_BUCKET)

    for obj in response['Contents']:
        # Check if it's a job req PDF uploaded today
        if (obj['Key'].startswith(f'{USER_INITIALS}_JobReq_') and 
            obj['Key'].endswith('.pdf') and 
            obj['LastModified'].date() == datetime.today().date()):

            print(f"Processing: {obj['Key']}")
            push_output_to_s3(obj['Key'])
            print(f"Completed: {obj['Key']}\n")
