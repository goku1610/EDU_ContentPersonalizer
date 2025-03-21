import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    files = [
        # Make the file available in local system working directory
        client.files.upload(file="15_Photosynthesis.pdf"),
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
                types.Part.from_text(text="""You are an expert educational content analyst with deep knowledge across multiple disciplines. Your task is to evaluate the attached PDF document and assess its quality and learning potential using a comprehensive set of criteria.
 
PDF FOR ANALYSIS:
[Attached PDF file]
 
TARGET AUDIENCE:
8th grade Indian Student
 
ANALYSIS INSTRUCTIONS:
Carefully review the attached PDF document. Conduct a thorough assessment based on the following quality criteria. For each criterion:
1. Provide a score from 1-5 (where 1=poor, 3=adequate, 5=excellent)
2. Support your rating with specific evidence from the PDF
3. Suggest specific learning strategies or enhancements to maximize the document's educational value
 
QUALITY CRITERIA:
 
1. CONTENT ACCURACY AND CURRENCY
   - Is the information presented accurate and up-to-date?
   - Does it reflect current understanding in the field?
   - Score (1-5):
 
2. CONCEPTUAL CLARITY
   - How clearly are key concepts explained?
   - Are complex ideas broken down effectively?
   - Score (1-5):
 
3. LOGICAL STRUCTURE AND FLOW
   - Is the content organized in a logical, coherent manner?
   - Does the structure support progressive understanding?
   - Score (1-5):
 
4. VISUAL AND MULTIMEDIA ELEMENTS
   - How effectively do diagrams, charts, or other visual aids support learning?
   - Are multimedia elements (if present) integrated meaningfully?
   - Score (1-5):
 
5. ENGAGEMENT AND RELEVANCE
   - How likely is the content to interest and engage the target audience?
   - Does it connect to real-world applications or student experiences?
   - Score (1-5):
 
6. COGNITIVE CHALLENGE (Bloom's Taxonomy)
   - At what levels of Bloom's Taxonomy does the text operate?
   - Does it promote higher-order thinking skills?
   - Score (1-5):
 
7. PROBLEM-SOLVING AND CRITICAL THINKING
   - How effectively does the text encourage analytical and problem-solving skills?
   - Are there opportunities for applying knowledge to novel situations?
   - Score (1-5):
 
8. INTERDISCIPLINARY CONNECTIONS
   - Does the text make meaningful connections to other subjects or fields?
   - How well does it promote holistic understanding?
   - Score (1-5):
 
9. SCAFFOLDING AND SUPPORT
   - Does the text provide appropriate scaffolding for complex ideas?
   - Are there sufficient examples, analogies, or explanations to support understanding?
   - Score (1-5):
 
10. METACOGNITIVE STRATEGIES
    - Does the text encourage self-reflection on learning?
    - Are there prompts for monitoring comprehension or setting learning goals?
    - Score (1-5):
 
11. ASSESSMENT AND FEEDBACK OPPORTUNITIES
    - Are there embedded questions, problems, or activities for self-assessment?
    - How well do these align with the learning objectives?
    - Score (1-5):
 
12. INCLUSIVE AND CULTURALLY RESPONSIVE CONTENT
    - Does the text represent diverse perspectives and experiences?
    - Is the content accessible and relevant to learners from various backgrounds?
    - Score (1-5):
 
13. VOCABULARY AND TERMINOLOGY DEVELOPMENT
    - How effectively does the text introduce and reinforce subject-specific vocabulary?
    - Are new terms presented in supportive contexts?
    - Score (1-5):
 
14. SCIENTIFIC/MATHEMATICAL LITERACY (for STEM texts)
    - How well does the text promote understanding of scientific/mathematical processes?
    - Does it encourage application of the scientific method or mathematical reasoning?
    - Score (1-5):
 
15. LITERARY MERIT (for humanities texts)
    - Does the text exemplify high-quality writing in the discipline?
    - Are literary or rhetorical devices used effectively?
    - Score (1-5):
 
OVERALL ASSESSMENT:
1. Calculate the overall quality score (average of individual criteria scores)
2. Identify the three strongest features of the text in promoting deep learning
3. Identify three opportunities for enhancing the text's learning potential
4. Recommend specific teaching and learning strategies to maximize educational value
5. Suggest three focused activities or projects that would deepen engagement with the material
 
LEARNING ENHANCEMENT RECOMMENDATIONS:
Based on your analysis, provide specific, actionable recommendations for:
1. How to supplement the text to address any gaps or weaknesses in promoting deep learning
2. Pre-reading activities to activate prior knowledge and set learning goals
3. During-reading strategies to promote active engagement and comprehension
4. Post-reading activities to consolidate learning and encourage application
5. Differentiation approaches to support diverse learners and learning styles
 
BLOOM'S TAXONOMY ALIGNMENT:
Evaluate how the text aligns with each level of Bloom's Taxonomy:
1. Remember: [Score 1-5 and brief explanation]
2. Understand: [Score 1-5 and brief explanation]
3. Apply: [Score 1-5 and brief explanation]
4. Analyze: [Score 1-5 and brief explanation]
5. Evaluate: [Score 1-5 and brief explanation]
6. Create: [Score 1-5 and brief explanation]
 
PDF-SPECIFIC CONSIDERATIONS:
1. Evaluate the document's formatting, layout, and overall readability
2. Assess the effectiveness of any embedded multimedia elements (if present)
3. Comment on the document's accessibility features for diverse learners
4. Analyze how well the PDF format supports or enhances the content presentation"""),
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
    generate()
