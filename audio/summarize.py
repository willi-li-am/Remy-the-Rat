from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=api_key)

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
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
    summary_file_path = subfolder_path / "summary.txt"

    # Load the transcribed text from the file
    with open(transcription_file_path, "r") as file:
        transcribed_text = file.read()

    # Generate the summary
    summary = summarize_text(transcribed_text)

    # Print the summary
    print("Summary:", summary)
    
    # Save the summary to a file in the subfolder
    with open(summary_file_path, "w") as file:
        file.write(summary)

    print(f"Summary saved to {summary_file_path}")