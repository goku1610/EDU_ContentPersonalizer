content_analysis_prompt = ""

with open("Photosynthesis.txt", "r") as f:
    original_content = f.read()

# Add functionality to randomly read a JSON profile and extract specific information
import json
import os
import random

def get_random_profile():
    # Get all JSON files from profiles_user directory
    profile_dir = "profiles_user"
    json_files = [f for f in os.listdir(profile_dir) if f.endswith('.json')]
    
    # Select a random JSON file
    random_file = random.choice(json_files)
    file_path = os.path.join(profile_dir, random_file)
    
    # Read and parse the JSON file
    with open(file_path, 'r') as file:
        profile_data = json.load(file)
    
    # Extract required information
    age = profile_data.get('age', '')
    class_level = profile_data.get('class', '')
    
    # Determine target audience based on age and class
    target_audience = f"{age} years old, {class_level} students with developing abstract thinking and interest-based learning"
    
    # Extract learning style preferences
    learning_style = profile_data.get('learning_style_preferences', {})
    primary_modality = learning_style.get('primary_mode', '')
    secondary_modality = learning_style.get('secondary_mode', '')
    
    # Extract core competencies from personalization vectors
    core_competencies = profile_data.get('personalization_vectors', {}).get('high_impact_approaches', [])
    
    # Determine subject area from primary interests
    primary_interests = profile_data.get('primary_interests', [])
    subject_area = primary_interests[0]['interest'] if primary_interests else "General Education"
    
    # Format the output
    profile_output = {
        "target_audience": target_audience,
        "learning_modality": {
            "primary": primary_modality,
            "secondary": secondary_modality
        },
        "core_competencies": core_competencies[:5],  # Limit to 5 competencies
        "subject_area": subject_area
    }
    
    return profile_output, random_file

# Get a random profile and print the output
random_profile, selected_file = get_random_profile()
print(f"Randomly selected profile: {selected_file}")
print(json.dumps(random_profile, indent=2))

