import os
from elevenlabs import ElevenLabs, play

# Initialize ElevenLabs client with your API key
api_key = "sk_e9be6c79895a6b1bb6505caabc328f01ec24c7b90aa08e75"
client = ElevenLabs(api_key=api_key)

# Function to list available voices
def list_voices():
    response = client.voices.get_all()
    voices = response.voices
    print("Available voices:")
    for idx, voice in enumerate(voices):
        print(f"{idx + 1}. {voice['name']}")
    return voices

# Function to get the user's choice of voice
def get_voice_choice(voices):
    choice = int(input("Enter the number of the voice you want to use: ")) - 1
    return voices[choice]['voice_id']

# List available voices and get user's choice
voices = list_voices()
voice_id = get_voice_choice(voices)

# Read input.txt file
with open('input.txt', 'r') as file:
    lines = file.readlines()

# Process each line in input.txt
for line in lines:
    # Split the line into filename and text
    if '=' in line:
        filename, text = line.split('=', 1)
        filename = filename.strip()
        text = text.strip()
        
        # Generate audio using ElevenLabs API with the selected voice
        audio = client.generate(
            text=text,
            voice=voice_id
        )
        
        # Save the audio file
        audio_path = f"{filename}.mp3"
        with open(audio_path, 'wb') as audio_file:
            audio_file.write(audio)

        print(f"Generated audio for '{text}' and saved to '{audio_path}'")
