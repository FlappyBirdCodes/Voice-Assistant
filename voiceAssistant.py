from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import time
import os
import webbrowser
import urllib.request
import re

# Creates and plays audio file of a message
def text_to_speech(message):
    speech = gTTS(text=message)
    speech.save("speech.mp3")
    playsound("speech.mp3")
    os.remove("speech.mp3")

# Gets audio from the microphone
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        print("Loading...")
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception:
            print("No sound was detected")
            return False
    
    return said

print("Say help if you require access to the specific voice controls")
print("")
text_to_speech("Virtual assistant activated")
while True:
    print("Virtual assistant listening...")
    
    # Listens to sound continously for 3 times
    message = get_audio()
    while message == False:
        message = get_audio()

    # Breaks program if instructed to or if no sound is detected
    if message == "deactivate":
        print("")
        print("Virtual Assistant Deactivated")
        text_to_speech("Virtual Assistant Deactivated")
        break

    message = message.lower()
    keyword = message.split(" ")

    # Tells user specific voice controls 
    if message == "help":
        print("Say: 'what is the time' to get the current time")
        print("Say: 'search <keyword>' to search that keyword on Google")
        print("Say: 'play <song>' to play that particular song on YouTube")
        print("Say: 'open <website>' to open that particular website (only supports Google, YouTube, Amazon and Gmail)")
        message = "Here's a list of all voice controls and it's usage"

    # Tells user the current time
    elif message == "what time is it":
        current_time = time.strftime("%I:%M%p")
        os.environ["TZ"] = "Eastern/USA"
        message = "The time is currently " + str(current_time)

    # Searches google with keyword
    elif keyword[0] == "search":
        message = message.replace(keyword[0], "")[1:]
        if len(message) > 0:
            url = "https://www.google.com.tr/search?q={}".format(message)
            webbrowser.open(url)
            message = "Searched" + message + " in new browser"
        else:
            message = "You must indicate a search keyword for command 'search'"

    # Plays song from YouTube
    elif keyword[0] == "play":
        message = message.replace(keyword[0], "")[1:]
        encoded_message = message.replace(" ", "+")

        # Checks that a search was indicated
        if len(encoded_message) > 0:
            video = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + encoded_message)
            video_ids = re.findall(r"watch\?v=(\S{11})", video.read().decode())
            
            # Opens video url in new browser
            video_url = "https://www.youtube.com/watch?v=" + video_ids[0]
            webbrowser.open(video_url)
            message = "Playing " + message
        else:
            message = "You must indicate a search keyword for command 'play'"

    elif keyword[0] == "open":
        message = message.replace(keyword[0], "")[1:]

        supported_websites = ["google", "youtube", "amazon", "gmail", "discord"]

        # Checks that a website was indicated
        if len(message) > 0:

            # Checks that the website is supported by this program
            if message in supported_websites:        
                if message == "google":
                    webbrowser.open("https://www.google.com/")
                elif message == "youtube":
                    webbrowser.open("https://www.youtube.com/")
                elif message == "amazon":
                    webbrowser.open("https://www.amazon.com/")
                elif message == "gmail":
                    webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
                elif message == "discord":
                    webbrowser.open("https://discord.com/channels/@me")
                message = "Opened " + message + " in new browser"
            else:
                message = "Cannot open unsupported website"

        else:
            message = "You must indicate a search keyword for command 'open'"

    else:
        message = "Sorry, the command you have inputed does not exist"

    print(message)
    text_to_speech(message)
    print("Resetting virtual assistant...")
    print("")
    time.sleep(2)