import speech_recognition as sr
import pyttsx3
import time
from tkinter import *
from tkinter import ttk
from pyautogui import size as sz
from PIL import Image, ImageTk
from pyglet import *
from logo import my_logo


class NaturalLanguage:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.duration = 0.5

    # Text to speech function
    def tts(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    # Speech to text function
    def stt(self, recognizer, microphone):
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=self.duration)
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
            response["error"] = "Unable to recognize speech"

        return response


class TestYourEnglish(NaturalLanguage):
    def __init__(self, nlu):
        self.root = Tk()
        self.page_num = 0
        self.sentences = ["Hey Misty", "Go Towards the Lion", "Go Around the Wolf"]

        # Initialize class and create list of voices from local device
        NaturalLanguage.__init__(self)
        self.nlu = nlu
        self.e = nlu.engine
        voices = self.e.getProperty('voices')
        voice_list = []
        max_length = 0
        for v in voices:
            voice_list.append(v.id)
            if len(v.id) > max_length:
                max_length = len(v.id)
        voice_tuple = tuple(voice_list)
        self.voice_choice = StringVar(self.root)

        # Initial GUI setup
        self.W, self.H = sz()
        self.root.title("Voice Synchronization for Misty")
        self.root.tk.call("wm", "iconphoto", self.root._w, PhotoImage(data=my_logo))
        self.root.geometry("{}x{}+{}+{}".format(
            round(self.W * 0.8), round(self.H * 0.8), round(self.W * 0.1), round(self.H * 0.1)))
        self.root.resizable(False, False)

        # Create frame and canvas
        self.frame = ttk.Frame(self.root)
        self.main_cv = Canvas(self.frame)
        self.sub_cv1 = Canvas(self.frame)
        self.sub_cv2 = Canvas(self.frame)
        self.sub_cv3 = Canvas(self.frame)
        self.last_cv = Canvas(self.frame)
        self.frame.pack(fill=BOTH, expand=YES)
        self.main_cv.pack(fill=BOTH, expand=YES)

        # Create widgets
        ttk.Combobox(self.main_cv, textvariable=self.voice_choice, width=max_length+2, font=("Arial", 10),
                     value=voice_tuple).place(x=round(self.H * 0.015), y=round(self.H * 0.015))
        Button(self.main_cv, text="Start!", command=self.button_func, bg="#77DD77", activebackground="#72DC72",
               font=("Brick", 50)).place(relx=0.5, rely=0.55, relwidth=0.2, relheight=0.2, anchor=CENTER)
        Button(self.sub_cv1, text=">>", command=self.button_func,
               bg="#D0E1F5", activebackground="#C9DCF3", font=("Helvetica", 16, "bold")).place(
            x=round(self.W * 0.8 - self.H * 0.015), y=round(self.H * 0.785), relwidth=0.06, relheight=0.04, anchor=SE)
        Button(self.sub_cv2, text=">>", command=self.button_func,
               bg="#D0E1F5", activebackground="#C9DCF3", font=("Helvetica", 16, "bold")).place(
            x=round(self.W * 0.8 - self.H * 0.015), y=round(self.H * 0.785), relwidth=0.06, relheight=0.04, anchor=SE)
        Button(self.sub_cv3, text=">>", command=self.button_func,
               bg="#D0E1F5", activebackground="#C9DCF3", font=("Helvetica", 16, "bold")).place(
            x=round(self.W * 0.8 - self.H * 0.015), y=round(self.H * 0.785), relwidth=0.06, relheight=0.04, anchor=SE)

        # Create Images
        self.intro = Image.open("src\images\intro.png").resize((round(self.W * 0.8), round(self.H * 0.8)))
        self.misty = Image.open("src\images\misty.jpg").resize((round(self.W * 0.8), round(self.H * 0.8)))
        self.lion = Image.open("src\images\lion.png").resize((round(self.W * 0.8), round(self.H * 0.8)))
        self.wolf = Image.open("src\images\wolf.jpg").resize((round(self.W * 0.8), round(self.H * 0.8)))
        self.last = Image.open("src\images\last.jpg").resize((round(self.W * 0.8), round(self.H * 0.8)))
        self.intro = ImageTk.PhotoImage(self.intro)
        self.misty = ImageTk.PhotoImage(self.misty)
        self.lion = ImageTk.PhotoImage(self.lion)
        self.wolf = ImageTk.PhotoImage(self.wolf)
        self.last = ImageTk.PhotoImage(self.last)
        self.mic = Image.open("src\images\mic.png")
        self.mic.thumbnail((self.H * 0.04, self.H * 0.04))
        self.mic = ImageTk.PhotoImage(self.mic)
        self.main_cv.create_image(0, 0, anchor=NW, image=self.intro)

    def button_func(self):
        if self.voice_choice.get() == "":
            return
        self.e.setProperty('voice', self.voice_choice.get())
        self.page_num += 1
        pages = [self.main_cv, self.sub_cv1, self.sub_cv2, self.sub_cv3, self.last_cv]
        images = [self.misty, self.lion, self.wolf, self.last]
        attempts = 10

        pages[self.page_num - 1].destroy()
        pages[self.page_num].pack(fill=BOTH, expand=YES)
        pages[self.page_num].create_image(0, 0, anchor=NW, image=images[self.page_num - 1])
        self.root.update()

        if self.page_num < 4:
            pages[self.page_num].create_text(
                round(self.H * 0.015), round(self.H * 0.015),
                text="Please Repeat the Sentence:\n" + self.sentences[self.page_num - 1],
                fill="black", font=("tvN 즐거운이야기 Bold", 40), anchor=NW)
            pages[self.page_num].create_image(
                pages[self.page_num].winfo_width() * 0.96, round(self.H * 0.015), anchor=NE, image=self.mic)
            on_off_text = pages[self.page_num].create_text(
                pages[self.page_num].winfo_width() * 0.96 - self.mic.width() * 0.5,
                round(self.H * 0.015) + self.mic.height() * 1.5, text="OFF", fill="black", font="Helvetica 20 bold",
                justify=CENTER, anchor=CENTER)
            attempts_text = pages[self.page_num].create_text(
                round(self.H * 0.015), round(pages[self.page_num].winfo_height() - self.H * 0.015),
                text="Attempts: " + str(attempts), fill="black", font="Helvetica 20 bold", justify=CENTER, anchor=SW)
            self.root.update()
            pages[self.page_num].update()
            time.sleep(2)
            self.nlu.tts("please repeat after me")
            time.sleep(1)
            self.nlu.tts(self.sentences[self.page_num - 1])
        else:
            pages[self.page_num].create_text(
                round(self.W * 0.4), round(self.H * 0.07), text="Congratulation!",
                fill="black", font=("tvN 즐거운이야기 Bold", 80), justify=CENTER, anchor=CENTER)
            self.root.update()

        while self.page_num < 4:
            r = sr.Recognizer()
            m = sr.Microphone()

            print("listening...")
            pages[self.page_num].itemconfig(on_off_text, text="ON", fill="red")
            pages[self.page_num].update()

            text = self.nlu.stt(r, m)
            if not text["success"]:
                print("ERROR: {}".format(text["error"]))
                pages[self.page_num].itemconfig(on_off_text, text="OFF", fill="black")
                pages[self.page_num].update()
                self.nlu.tts("an error has occurred")
                self.nlu.tts("please try again.")
                continue

            try:
                you_said = text["transcription"].lower()
            except AttributeError:
                print("Try Again")
                pages[self.page_num].itemconfig(on_off_text, text="OFF", fill="black")
                pages[self.page_num].update()
                self.nlu.tts("sorry, I couldn't hear you")
                self.nlu.tts("please try again")
                continue

            if you_said.split()[-1] == self.sentences[self.page_num - 1].lower().split()[-1]:
                print("Correct. You said: {}".format(you_said))
                pages[self.page_num].itemconfig(on_off_text, text="OFF", fill="black")
                pages[self.page_num].create_text(
                    round(self.W * 0.4), round(self.H * 0.07), text="Good Job!", fill="black",
                    font=("tvN 즐거운이야기 Bold", 80), justify=CENTER, anchor=CENTER)
                pages[self.page_num].update()
                self.nlu.tts("good job")
                if self.page_num < 3:
                    self.nlu.tts("please move on to the next question")
                else:
                    self.nlu.tts("please move on to the next page")
                return
            else:
                print("Wrong. You said: {}".format(you_said))
                attempts -= 1
                if attempts == 0:
                    pages[self.page_num].itemconfig(attempts_text, text="Attempts: " + str(attempts))
                    pages[self.page_num].update()
                    self.nlu.tts("you have exceeded the maximum attempts")
                    self.nlu.tts("please move on to the next question")
                    return
                else:
                    pages[self.page_num].itemconfig(on_off_text, text="OFF", fill="black")
                    pages[self.page_num].itemconfig(attempts_text, text="Attempts: " + str(attempts))
                    pages[self.page_num].update()
                    self.nlu.tts("please try again")


if __name__ == "__main__":
    natural_language = NaturalLanguage()
    font.add_directory(r"src\fonts")
    my_font1 = font.load("tvN 즐거운이야기")
    my_font2 = font.load("Brick")
    app = TestYourEnglish(natural_language)
    app.root.mainloop()
