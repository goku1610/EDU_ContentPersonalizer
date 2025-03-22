import base64
import os
from google import genai
from google.genai import types
import sys

if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    print("Error: Please provide a name as an argument. Example: python3 feedback.py username")
    sys.exit(1)

files_in_directory = os.listdir("dirr")
filename = "dirr/" + files_in_directory[0]

with open("llm_output.txt", "r") as f:
    content = f.read()

with open("output.txt", "r") as f:
    personalized_content = f.read()


with open(f"profiles_user/{name}.json", "r") as f:
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

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate(filename,content=content,user_profile=f"profiles_user/{name}.json",personalized_content=personalized_content)
