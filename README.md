# QUZZIZ: Educational Content Personalization System

## Project Overview
QUZZIZ is an AI-powered educational content personalization system that transforms standard educational materials into personalized learning experiences tailored to individual learner profiles. The system operates in two main stages:

1. **Content Analysis Stage**: Analyzes educational content using scientific methodologies to assess quality, identify drawbacks, and highlight areas for improvement.
2. **Personalization Stage**: Combines the content analysis with user profiles to create personalized educational materials that address the specific needs, interests, and learning preferences of individual readers.

## Directory Structure
```
QUZZIZ/
├── main_workflow/
│   ├── dirr/                   # Directory for source educational content (accepts .txt and .pdf)
│   │   └── Photosynthesis.txt  # Example educational content
│   ├── llm_output.txt          # Output from Stage 1 (content analysis)
│   ├── main.py                 # Main script that orchestrates the two-stage process
│   ├── output.txt              # Final personalized content from Stage 2
│   ├── profiles_user/          # User profile storage directory
│   │   ├── f.json              # Individual user profiles in JSON format
│   │   ├── g.json              # Each profile contains learning preferences, interests, etc.
│   │   └── ...                 # Additional user profiles
│   └── requirements.txt        # Required Python dependencies
├── user_data_to_profile/
│   ├── profile_structure.txt   # Template for user profile structure
│   ├── user_data_example.txt   # Example of raw user data
│   ├── user_data_to_profile.py # Script to convert raw user data to structured profiles
│   └── user_profile_example.txt # Example of processed user profile
└── venv/                       # Python virtual environment
```

## Important Notes
- **The `dirr` directory must contain only a single file at a time.** Having multiple files in this directory may cause unexpected behavior.
- Make sure your source content file is properly formatted as .txt or .pdf.

## How QUZZIZ Works

### Stage 1: Content Analysis
In this stage, QUZZIZ analyzes the educational content provided in the `dirr` directory using an LLM (Large Language Model) prompt:

1. The system reads the content file (txt or pdf) from the `dirr` directory
2. It applies a comprehensive analysis based on educational science methodologies:
   - Content accuracy and currency assessment
   - Conceptual clarity evaluation
   - Structural logic analysis
   - Visual/multimedia effectiveness review
   - Engagement and relevance measurement
   - Cognitive challenge assessment (using Bloom's Taxonomy)
   - Critical thinking and problem-solving evaluation
   - Interdisciplinary connection identification
   - Scaffolding and support analysis
   - And several other educational quality metrics
3. The analysis results are stored in `llm_output.txt`, providing detailed insights into:
   - Strengths and weaknesses of the content
   - Areas requiring improvement
   - Cognitive demand profile
   - Transfer potential index
   - Differentiation depth analysis
   - Enhancement prioritization matrix

### Stage 2: Content Personalization
In this stage, QUZZIZ takes the content analysis and combines it with user profile data:

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
QUZZIZ uses a structured user profile system to store information about learners:

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

## Setup and Usage

### Setup
1. Create a virtual environment:
   ```
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
3. Install the dependencies:
   ```
   pip install -r main_workflow/requirements.txt
   ```
4. Set up your API key (required for the LLM):
   - Create a `.env` file in the project root
   - Add your Gemini API key: `GEMINI_API_KEY=your_api_key_here`

### Usage

#### Running the Full Personalization Pipeline
To process educational content and generate personalized output:
```
python main_workflow/main.py [profile_name]
```
Where `profile_name` is the name of the JSON file in the `profiles_user/` directory (without the .json extension).

For example:
```
python main_workflow/main.py f    # Uses profiles_user/f.json
python main_workflow/main.py j    # Uses profiles_user/j.json
```

If no profile name is specified, the system will default to using `f.json`.

This will:
1. Analyze the educational content files in `dirr/`
2. Generate the content analysis in `llm_output.txt`
3. Combine this analysis with the specified user profile from `profiles_user/`
4. Create the personalized content in `output.txt`

#### Selecting a User Profile
The system now allows you to easily switch between different user profiles:

1. Use the command-line argument to specify which profile to use (e.g., `python main_workflow/main.py j`)
2. This eliminates the need to manually edit the script when switching between profiles
3. You can still modify `main.py` directly if you prefer to hardcode a specific profile

#### Creating New User Profiles
To convert raw user data into a structured profile:
```
python user_data_to_profile/user_data_to_profile.py
```
This will:
1. Read raw user data from `user_data_example.txt`
2. Convert it to a structured profile based on `profile_structure.txt`
3. Generate a user profile in `profile_generated.txt`

## Adding New Content and Profiles

### Adding New Educational Content
1. Place your educational content file (txt or pdf) in the `main_workflow/dirr/` directory
2. Run the main script to process this content

### Adding New User Profiles
1. Prepare raw user data in a format similar to `user_data_example.txt`
2. Run the user data conversion script to generate a structured profile
3. Save the generated profile in the `profiles_user/` directory with a unique name