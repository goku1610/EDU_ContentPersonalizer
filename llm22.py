import os
import glob
from google import genai
from google.genai import types
from dotenv import load_dotenv

def generate_content():
    # Load environment variables from .env file
    load_dotenv()
    
    # Initialize the Gemini client
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    
    # Read content from analysis.txt
    try:
        with open("analysis.txt", "r", encoding="utf-8") as f:
            analysis_content = f.read()
    except Exception as e:
        print(f"Error reading analysis.txt: {e}")
        analysis_content = ""
    
    # Read content from user_profile.txt
    try:
        with open("user_profile.txt", "r", encoding="utf-8") as f:
            profile_content = f.read()
    except Exception as e:
        print(f"Error reading user_profile.txt: {e}")
        profile_content = ""
    
    # Find PDF files in the 'pdfs' folder
    pdf_folder = os.path.join(os.getcwd(), "pdfs")
    pdf_files = glob.glob(os.path.join(pdf_folder, "*.pdf"))
    uploaded_files = []
    
    # Upload PDF files if found
    if pdf_files:
        for pdf_file in pdf_files:
            try:
                file = client.files.upload(file=pdf_file)
                uploaded_files.append(file)
                print(f"Uploaded: {pdf_file}")
            except Exception as e:
                print(f"Error uploading {pdf_file}: {e}")
    else:
        print("No PDF files found in the 'pdfs' folder")
    
    # Prepare content for the model
    parts = []
    
    # Add text content first
    prompt_text = f"""
Analysis Content:
{analysis_content}

User Profile:
{profile_content}

craft a personalised version of the complete study content in the pdf, using the analysis of the content and user profile provided. The content should be tailored to the target audience, considering their age, class level, learning style preferences, and core competencies. The output should be engaging and suitable for the specified subject area.
"""
    parts.append(types.Part.from_text(text=prompt_text))
    
    # Add PDF files if any were uploaded
    for file in uploaded_files:
        parts.append(
            types.Part.from_uri(
                file_uri=file.uri,
                mime_type=file.mime_type,
            )
        )
    
    # Create content for the model
    contents = [
        types.Content(
            role="user",
            parts=parts,
        ),
    ]
    
    # Set configuration with temperature 1.8
    generate_content_config = types.GenerateContentConfig(
        temperature=1.8,  # Setting temperature to 1.8 as requested
        top_p=0.95,
        top_k=64,
        max_output_tokens=65536,
        response_mime_type="text/plain",
    )
    
    # Model selection - using gemini-flash-2.0 as requested
    model = "gemini-2.0-flash"
    
    response_text = ""
    # Generate content using the model
    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                print(chunk.text, end="")
                response_text += chunk.text
    except Exception as e:
        error_message = f"Error generating content: {e}"
        print(error_message)
        response_text = error_message
    
    # Save the generated content to output.txt
    try:
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(response_text)
        print("\n\nResponse saved to output.txt")
    except Exception as e:
        print(f"Error saving to output.txt: {e}")

if __name__ == "__main__":
    generate_content()