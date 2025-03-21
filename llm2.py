import base64
import os
from google import genai
from google.genai import types

# with open("user_input.txt", "r") as f:
#     user_input = f.read()

with open("Photosynthesis.txt", "r") as f:
    data = f.read()

def generate(strr):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash-thinking-exp-01-21"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=strr),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        top_k=64,
        max_output_tokens=65536,
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    
    content = f"""{data}/nFor the above text i would like you to\n1. Identify the primary subject domain: (history/science/math/language/etc.)

2. Assess the content structure:
   - Sequential/chronological material
   - Conceptual/theoretical material
   - Procedural/skill-based material
   - Descriptive/informational material

3. Determine learning objectives:
   - Knowledge acquisition (facts, information)
   - Skill development (procedures, techniques)
   - Conceptual understanding (principles, theories)
   - Analysis capabilities (critical thinking)
   - Creative application \n\n\n\n
    Finally give the answer in a strcutured format for all the three parts.


Give the final answer in this format:: 
    1: = [<primary subject domain>],
    2: = [<content structure/structures>],
    3: = [<learning objective/objectives>]
    Strictly return this and nothing else."""
    
    content_profile = generate(content)
    print(content_profile)