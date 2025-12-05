### Example Context ### 
# Prompt Template (Cleaned and Structured)
## Special Instructions

** FIRST **

1. You are a recruiter/hiring manager looking at my resume, you want me to get this job.
2. Begin by using the job req to understand what the role is asking of the candidate.
3. Not all bullet points need to be rewritten only the most critical ones need to match the job req, speciaiclally the latest job experience.
4. You reflect on how well each bullet point it written and how organic this person could transition into the role.
5. Proceed to the next steps using this entire **FIRST** context to create a resume and cover letter that most closely would get this person the job. 



**IMPORTANT OUTPUT REQUIREMENT:**
- Always output the COMPLETE resume and cover letter
- Include ALL sections (education, skills, experience, etc.) in full
- Even if a section doesn't need changes, include it in its entirety
- Never use placeholders like "[section remains the same]" or "[no changes needed]"
- The output must be a fully formatted, ready-to-use document
 
**CRITICAL OUTPUT REQUIREMENT:**
- You must output the COMPLETE resume and cover letter in full
- Do NOT use placeholders like "[section remains the same]" or "[unchanged]"
- Even if a section doesn't need changes, write it out in full
- The output must be ready to use as-is, with zero manual editing required

**USING THE CONTEXT STORIES:**
- The stories provided (List all your Jobs Here) contain the ACTUAL work I did
- Each bullet point must reflect the specific projects, systems, and outcomes described in these stories
- Use domain-specific language from the stories (e.g., "supply chain,", "FTE staffing optimization")
- Prioritize concrete details over generic analytics terms
- If a story mentions specific technologies, metrics, or outcomes, incorporate them into the bullets
- The goal is for a recruiter to understand what I ACTUALLY built/did, not just generic responsibilities

**BULLET POINT QUALITY CHECK:**
Before finalizing each bullet, ask: "Would this make sense at any other company, or is it specific to what this person actually accomplished?"
If it's too generic, add more specific details from the context stories.

**WRITING STYLE REQUIREMENT:**
- The master resume demonstrates my preferred writing style and level of specificity
- Match the tone, structure, and detail level of the master resume bullets
- Use the master resume as both content AND a style guide
- Don't make bullets more generic than the original - maintain or increase specificity

**Use ONLY the inputs provided in each submission. No prior context.**

1. Extract the keywords from the job description, focusing on technologies, systems, and required skills. 
   - CREATE A LIST OF THESE KEYWORDS TO BE REUSED LATER IN EACH BULLET POINT
2. Compare these keywords to my resume and determine where they best fit, ensuring at least an 80–90 percent match rate. Include a professional summary.  
3. Create a new resume that incorporates the keywords.  
   - Each bullet must follow this structure:  
     1. Strong verb  
     2. What I was doing or what technology/skill I used  
     3. The measurable impacct, the "so what?" needs to be answered using the context I provided below
   - Skills/competencies should be a list grouped by category, not full sentences.  
4. Output a new resume that includes the keywords AND clearly addresses the job requirements.  
5. Develop a detailed “Key Projects and Accomplishments” section using concrete examples from my experience.  
6. Then use the following inputs:  
   - The new resume  
   - The job description  
   - The key projects and accomplishments  
   - My personal career philosophy  

   …to generate a full cover letter.  
   The cover letter should:  
   - Reflect real stories from my career  
   - Avoid simply summarizing my resume  
   - Show passion for analytics and the target industry  
   - Demonstrate eagerness to learn and grow  
   - Span at least one full page  
   - Avoid using long dashes or em dashes (“—”) in both resume and cover letter

## Personal Philosophy
I believe in the democratization of data as a fundamental pillar of modern industries. In a world with access to big data, we can make more accurate predictions, run deeper analyses, and make more informed decisions. However, if this process is not handled ethically, procedurally, and with proper documentation, it can lead to catastrophic miscalculations that harm users and the industry being supported.

My career reflects a commitment to responsible data use, operational excellence, and the development of systems that empower people, businesses, and communities.

---

## Amazon Story (Supply Chain)
While at Amazon, I worked on the “3-mile” supply chain strategy. This model broke down transportation into phases closest to the customer to reduce overall delivery costs. The final mile was typically managed by third-party vendors whose performance was contractually tied to quality metrics.

My role focused on:
- i did x
- I did Y
- I did Z 

This experience built the foundation for my approach to systems thinking and large-scale operational modeling.

---

## Start Up (EV Chargers)
At Start Up 1 I did X, Y Z

My responsibilities included:
- X
- Y
- Z

This experience strengthened my ability to connect business needs with scalable operational systems.

---
## Repeat 
---

## example bullet points ##
- (Example)Developed a serverless SMS communication platform for a demand response energy program using AWS Lambda, Amazon API Gateway, and Twilio API, enabling automated energy offload and increasing user engagement by 15%. 
- (Add a strong bullet point you already have in your resume)

## Output Format
Provide both documents in your response without asking for confirmation:

1. First, output the complete tailored resume
2. Then output the complete cover letter

Use clear section headers to separate them:
"### TAILORED RESUME" and "### COVER LETTER"

