# EDUContentPersonalizer: Educational Content Personalization System

## Project Overview

### Project Demo
https://www.youtube.com/watch?v=b-D8xti3DdU

### Overview
EDUContentPersonalizer is an AI-powered educational content personalization system that transforms standard educational materials into personalized learning experiences tailored to individual learner profiles. The system operates in two main stages:

1. **Content Analysis Stage**: Analyzes educational content using scientific methodologies to assess quality, identify drawbacks, and highlight areas for improvement.
2. **Personalization Stage**: Combines the content analysis with user profiles to create personalized educational materials that address the specific needs, interests, and learning preferences of individual readers.


## Important Notes
- **The `dirr` directory must contain only a single file at a time.** Having multiple files in this directory may cause unexpected behavior.
- Make sure your source content file is either a .txt or a PDF file.
- If the output does not appear on the browser, try again or check the result in `main_workflow/output.txt`

### Setup
1. Clone the GitHub repository:
   ```
   git clone https://github.com/goku1610/EDU_ContentPersonalizer
   cd EDU_ContentPersonalizer
   ```
2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
4. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Set up your Gemini API key (required for the LLM):
   - On Windows (PowerShell):
      ```
      New-Item -Path .env -ItemType File
      Add-Content .env "GEMINI_API_KEY=your_api_key_here"
      ```
   - On macOS and Linux
      ```
      touch .env
      echo "GEMINI_API_KEY=your_api_key_here" >> .env
      ```

## Usage

### Running via GUI (Recommended)

#### Running the Web Interface
To use the frontend web interface:
```
cd main_workflow/
python3 app.py
```
This will:
1. Start a local web server
2. Allow you to access the interface through your browser
3. Provide a user-friendly way to select profiles and upload content
4. Display personalized content in a formatted manner

#### Web Interface Workflow
Follow these steps to personalize educational content:

1. Access the application at http://127.0.0.1:5000/
2. Select one of the pre-configured user profiles or upload a custom profile (text file containing relevant information about the learner)(a sample learner_text is provided in /user_data_to_profile/user_profile_example.txt)
3. Upload the educational material to be personalized (.txt file/PDF file) (sample text on photosynthesis present in /dirr/Photosynthesis.txt)
4. Click "Upload" and wait for processing (approximately 20-90 seconds)
5. Review the personalized output presented on screen

**Note:** If you encounter an empty output, this may be due to network issues or LLM server-side errors. In such cases, terminate the application process and restart it by running `app.py` again.

### Running via CLI

#### Running the Personalization Pipeline using Terminal
To process educational content and generate personalized output using only Terminal:
```
python3 main_workflow/newmain.py [profile_name]
```
Where `profile_name` is the name of the JSON file in the `profiles_user/` directory (without the .json extension).

For example:
```
python3 main_workflow/newmain.py f    # Uses profiles_user/f.json
python3 main_workflow/newmain.py j    # Uses profiles_user/j.json
```

If no profile name is specified, the system will default to using `f.json`.

This will:
1. Analyze the educational content files in `dirr/`
2. Generate the content analysis in `llm_output.txt`
3. Combine this analysis with the specified user profile from `profiles_user/`
4. Create the personalized content in `output.txt`

#### Selecting a User Profile
The system allows you to easily switch between different user profiles:

1. Use the command-line argument to specify which profile to use (e.g., `python3 main_workflow/newmain.py j`)
2. This eliminates the need to manually edit th escript when switching between profiles
3. You can still modify `newmain.py` directly if you prefer to hardcode a specific profile

#### Creating New User Profiles
To convert raw user data into a structured profile:
```
python3 user_data_to_profile/user_data_to_profile.py
```
This will:
1. Read raw user data from `user_data_example.txt`
2. Convert it to a structured profile based on `profile_structure.txt`
3. Generate a user profile in `profile_generated.txt`

#### Evaluating Personalization Quality Through Feedback Scoring
To assess the quality of the personalization:
```
python3 main_workflow/feedback.py
```
This will:
1. Analyze the original content, personalized output, and user profile
2. Generate feedback on the personalization quality
3. Output evaluation results to `output_feedback.txt`

## Working 

### Stage 1: Content Analysis
Analyzes the educational content provided in the `dirr` directory using a LLM  prompt:

1. The system reads the content file (txt/pdf) from the `dirr` directory
2. Perfroms Comprehensive Quality Criteria Assessment
The core of the evaluation framework consists of 14 detailed quality criteria (C1-C14) assessed
on a 1-5 scale:
1. Content Accuracy & Currency (C1) - Evaluates factual correctness and timeliness
2. Conceptual Clarity (C2) - Assesses explanation depth and use of examples
3. Structural Logic (C3) - Examines content flow and transitional quality
4. Visual/Multimedia Effectiveness (C4) - Analyzes non-text elements and accessibility
5. Engagement & Relevance (C5) - Measures real-world connections and cultural relevance
6. Cognitive Challenge (C6) - Maps content to Bloom's taxonomy levels
7. Critical Thinking & Problem-Solving (C7) - Identifies open-ended questions and reasoning
prompts
8. Interdisciplinary Connections (C8) - Counts cross-disciplinary links and integration depth
9. Scaffolding & Support (C9) - Examines example density and complexity progression
10. Metacognitive Strategies (C10) - Identifies reflection prompts and self-assessment tools
11. Assessment Alignment (C11) - Maps activities to learning objectives
12. Vocabulary Development (C12) - Analyzes context clues and term reinforcement
13. STEM Literacy (C13) - Evaluates scientific method integration and data literacy components
14. Literary Merit (C14) - Analyzes rhetorical device usage (for humanities texts)
3. The analysis results are stored in `llm_output.txt`, providing detailed insights into:
   - Strengths and weaknesses of the content
   - Areas requiring improvement
   - Cognitive demand profile
   - Transfer potential index
   - Differentiation depth analysis
   - Enhancement prioritization matrix

### Stage 2: Content Personalization
Takes the content analysis and combines it with user profile data:

1. The system reads the user profile from the `profiles_user` directory
2. It merges the content analysis findings with the user's:
   - Primary and secondary interests
   - Learning style preferences
   - Narrative frameworks
   - Personalization vectors
   - Engagement triggers
3. Using this combined information, the system then generates a personalized version of the educational content that:
   - Aligns with the user's interests and preferences
   - Addresses the content quality issues identified in Stage 1
   - Creates connections to topics the user cares about
   - Adjusts the presentation format to match learning style preferences
   - Enhances engagement through personalized examples and analogies
4. The final personalized content is saved to `output.txt`

### User Profile System
Uses a structured user profile system to store information about learners:

- Profiles are stored as JSON files in the `profiles_user` directory
- Each profile contains detailed information about:
  - Demographics (age, class/grade)
  - Primary interests with significance levels
  - Secondary interests with application contexts
  - Learning style preferences
  - Narrative frameworks the user responds to
  - Personalization vectors that guide content adaptation
  - Engagement triggers that capture attention

The `user_data_to_profile` workflow helps convert raw user data into this structured format.

### Feedback and Evaluation System
Includes a comprehensive feedback and evaluation system:

1. The `feedback.py` script evaluates the personalization quality by analyzing:
   - The original educational content
   - The personalized content
   - The content analysis
   - The user profile being used
2. Evaluation metrics include:
   - Personalization effectiveness
   - Content enhancement quality
   - User profile alignment
   - Educational value preservation
3. To run the feedback system:
   ```
   python3 main_workflow/feedback.py
   ```
   The script automatically identifies and processes all the necessary files

## Adding New Content and Profiles

### Adding New Educational Content
1. Place your educational content file (txt/pdf) in the `main_workflow/dirr/` directory
2. Run the main script to process this content

### Adding New User Profiles
1. Prepare raw user data in a format similar to `user_data_example.txt`
2. Run the user data conversion script to generate a structured profile
3. Save the generated profile in the `profiles_user/` directory with a unique name
