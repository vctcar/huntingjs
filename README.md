Read Me
# AI-Powered Job Application Generator

An automated workflow that uses AWS services and Claude AI to generate tailored resumes and cover letters for job applications. This tool reads your master resume, personal career context, and job requirements, then creates customized application materials optimized for each specific role.

## Overview

This notebook streamlines the job application process by:
- Reading your master resume and career context from AWS S3
- Extracting job requirements from PDF files
- Using Claude AI (via AWS Bedrock) to generate tailored resumes and cover letters
- Converting markdown outputs to professionally formatted PDFs
- Automatically uploading results to S3
- Supporting batch processing for multiple applications

## Features

- **Automated tailoring**: Matches 80-90% of job requirement keywords
- **Context-aware generation**: Incorporates your personal philosophy and career stories
- **PDF styling**: Custom CSS for professional formatting
- **Batch processing**: Process multiple job applications at once
- **Cloud-native**: All files stored and processed via AWS S3
- **Cost-effective**: ~$0.05-0.07 per application

## Prerequisites

### AWS Services
- AWS Account with access to:
  - S3 (for file storage)
  - Bedrock (for Claude AI access)
  - IAM (for credentials management)

### Python Environment
- Python 3.12+
- Libraries (see requirements.txt):
  - boto3
  - pypdf
  - markdown2
  - weasyprint

## Setup Instructions

### 1. AWS Configuration

#### Create S3 Buckets
Create two S3 buckets:

%%
#### Set up AWS Credentials
You have two options:

**Option A: AWS Access Keys (Standard)**
1. Go to AWS IAM Console
2. Create an IAM user with permissions for S3 and Bedrock
3. Generate access keys
4. Set as environment variables or in secrets console:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

**Option B: Bedrock API Keys (Recommended for prototyping)**
1. Go to AWS Bedrock Console
2. Navigate to "API keys" section
3. Generate a short-term API key (valid 12 hours) or long-term key
4. Set as environment variable:
   - `AWS_BEARER_TOKEN_BEDROCK`

For more details, see: [AWS Bedrock API Keys Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/api-keys.html)

### 2. File Structure Setup

Upload these files to your **reference bucket**:

%%
#### Master Resume Format
Your master resume should be in markdown format with all your experience, skills, and education.

#### Career Context Format
Create a markdown file with:
- **Personal Philosophy**: Your beliefs about your industry/field
- **Career Stories**: Detailed accounts of key projects and accomplishments
- **Special Instructions**: Guidelines for how Claude should tailor your materials

See the template section below for structure.

### 3. Notebook Configuration

Update these variables in the notebook:

%%
### 4. CSS Styling (Optional)

Create a `resume_style.css` file in your working directory for PDF formatting:

%%
## Usage

### Single Job Application

Process one job at a time:

%%
This will generate:
- `ABC_Google_R.pdf` (tailored resume)
- `ABC_Google_CL.pdf` (tailored cover letter)

Both files will be uploaded to your output bucket.

### Batch Processing

Process all job reqs uploaded today:

%%
This automatically finds and processes all PDFs matching:
- Pattern: `[INITIALS]_JobReq_*.pdf`
- Upload date: Today

## File Naming Conventions

**Input files** (in reference bucket):
- Master resume: `[INITIALS]_Master.md`
- Career context: `[INITIALS]_career_context.md`
- Job requirements: `[INITIALS]_JobReq_[CompanyName].pdf`

**Output files** (in output bucket):
- Resume: `[INITIALS]_[CompanyName]_R.pdf`
- Cover letter: `[INITIALS]_[CompanyName]_CL.pdf`

## Cost Estimates

### AWS Bedrock (Claude 3.5 Sonnet)
- Input tokens: ~$3 per million tokens
- Output tokens: ~$15 per million tokens
- **Per application**: $0.05 - $0.07

### AWS S3
- Storage: Minimal (a few cents per month)
- API calls: Negligible for typical usage

**Monthly estimate** (for 20 applications): ~$1-2

## Career Context Template

Here's a template structure for your `career_context.md` file:

%%
## Troubleshooting

### "Access Denied" errors
- Check your IAM permissions include S3 and Bedrock access
- Verify your AWS credentials are set correctly

### PDFs not generating
- Ensure `resume_style.css` exists in your working directory
- Check that WeasyPrint dependencies are installed

### Claude not formatting correctly
- Review your career context instructions
- Ensure the "Special Instructions" section is clear about output format

### Batch processing finds no files
- Verify job req PDFs use correct naming: `[INITIALS]_JobReq_*.pdf`
- Check that files were uploaded today (or modify date filter)

## Security Best Practices

- **Never commit** AWS credentials to version control
- Use `.gitignore` to exclude personal files
- Rotate API keys regularly (especially long-term Bedrock keys)
- Use short-term Bedrock API keys for development
- Limit IAM permissions to only what's needed (S3 + Bedrock)

## Contributing

Feel free to fork this project and adapt it to your needs. Suggestions for improvements:
- Add support for multiple resume versions
- Implement cost tracking and logging
- Add email notification when batch processing completes
- Support for additional output formats (Word, HTML)

## License

[Choose your license - MIT, Apache 2.0, etc.]

## Acknowledgments

Built using:
- AWS Bedrock (Claude 3.5 Sonnet by Anthropic)
- AWS S3
- WeasyPrint for PDF generation