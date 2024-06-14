from mistyPy.Robot import Robot
from mistyPy.Events import Events
from mistyPy.EventFilters import EventFilters
import speech_recognition as sr
import time

ip_address = "10.245.146.204"
misty = Robot(ip_address)


# Speech to text function
def stt(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["success"] = False
        response["error"] = "Unable to recognize speech"

    return response


# Function to process speech for Misty to understand
def misty_listens():
    while True:
        r = sr.Recognizer()
        m = sr.Microphone()

        print("listening...")

        text = stt(r, m)
        if not text["success"]:
            print("ERROR: {}".format(text["error"]))
            misty.Speak("Sorry, please say that again.")
            return ""

        try:
            you_said = text["transcription"].lower()
        except AttributeError:
            print("Try Again")
            misty.Speak("Sorry, I could not hear you.")
            return ""

        print("You said: {}".format(you_said))

        return you_said


# Move Misty towards an object
def misty_moves_towards(command_name):
    misty.ChangeLED(0, 255, 0)
    misty.Speak("Okay.")
    misty.Drive(10.0, 0.0)
    misty.RegisterEvent(command_name, Events.TimeOfFlight,
                        condition=[EventFilters.TimeOfFlightPosition.FrontCenter,
                                   EventFilters.TimeOfFlightDistance.MaxDistance(0.15)],
                        keep_alive=False, callback_function=misty_stops, debounce=1)


# Turn Misty left or right
def misty_turns():
    misty.ChangeLED(0, 255, 0)
    misty.Speak("Okay.")
    global state
    if state == 1 or state == 7:
        misty.DriveArc(270.0, 0.0, 1000.0, False)
    elif state == 5:
        misty.DriveArc(180.0, 0.0, 1000.0, False)
    misty.ChangeLED(0, 0, 0)


# Move Misty around an object
def misty_goes_around():
    misty.ChangeLED(0, 255, 0)
    misty.Speak("Okay.")
    misty.DriveArc(0.0, 0.0, 2000.0, False)
    time.sleep(5)
    misty.DriveTime(5.0, 0.0, 3000)
    time.sleep(5)
    misty.DriveArc(270.0, 0.0, 2000.0, False)
    time.sleep(5)
    misty.DriveTime(5.0, 0.0, 3000)
    time.sleep(5)
    misty.ChangeLED(0, 0, 0)


# Stop Misty
def misty_stops(event):
    misty.Stop()
    misty.ChangeLED(0, 0, 0)


# Function to control Misty when she hears the key phrase
def misty_follows_command(event):
    misty.StopKeyPhraseRecognition()
    misty.ChangeLED(255, 255, 0)
    misty.Speak("Yes?")
    time.sleep(0.2)

    what_she_heard = misty_listens()
    if what_she_heard == "":
        misty.StartKeyPhraseRecognition()
        return
    sentence = what_she_heard.split()
    key_word = sentence[-1]

    global state
    # incorrect commands
    if (state == 0) and (key_word in ["wolf", "sloth", "squirrel", "end"]):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("Sorry. I cannot see the {}.".format(key_word))
    elif (state == 1) and (key_word in ["wolf", "sloth", "squirrel", "end"]):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("Sorry. I cannot see the {}.".format(key_word))
    elif (state == 1) and (key_word == "lion"):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("I am already at the {}.".format(key_word))
    elif (state == 2) and (key_word in ["lion", "sloth", "squirrel", "end"]):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("Sorry. I cannot see the {}.".format(key_word))
    elif (state == 3) and (key_word in ["lion", "sloth", "squirrel", "end"]):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("Sorry. I cannot see the {}.".format(key_word))
    elif (state == 3) and (key_word == "wolf") and ("towards" in sentence):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("I am already at the {}.".format(key_word))
    elif (state == 4) and (key_word in ["lion", "wolf", "squirrel", "end"]):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("Sorry. I cannot see the {}.".format(key_word))
    elif (state == 5) and (key_word in ["lion", "wolf", "squirrel", "end"]):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("Sorry. I cannot see the {}.".format(key_word))
    elif (state == 5) and (key_word == "sloth"):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("I am already at the {}.".format(key_word))
    elif (state == 6) and (key_word in ["lion", "wolf", "sloth", "end"]):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("Sorry. I cannot see the {}.".format(key_word))
    elif (state == 7) and (key_word in ["lion", "wolf", "sloth", "end"]):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("Sorry. I cannot see the {}.".format(key_word))
    elif (state == 7) and (key_word == "squirrel"):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("I am already at the {}.".format(key_word))
    elif (state == 8) and (key_word in ["lion", "wolf", "sloth", "squirrel"]):
        misty.ChangeLED(0, 0, 0)
        misty.Speak("Sorry. I cannot see the {}.".format(key_word))

    # correct commands
    elif (state == 0) and ("towards" in sentence) and (key_word == "lion"):
        misty_moves_towards("lion")
        state = 1
    elif (state == 1) and ("turn" in sentence) and (key_word == "right"):
        misty_turns()
        state = 2
    elif (state == 2) and ("towards" in sentence) and (key_word == "wolf"):
        misty_moves_towards("wolf")
        state = 3
    elif (state == 3) and ("around" in sentence) and (key_word == "wolf"):
        misty_goes_around()
        state = 4
    elif (state == 4) and ("towards" in sentence) and (key_word == "sloth"):
        misty_moves_towards("sloth")
        state = 5
    elif (state == 5) and ("turn" in sentence) and (key_word == "right"):
        misty_turns()
        state = 6
    elif (state == 6) and ("towards" in sentence) and (key_word == "squirrel"):
        misty_moves_towards("squirrel")
        state = 7
    elif (state == 7) and ("turn" in sentence) and (key_word == "left"):
        misty_turns()
        state = 8
    elif (state == 8) and (key_word == "end"):
        misty_moves_towards("end")
        misty.StopKeyPhraseRecognition()
        state = 9
    else:
        misty.ChangeLED(0, 0, 0)
        misty.Speak("Sorry. I could not understand.")
    misty.StartKeyPhraseRecognition()


if __name__ == "__main__":
    state = 0
    misty.StartKeyPhraseRecognition()
    misty.RegisterEvent("key_phrase", Events.KeyPhraseRecognized,
                        keep_alive=True, callback_function=misty_follows_command, debounce=1)
    misty.KeepAlive()
