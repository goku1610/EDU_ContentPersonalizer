import base64
import os
import sys
from google import genai
from google.genai import types
import glob
import json

# Get JSON file name from command-line argument
if len(sys.argv) > 1:
    json_file = sys.argv[1]
    file_path = f'profiles_user/{json_file}.json'
else:
    # Default file if no argument is provided
    file_path = 'profiles_user/f.json'
    print("No JSON file specified, using default: f.json")

try:
    with open(file_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"Error: File {file_path} not found")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: File {file_path} contains invalid JSON")
    sys.exit(1)

reader = data.get('reader')
learning_modality = data.get('learning_modality')
core_competencies = data.get('core_competencies')

papa_prompt = f"""# ADVANCED EDUCATIONAL CONTENT ANALYSIS PROMPT


## CORE ANALYSIS PARAMETERS
CONTENT_TO_ANALYZE: [attached PDF/TEXT CONTENT]

[
{reader}
{learning_modality}
{core_competencies}
]



## IN-DEPTH QUALITY CRITERIA INSTRUCTIONS

[1] CONTENT QUALITY ASSESSMENT
INSTRUCTIONS:
- Score each criterion 1-5 (1=poor, 3=adequate, 5=excellent)
- Cite 2+ specific text examples per criterion
- Suggest concrete improvements per criterion

CRITERIA_DETAILS:

C1: CONTENT ACCURACY & CURRENCY
- Verify factual correctness against current standards
- Check publication/update dates
- Identify outdated information
SCORING_QUESTIONS:
1. Is information verified by authoritative sources?
2. Does content reflect recent developments?
3. Are statistics/data sources current?

C2: CONCEPTUAL CLARITY 
- Analyze explanation depth for key concepts
- Evaluate use of examples/analogies
- Assess technical term definitions
SCORING_QUESTIONS:
1. Are complex ideas broken into components?
2. Does sequencing build conceptual understanding?
3. Are relationships between concepts explicit?

C3: STRUCTURAL LOGIC
- Map content flow diagrammatically
- Identify transition quality between sections
- Evaluate coherence of argumentation
SCORING_QUESTIONS:
1. Does organization follow pedagogical best practices?
2. Are sections proportioned appropriately?
3. Do headings accurately reflect content?

C4: VISUAL/MULTIMEDIA EFFECTIVENESS
- Catalog all non-text elements
- Assess multimedia-text integration
- Evaluate accessibility of visual data
SCORING_QUESTIONS:
1. Do visuals complement textual content?
2. Are complex processes diagrammed effectively?
3. Are alt-text/captions informative?

C5: ENGAGEMENT & RELEVANCE
- Calculate real-world connection frequency
- Analyze narrative voice/style
- Identify cultural relevance factors
SCORING_QUESTIONS:
1. Does content link to learner experiences?
2. Are authentic problems/scenarios used?
3. Is material culturally responsive?

C6: COGNITIVE CHALLENGE (BLOOM'S TAXONOMY)
- Tag learning objectives to Bloom's levels
- Calculate HOTS/LOTS distribution
SCORING_QUESTIONS:
1. Does content progress across cognitive levels?
2. Are higher-order tasks scaffolded appropriately?

C7: CRITICAL THINKING & PROBLEM-SOLVING
- Identify open-ended questions
- Evaluate reasoning prompts
SCORING_QUESTIONS:
1. Are learners asked to justify conclusions?
2. Does content present ambiguous scenarios?

C8: INTERDISCIPLINARY CONNECTIONS
- Count explicit cross-disciplinary links
- Assess integration depth
SCORING_QUESTIONS:
1. Are connections superficial or substantive?
2. Do activities require multi-domain knowledge?

C9: SCAFFOLDING & SUPPORT
- Analyze example density and quality
- Evaluate gradual complexity progression
SCORING_QUESTIONS:
1. Are worked examples provided?
2. Is fading used appropriately?

C10: METACOGNITIVE STRATEGIES
- Identify reflection prompts
- Evaluate self-assessment tools
SCORING_QUESTIONS:
1. Does content model expert thinking processes?
2. Are learners prompted to monitor understanding?

C11: ASSESSMENT ALIGNMENT
- Map activities to learning objectives
- Evaluate feedback mechanisms
SCORING_QUESTIONS:
1. Are assessments formative and summative?
2. Do rubrics align with stated goals?

C12: VOCABULARY DEVELOPMENT
- Analyze context clues for new terms
- Count intentional vocabulary repetitions
SCORING_QUESTIONS:
1. Are glossaries/definition boxes provided?
2. Are terms reinforced across contexts?

C13: STEM LITERACY (STEM TEXTS)
- Evaluate scientific method integration
- Assess data literacy components
SCORING_QUESTIONS:
1. Are learners guided through inquiry cycles?
2. Are datasets provided for analysis?

C14: LITERARY MERIT (HUMANITIES TEXTS)
- Analyze rhetorical device usage
- Evaluate primary source engagement
SCORING_QUESTIONS:
1. Does text model disciplinary writing standards?
2. Are literary devices used purposefully?

## TRANSFER ANALYSIS MATRIX (ENHANCED)

TRANSFER_CATEGORIES:
|| NEAR TRANSFER ||
- PROCEDURAL: Step-by-step application
  EVIDENCE_REQ: <<exact text examples of algorithms/routines>>
  
- CONTEXTUAL: Slightly modified situations
  EVIDENCE_REQ: <<examples with varied parameters/settings>>

|| CONDITIONAL TRANSFER ||
- STRATEGY_SELECT: Multiple solution paths
  EVIDENCE_REQ: <<text prompting approach comparison>>

- METACOGNITIVE: Reflection prompts
  EVIDENCE_REQ: <<self-assessment questions/checklists>>

|| FAR TRANSFER ||
- CROSS-DOMAIN: Interdisciplinary links
  EVIDENCE_REQ: <<explicit connections to other fields>>
  
- NOVEL_PROBLEM: Unfamiliar challenges
  EVIDENCE_REQ: <<open-ended problem statements>>

## COGNITIVE DEMAND PROFILE

BLOOMS_ANALYSIS:
- Tag each learning objective/activity to Bloom level
- Calculate time/content percentage per level
- Identify highest-level cognitive task

REQUIRED_OUTPUT:
B1 (Remember): [%] 
  EXAMPLES: 
  1. <<List of key terms>> 
  2. <<Factual recall questions>>

B2 (Understand): [%]
  EXAMPLES:
  1. <<Concept summaries>>
  2. <<Paraphrasing exercises>>

B3 (Apply): [%]
  EXAMPLES:
  1. <<Procedure executions>>
  2. <<Algorithm implementations>>

B4 (Analyze): [%]
  EXAMPLES:
  1. <<Data interpretation exercises>>
  2. <<Comparative analyses>>

B5 (Evaluate): [%]
  EXAMPLES:
  1. <<Peer review activities>>
  2. <<Hypothesis validations>>

B6 (Create): [%]
  EXAMPLES:
  1. <<Design challenges>>
  2. <<Original solution development>>

HOTS_PERCENTAGE: [B4+B5+B6] = [%]

## DIFFERENTIATION DEPTH ANALYSIS

ACCOMMODATION_LEVELS:
4 = Embedded universal design elements
3 = Suggested adaptation strategies
2 = Possible with modification
1 = No apparent support

ASSESSMENT_FOCI:
- Multimodal input options
- Alternative expression formats
- Scaffolding granularity
- Language accessibility features

LEARNER_PROFILES:
Visual: [1-4] <<Diagram/chart references>>
Auditory: [1-4] <<Podcast/audio gaps>>
Kinesthetic: [1-4] <<Hands-on activity absences>>
ELL: [1-4] <<Language support elements>>

## ENHANCEMENT PRIORITIZATION MATRIX

PRIORITY_1: Criteria scoring <2 with high learning impact
PRIORITY_2: Missing transfer types per TPI calculation
PRIORITY_3: HOTS activities below 30% threshold
PRIORITY_4: Learner types with accommodation <2

## PROCESSING RULES
1. Cross-validate quality scores against transfer evidence
2. Align cognitive profile with target audience needs
3. Flag content-rubric mismatches
4. Ensure enhancement suggestions address root causes
5. Maintain strict evidence-based justification

## OUTPUT VALIDATION CHECKS
[REQUIRED BEFORE FINALIZING]
1. Criteria scores match cited evidence
2. Transfer matrix aligns with TPI calculation
3. Cognitive percentages sum to 100% ±2%
4. Enhancement priorities match flagged issues
5. Sample implementation demonstrates key improvements

## TPI CALCULATION FRAMEWORK
1. Near_Score = (Present Transfer Types/3)*10
2. Conditional_Score = (Present Transfer Types/3)*10
3. Far_Score = (Present Transfer Types/3)*10
4. TPI = (Near*0.2)+(Conditional*0.3)+(Far*0.5)

INTERPRETATION:
8-10 = Exemplary transfer potential
6-7.9 = Strong transfer potential
4-5.9 = Moderate transfer potential
<4 = Limited transfer potential

## SAMPLE IMPLEMENTATION TEMPLATE
ORIGINAL: <<"Cells divide through mitosis">>
ENHANCED: <<"Design an experiment comparing mitosis rates in normal vs. stressed cells">>
RATIONALE:
- Bloom's: B1→B6 (Recall→Create)
- Transfer: Adds Novel Problem-Solving (Far)
- Differentiation: Kinesthetic engagement boost

## AUTO-FLAGS SYSTEM
CRITICAL_WEAKNESS: Any criterion score <2
TRANSFER_DEFICIT: TPI <4
COGNITIVE_IMBALANCE: HOTS <30%
ACCESSIBILITY_GAP: Any learner profile score <2

##EXPLICIT INSTRUCTIONS
  -Do not modify the input no matter how low it scores, find the scores for the original input

// END OF PROMPT //


"""

def get_files_from_directory(directory_path):
    return glob.glob(os.path.join(directory_path, '*.pdf')) + glob.glob(os.path.join(directory_path, '*.txt'))

def generate(strr):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    directory_path = 'dirr'
    files_to_upload = get_files_from_directory(directory_path)

    files = [
        client.files.upload(file=file_path) for file_path in files_to_upload
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
                types.Part.from_text(text=strr),
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

    # Create a file to store the output
    output_file = open("llm_output.txt", "w", encoding="utf-8")
    
    full_response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")
        full_response += chunk.text
    
    # Write the complete response to the file
    output_file.write(full_response)
    output_file.close()
    
    print("\n\nOutput has been saved to llm_output.txt")

def generate_content(analysis_content,file_path):
    # Load environment variables from .env file
    
    # Initialize the Gemini client
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    
    
    # Read content from user_profile.txt
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            profile_content = f.read()
    except Exception as e:
        print(f"Error reading user_profile.txt: {e}")
        profile_content = ""
    
    # Find PDF and TXT files in both 'pdfs' and 'dirr' folders
    folder = os.path.join(os.getcwd(), "dirr")
    
    # Get all PDF and TXT files from both directories
    pdf_files = []
    txt_files = []
    

    if os.path.exists(folder):
        pdf_files.extend(glob.glob(os.path.join(folder, "*.pdf")))
        txt_files.extend(glob.glob(os.path.join(folder, "*.txt")))
    
    uploaded_files = []
    
    # Upload PDF and TXT files if found
    all_files = pdf_files + txt_files
    if all_files:
        for file_path in all_files:
            try:
                file = client.files.upload(file=file_path)
                uploaded_files.append(file)
                print(f"Uploaded: {file_path}")
            except Exception as e:
                print(f"Error uploading {file_path}: {e}")
    else:
        print("No PDF or TXT files found in the 'pdfs' and 'dirr' folders")
    
    # Prepare content for the model
    parts = []
    
    # Add text content first
    prompt_text = f"""
Original Content = [Uploaded as a file]

Analysis Content:
{analysis_content}

User Profile:
{profile_content}

now based on this user_profile personalize this lesson based on the given recommendations to improve learning, knowledge transfer, focus and overall content engagement.
output the new and refined lesson without skipping any topic or context.
The final output should be in a presentable format such that it can be given directly to the end user. Do not return your thoughts or justification."""
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
    model = "gemini-2.0-flash-thinking-exp-01-21"
    
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
    analysis_content = generate(papa_prompt)
    generated_content = generate_content(analysis_content,file_path)
    print(generated_content)

