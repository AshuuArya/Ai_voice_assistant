import openai
import pyttsx3
import speech_recognition as sr
import os

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return ""

def generate_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-002",  # Note: This model is deprecated; consider updating to a newer model
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    if not openai.api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return
    
    while True:
        print("Say 'Hi' to start recording your questions...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "hi":  # Case-insensitive match
                    filename = "input.wav"
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 0.5
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")
                        response = generate_response(text)
                        print(f"Assistant says: {response}")
                        speak_text(response)
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()