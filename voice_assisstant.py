import speech_recognition as sr
import pyttsx3
import openai
import os

# Set your OpenAI API key
openai.api_key = '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'

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to speech
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Function to check if the text contains the wake word
def wakeWord(text):
    WAKE_WORDS = ['assistant', 'hey anisha', 'anisha', 'okay anisha', 'hi anisha', 'hello anisha']
    text = text.lower()
    return any(word in text for word in WAKE_WORDS)

# Function to perform actions based on user commands
def performAction(command):
    if "open" in command:
        words = command.split()
        index = words.index("open")
        program = words[index + 1]
        SpeakText(f"Opening{program}")
        os.system(f'start {program}')
    elif "ask a question" in command:
        SpeakText("Sure, what would you like to ask?")
        audio_data = r.listen(source, timeout=10)  # Listen for the user's question
        question = r.recognize_google(audio_data, language='en-US')
        response = chatgpt_query(question)
        SpeakText(response)
    elif "bye" in command:
        SpeakText("Bye, See you soon")
        exit()
    elif "goodbye" in command:
        SpeakText("Goodbye, See you soon")
        exit()
    elif "good night" in command:
        SpeakText("Good Night, Sweet Dreams")
        exit()
    else:
        SpeakText("Sorry, I did not understand that.")

# Function to query ChatGPT
def chatgpt_query(question):
    try:
        # Send the user's question to ChatGPT
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            temperature=0.7,
            max_tokens=150,
            n=1,
        )

        return response["choices"][0]["text"].strip()

    except Exception as e:
        print(f"Error querying ChatGPT: {e}")
        return "I'm sorry, I couldn't generate a response at the moment."

# Continuous listening loop
while True:
    print("Say something")

    with sr.Microphone(device_index=1) as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio_data = r.listen(source)
        print("Recognizing...")

        try:
            MyText = r.recognize_google(audio_data, language='en-US')
            print(MyText)

            if "bye" or "goodbye" or "goodnight" in command:
                SpeakText("Bye, have a good day")
                exit()


            elif wakeWord(MyText):
                SpeakText("Hello, How can I assist you?")

                # Listen for the user's command after the wake word
                audio_data = r.listen(source, timeout=5)
                command = r.recognize_google(audio_data, language='en-US')

                # Perform actions based on the user's command
                performAction(command)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")
        except Exception as e:
            print(f"An error occurred; {e}")
