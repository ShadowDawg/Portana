"""
Gemini Voice Chat Application

This application allows you to have a voice conversation with Google's Gemini AI.
It uses the Gemini API for text generation and integrates with speech recognition
and text-to-speech capabilities.

Requirements:
- google-generativeai
- SpeechRecognition
- pyttsx3
- pyaudio
"""

import os
import time
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

# Configure your API key
# You need to set your Gemini API key as an environment variable or directly here
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")  # Replace with your API key if not using env variable

# Initialize the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def setup_gemini_model():
    """Set up and return the Gemini model for chat."""
    # Configure the model
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1024,
    }
    
    # Create the model
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config
    )
    
    # Start a chat session
    chat = model.start_chat(history=[])
    return chat

def listen_to_speech():
    """Listen to user's speech and convert it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10)
            print("Processing speech...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def speak_response(text):
    """Convert text to speech and play it."""
    print(f"Gemini: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

def main():
    """Main function to run the voice chat application."""
    print("Welcome to Gemini Voice Chat!")
    
    if not GEMINI_API_KEY:
        print("Error: Gemini API key not found. Please set your API key.")
        return
    
    print("Initializing Gemini model...")
    chat = setup_gemini_model()
    
    print("Ready to chat! Speak to start a conversation. Say 'exit' or 'quit' to end the session.")
    speak_response("Hello! I'm Gemini. How can I help you today?")
    
    while True:
        user_input = listen_to_speech()
        if not user_input:
            continue
        
        if user_input.lower() in ["exit", "quit", "goodbye"]:
            speak_response("Goodbye! Have a great day.")
            break
        
        response = chat.send_message(user_input).text
        speak_response(response)

if __name__ == "__main__":
