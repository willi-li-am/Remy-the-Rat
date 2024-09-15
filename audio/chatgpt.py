from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=api_key)

def remy_gpt(text):
    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal:remy:A7TF2xZK",
        messages=[
            {"role": "system", "content": "You are Remy the rat from Ratatouille. Guide users through this recipe: Smash 1 cucumber and cut into bite-sized pieces. Mix 1 teaspoon salt, 2 teaspoons sugar, 1 teaspoon sesame oil, 2 teaspoons soy sauce, and 1 tablespoon rice vinegar to make dressing. Toss cucumber with dressing, 3 chopped garlic cloves, and 1 teaspoon chili oil. Garnish with 1 tsp sesame seeds and cilantro. with step by step with concise responses."},
            {"role": "user", "content": text}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    # Define the subfolder name
    subfolder = "generated_files"

    # Create the full path to the subfolder
    subfolder_path = Path(__file__).parent / subfolder

    # Create the subfolder if it doesn't exist
    subfolder_path.mkdir(parents=True, exist_ok=True)

    # Define file paths within the subfolder
    transcription_file_path = subfolder_path / "transcription.txt"
    remy_gpt_output_file_path = subfolder_path / "remy_gpt_output.txt"

    # Load the transcribed text from the file
    with open(transcription_file_path, "r") as file:
        transcribed_text = file.read()

    # Generate the remy_gpt_output
    remy_gpt_output = remy_gpt(transcribed_text)

    # Print the remy_gpt_output
    print(remy_gpt_output)
    
    # Save the remy_gpt_output to a file in the subfolder
    with open(remy_gpt_output_file_path, "w") as file:
        file.write(remy_gpt_output)

    print(f"remy_gpt_output saved to {remy_gpt_output_file_path}")