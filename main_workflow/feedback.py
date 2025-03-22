import base64
import os
from google import genai
from google.genai import types
import sys
from fpdf import FPDF
import os
import re
import markdown
from bs4 import BeautifulSoup

def convert_text_to_pdf(input_file, output_pdf, font_family='Courier', font_size=10):
    """
    Convert a text file to PDF while preserving formatting and converting markdown to plain text.
    Handles Unicode characters by replacing them with ASCII equivalents.
    
    Parameters:
    input_file (str): Path to the input text file (potentially containing markdown)
    output_pdf (str): Path for the output PDF file
    font_family (str): Font to use (monospaced fonts like Courier work best for preserving format)
    font_size (int): Font size to use
    """
    # Create PDF object
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Set font (using a monospaced font to preserve formatting)
    pdf.set_font(font_family, '', font_size)
    
    # Calculate line height
    line_height = pdf.font_size * 1.5
    
    # Define replacements for problematic Unicode characters
    replacements = {
        '\u2019': "'",  # right single quotation mark
        '\u2018': "'",  # left single quotation mark
        '\u201c': '"',  # left double quotation mark
        '\u201d': '"',  # right double quotation mark
        '\u2013': '-',  # en dash
        '\u2014': '--', # em dash
        '\u2026': '...', # ellipsis
        '\u00a0': ' ',  # non-breaking space
        # Add more replacements as needed
    }
    
    # Read the entire content of the file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(content)
    
    # Convert HTML to plain text
    soup = BeautifulSoup(html_content, 'html.parser')
    plain_text = soup.get_text()
    
    # Process the plain text line by line
    for line in plain_text.split('\n'):
        # Replace problematic Unicode characters
        for char, replacement in replacements.items():
            line = line.replace(char, replacement)
        
        # Further sanitize by replacing any remaining non-ASCII characters
        line = re.sub(r'[^\x00-\x7F]+', ' ', line)
        
        pdf.cell(0, line_height, line, ln=1)
    
    # Save the PDF
    pdf.output(output_pdf)
    return output_pdf

def auto_convert_on_file_change(input_file, output_pdf):
    """
    Monitor the input file and automatically convert to PDF when it changes.
    
    Parameters:
    input_file (str): Path to the input text file
    output_pdf (str): Path for the output PDF file
    """
    import time
    last_modified = os.path.getmtime(input_file)
    
    print(f"Monitoring {input_file} for changes...")
    
    while True:
        current_modified = os.path.getmtime(input_file)
        if current_modified > last_modified:
            print(f"File changed. Converting to PDF...")
            convert_text_to_pdf(input_file, output_pdf)
            print(f"PDF created: {output_pdf}")
            last_modified = current_modified
        time.sleep(1)  # Check every second





with open("name_json.txt", "r") as f:
    name = f.read()

files_in_directory = os.listdir("dirr")
filename = "dirr/" + files_in_directory[0]

with open("llm_output.txt", "r") as f:
    content = f.read()

with open("output.txt", "r") as f:
    personalized_content = f.read()


with open(name, "r") as f:
    user_profile = f.read()

def generate(filename,content,user_profile,personalized_content):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    files = [
        # Make the file available in local system working directory
        client.files.upload(file=filename),
    ]
    model = "gemini-2.0-flash-thinking-exp-01-21"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
                types.Part.from_text(text=f"""Educational Content Evaluation Protocol
INPUTS REQUIRED

ORIGINAL_CONTENT: [The uploaded file]

CONTENT_ANALYSIS: {content}

USER_PROFILE: {user_profile}

PERSONALIZED_CONTENT: {personalized_content}

# Educational Content Evaluation Protocol


## EVALUATION FRAMEWORK

1. CONTENT PRESERVATION CHECK
---INSTRUCTIONS---
- Verify all original learning objectives are maintained
- Confirm key concepts remain intact
- Check difficulty matches learner's capabilities
---SCORING---
* Completeness (1-5): All objectives present?
* Accuracy (1-5): Core information preserved?
* Difficulty (1-5): Appropriate challenge level?

2. ANALYSIS IMPLEMENTATION AUDIT
---INSTRUCTIONS---
- Cross-reference analysis recommendations
- Categorize as: Implemented/Partial/Missing
- Assess implementation quality
---SCORING---
For each C1-C14 criterion:
* Implementation (1-5): Recommendation adoption
* Quality (1-5): Execution effectiveness
* Impact (1-5): Learning enhancement

3. PERSONALIZATION EFFECT ANALYSIS
---INSTRUCTIONS---
- Evaluate learning style alignment
- Assess interest integration
- Check engagement balance
---SCORING---
* Style Match (1-5): Modality alignment
* Interest Use (1-5): Relevance to profile
* Engagement (1-5): Added value without distraction

4. QUALITY COMPARISON MATRIX
---INSTRUCTIONS---
- Create improvement heatmap
- Calculate transfer potential
- Identify innovation points
---SCORING---
* Quality Delta (-5 to +5): Net improvement
* Engagement Gain (1-5): Motivation boost
* Structure (1-5): Organization improvements
* Cognition (1-5): Challenge optimization

5. HOLISTIC ASSESSMENT
---INSTRUCTIONS---
- Synthesize all findings
- Identify critical success factors
- Highlight improvement opportunities
- Provide actionable recommendations
---SCORING---
* Implementation (1-10): Recommendation adoption
* Personalization (1-10): Profile alignment
* Integrity (1-10): Educational value
* Innovation (1-10): Novel effective approaches

## OUTPUT REQUIREMENTS
<<STRUCTURED REPORT FORMAT>>
# Evaluation Report

[1] Preservation Summary
- Missing elements: [List]
- Preserved strengths: [Examples]
- Difficulty adjustments: [Changes]

[2] Implementation Status
- Critical gaps: [Unaddressed C1-C14]
- Best implementations
- Quality issues: [Poor executions]
- Impact assessment: [Learning enhancement]

[3] Personalization Audit
- Style alignment: [Evidence]
- Interest integration: [Examples]
- Over-personalization: [If any]
- Engagement balance: [Positive/Negative]

[4] Quality Comparison
- Key improvements
- Transfer potential: [Before vs After]
- Innovation score: [Novel elements]
- Engagement score: [Motivation boost]
- Structure score: [Organization]
- Cognition score: [Challenge optimization]
- Quality delta: [Net improvement]

## PROCESS RULES
1. Cite specific text examples for all scores
2. Maintain educational priorities over engagement
3. Use concrete before/after comparisons
4. Flag over-personalization risks
5. Highlight critical success factors
6. Avoid generic language
7. Provide actionable recommendations

//END PROMPT//
"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=2,
        top_p=0.95,
        top_k=64,
        max_output_tokens=65536,
        response_mime_type="text/plain",
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        chunk_text = chunk.text
        print(chunk_text, end="")
        response_text += chunk_text
    
    return response_text

if __name__ == "__main__":
    gg = generate(filename,content=content,user_profile=f"profiles_user/{name}.json",personalized_content=personalized_content)
    with open("output_feedback.txt", "w") as f:
        f.write(gg)
    input_file = "output_feedback.txt"
    output_pdf = "evaluation_report.pdf"
    
    # Option 1: Convert once
    convert_text_to_pdf(input_file, output_pdf)
    print(f"PDF created successfully: {output_pdf}")