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
        with open("user_data_example.txt", "r", encoding="utf-8") as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading user_data.txt: {e}")
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
        print(f"Error reading user_profile.txt: {e}")
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
    
    # Save the generated content to output.txt
    try:
        with open("profile_generated.txt", "w", encoding="utf-8") as f:
            f.write(response_text)
        print("\n\nResponse saved to profile_generated.txt")
    except Exception as e:
        print(f"Error saving txt {e}")

if __name__ == "__main__":
    generate_content()