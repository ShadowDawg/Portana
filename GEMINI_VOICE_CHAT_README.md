# Gemini Voice Chat

A Python application that allows you to have voice conversations with Google's Gemini AI. This application uses speech recognition to convert your voice to text, sends the text to the Gemini API, and then uses text-to-speech to speak the AI's response.

## Features

- Voice input through your microphone
- Text-to-speech output of Gemini's responses
- Continuous conversation mode
- Simple command-line interface

## Requirements

- Python 3.7+
- Google Gemini API key
- Microphone and speakers

## Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
   - Option 1: Set it as an environment variable:
     ```bash
     export GEMINI_API_KEY="your_api_key_here"
     ```
   - Option 2: Edit the `gemini_voice_chat.py` file and add your API key directly

## Usage

1. Run the application:

```bash
python gemini_voice_chat.py
```

2. Speak into your microphone when prompted
3. Listen to Gemini's response
4. Continue the conversation or say "exit", "quit", or "goodbye" to end the session

## Troubleshooting
