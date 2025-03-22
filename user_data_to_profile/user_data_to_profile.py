import os
import glob
import json
import datetime
import random
import re
from google import genai
from google.genai import types

def generate_content():
    # Load environment variables from .env file

    # Initialize the Gemini client
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    # Ensure the script is running from the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Read content from analysis.txt
    try:
        with open("user_data_example.txt", "r", encoding="utf-8") as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading user_data_example.txt: {e}")
        data = ""

    try:
        with open("profile_structure.txt", "r", encoding="utf-8") as f:
            structure = f.read()
    except Exception as e:
        print(f"Error reading profile_structure.txt: {e}")
        structure = ""        
    try:
        with open("user_profile_example.txt", "r", encoding="utf-8") as f:
            prof = f.read()
    except Exception as e:
        print(f"Error reading user_profile_example.txt: {e}")
        prof = ""

    # Prepare content for the model
    parts = []

    # Add text content first
    prompt_text = f"""
You have to create a structured user profile based on the user data provided. The user profile should be structured like this:
{structure}
An example of conversion of user data to user profile is given below:
User Data: 
Name: Alex Chen
Age: 16
Grade: 11th

Academic Information:
- GPA: 3.7/4.0
- Strongest subjects: Biology, English Literature
- Challenging subjects: Physics, Calculus
- Learning style assessment: Visual learner, benefits from graphical representations, prefers independent study before group discussions

Interests and Hobbies:
- Video games (especially Minecraft, The Legend of Zelda, and strategy games)
- Astronomy (follows NASA updates, has a telescope, watches space documentaries)
- Plays guitar (3 years, likes alternative rock and folk music)
- Participates in school's robotics club
- Enjoys anime (favorite series: Fullmetal Alchemist, My Hero Academia)
- Basketball (plays casually with friends)

Media Preferences:
- Favorite books: Science fiction, fantasy (currently reading Brandon Sanderson's novels)
- Favorite movies: Marvel Cinematic Universe, Studio Ghibli films
- Favorite TV shows: Stranger Things, The Expanse
- YouTube subscriptions: Vsauce, Veritasium, Guitar tutorial channels

Personal Traits:
- Introvert who opens up when discussing topics of interest
- Detail-oriented, notices patterns
- Prefers to understand the "why" behind concepts
- Gets easily bored with repetitive tasks
- Responds well to challenges and achievement-based motivation

Corresponding User Profile:
{prof}
Now , similarly, create the user profile of the user data provided below, and just give the user profile in the output, and nothing else.:
{data}


"""
    parts.append(types.Part.from_text(text=prompt_text))



    # Create content for the model
    contents = [
        types.Content(
            role="user",
            parts=parts,
        ),
    ]

    # Set configuration with temperature 1.8
    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,  
        top_p=0.95,
        top_k=64,
        max_output_tokens=65536,
        response_mime_type="text/plain",
    )

    # Model selection - using gemini-flash-2.0 as requested
    model = "gemini-2.0-pro-exp-02-05"

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

    # Save the generated content to a JSON file in the profile_user folder
    try:
        # Create the profile_user folder if it doesn't exist
        profile_folder = "../main_workflow/profiles_user"
        if not os.path.exists(profile_folder):
            os.makedirs(profile_folder)

        # Create a unique filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        filename = f"n.json"
        filepath = os.path.join(profile_folder, filename)

        # Check if the file already exists (very unlikely but just in case)
        while os.path.exists(filepath):
            filename = f"n.json"
            filepath = os.path.join(profile_folder, filename)

        # Extract JSON content from response_text (handling possible markdown code blocks)
        json_content = response_text
        # Check if response is wrapped in code blocks and extract the JSON part
        json_pattern = r'```(?:json)?\s*(\{[\s\S]*?\})\s*```'
        match = re.search(json_pattern, response_text)
        if match:
            json_content = match.group(1)

        # Parse the extracted JSON string into a Python object
        profile_data = json.loads(json_content)

        # Save to JSON file (direct JSON object, not nested in "profile" key)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(profile_data, f, ensure_ascii=False, indent=2)

        print(f"\n\nResponse saved to {filepath}")
    except Exception as e:
        print(f"Error saving JSON: {e}")
        # Fallback: save the raw response for debugging
        with open(os.path.join(profile_folder, f"raw_response_{timestamp}.txt"), "w", encoding="utf-8") as f:
            f.write(response_text)
        print(f"Raw response saved for debugging")

if __name__ == "__main__":
    generate_content()
