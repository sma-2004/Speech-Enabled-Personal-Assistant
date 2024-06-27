import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import wikipedia
import pygame
import psutil
import cv2
import subprocess
import pywhatkit as kit
from requests import get



class Jarvis:
    def _init_(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)


    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()


    def greet(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            print("Good Morning Sir, I am Jarvis. How may I help you?")
            self.speak("Good Morning Sir, I am Jarvis. How may I help you?")

        elif 12 <= hour < 17:
            print("Good Afternoon Sir, I am Jarvis. How may I help you?")
            self.speak("Good Afternoon Sir, I am Jarvis. How may I help you?")

        else:
            print("Good Evening Sir, I am Jarvis. How may I help you?")
            self.speak("Good Evening Sir, I am Jarvis. How may I help you?")



class VoiceRecognition_and_SpeechToText:
    def _init_(self):
        self.recognizer = sr.Recognizer()
        self.jarvis = Jarvis()


    def take_command(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing voice...")
            user_voice = self.recognizer.recognize_google(audio)
            print(f"You said: {user_voice}\n")

        except Exception as e:
            print(e)
            print("Can't recognize, try once again!")
            return "None"

        return user_voice.lower()



class Tasks:
    def _init_(self):
        self.jarvis = Jarvis()
        self.voice_recognition = VoiceRecognition_and_SpeechToText()


    def search_wikipedia(self, user_voice):
        print("Searching for Wikipedia")
        search_query = user_voice[user_voice.find(' ') + 1:]
        results = wikipedia.summary(search_query, sentences=2)
        print(results)
        self.jarvis.speak("According to Wikipedia")
        self.jarvis.speak(results)


    def open_youtube(self):
        print("Sir, what should I search on Youtube?")
        self.jarvis.speak("Sir, what should I search on Youtube?")
        self.search = self.voice_recognition.take_command()
        kit.playonyt(self.search)


    def open_google(self):
        print("Sir, what should I search on Google?")
        self.jarvis.speak("Sir, what should I search on Google?")
        self.search = self.voice_recognition.take_command()
        webbrowser.open(self.search)


    class MusicPlayer:
        def _init_(self):
            pygame.init()
            pygame.mixer.init()
            self.playlist = []
            self.current_song = 0
            self.voice_recognition = VoiceRecognition_and_SpeechToText()

        def load_songs_from_folder(self, folder_path):
            songs = os.listdir(folder_path)
            self.playlist = [os.path.join(folder_path, song) for song in songs if song.endswith(".mp3")]

        def play(self):
            pygame.mixer.music.load(self.playlist[self.current_song])
            pygame.mixer.music.play()

        def pause(self):
            pygame.mixer.music.pause()

        def unpause(self):
            pygame.mixer.music.unpause()

        def stop(self):
            pygame.mixer.music.stop()

        def next_song(self):
            self.stop()
            self.current_song = (self.current_song + 1) % len(self.playlist)
            self.play()

        def choose_song(self):
            print("Select a song:")
            for i, song_path in enumerate(self.playlist):
                print(f"{i+1}. {os.path.basename(song_path)}")

            choice = int(input("Enter the number of the song: "))
            if choice > 0 and choice <= len(self.playlist):
                self.stop()
                self.current_song = choice - 1
                self.play()
            else:
                print("Invalid choice.")

        
        def get_user_choice(self):
            print("\n1. Play\n2. Pause\n3. Unpause\n4. Stop\n5. Next Song\n6. Choose Song\n7. Exit")
            choice = input("Enter your choice: ")
            return choice

        def run(self):

            while True:
                user_voice = self.voice_recognition.take_command()

                if "play" in user_voice:
                    self.play()

                elif "pause" in user_voice:
                    self.pause()

                elif "unpause" in user_voice:
                    self.unpause()

                elif "stop" in user_voice:
                    self.stop()

                elif "next song" in user_voice:
                    self.next_song()

                elif "select song" in user_voice:
                    self.choose_song()

                elif "option" in user_voice:
                    self.get_user_choice()

                elif "exit" in user_voice:
                    break

                else:
                    print("Invalid choice. Try again.")


    def stop_movie(self):
            def find_media_pid():
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] == 'Microsoft.Media.Player.exe':
                        return proc.pid
                return None

            media_pid = find_media_pid()

            if media_pid != None:
                os.kill(media_pid, 9)




    def get_current_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.jarvis.speak(f"Sir, the time is {current_time}")


    def open_camera(self):
        self.cam = cv2.VideoCapture(0)
        cv2.namedWindow("Camera")
        img_counter = 0
        while True:
            ret, frame = self.cam.read()
            if not ret:
                print("Failed to grab frame")
                break
            cv2.imshow("Camera", frame)
            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = f"opencv_frame_{img_counter}.png"
                cv2.imwrite(img_name, frame)
                print(f"{img_name} written!")
                img_counter += 1
        self.cam.release()
        cv2.destroyAllWindows()


    def send_whatsapp_message(self):
        self.country_code = 91
        self.jarvis.speak("Whomever you want to send a message, please tell their phone number?")
        self.phone_number = self.voice_recognition.take_command()

        self.jarvis.speak("What message do you want to write?")
        user_voice = self.voice_recognition.take_command()
        self.message = user_voice if user_voice != "None" else ""

        self.full_phone_number = f"+{self.country_code}{self.phone_number}"
        self.h=int(datetime.datetime.now().hour)
        self.m=int(datetime.datetime.now().minute)+1
        kit.sendwhatmsg(self.full_phone_number, self.message, self.h, self.m)


    def ask_user(self):
        self.jarvis.speak("Sir, do you have any other work?")


        
    class MoviePlayer:
        def _init_(self):
            self.movie_folder = "C://movies//Pirates of the Caribbean Dead Man's Chest (2006) 720p - [SyED]"
            self.movie_list = []
            self.voice_recognition = VoiceRecognition_and_SpeechToText()

        def get_movie_list(self):
            self.movie_list = os.listdir(self.movie_folder)

        def play_movie(self, movie_index):
            if movie_index < 1 or movie_index > len(self.movie_list):
                print("Invalid choice.")
                return

            movie_name = self.movie_list[movie_index - 1]
            movie_path = os.path.join(self.movie_folder, movie_name)
            try:
                subprocess.run(["start", "", movie_path], shell=True)
            except Exception as e:
                print(f"Error: {e}")

        def get_user_choice(self):
            print("\nMovie Player")
            print("Select a movie to play:")
            for i, movie_name in enumerate(self.movie_list):
                print(f"{i+1}. {movie_name}")

            print(f"{len(self.movie_list)+1}. Exit")
            self.choice = int(input("Enter the number of the movie to play: "))
            return self.choice

        def run(self):
            self.get_movie_list()
            self.choice = self.get_user_choice()

            while self.choice != len(self.movie_list) + 1:
                self.play_movie(self.choice)
                self.choice = self.get_user_choice()


    def open_stackoverflow(self):
        webbrowser.open("https://stackoverflow.com/")


    def open_instagram(self):
        webbrowser.open("https://www.instagram.com/")


    def open_whatsapp(self):
        webbrowser.open("https://web.whatsapp.com/")


    def open_facebook(self):
        webbrowser.open("https://www.facebook.com/")


    def open_notepad(self):
        self.path = "C:\\Windows\\Notepad"
        os.startfile(self.path)


    def open_command_prompt(self):
        os.system("start cmd")


    def ip_address(self):
        self.ip = get("https://api.ipify.org").text
        print(self.ip)
        self.jarvis.speak(f"Your IP address is {self.ip}")

    
    def help(self):
        print("Function i can perform sir are:-\n")
        self.jarvis.speak("Function i can perform sir are\n")
        print("1) Open Youtube \n2)Open Wikipedia \n3)Open Google and search \n4)Open notepad \n5)open camera\n")
        print("6)Play Music \n7)Play Movies \n8)Open Command Prompt \n9)Send Message \n10)Ask Time\n")
        print("11)Open Facebook \n12)Open Whatsapp \n13)Open Instagram\n 14)Exit\n")


class Execution:
    def _init_(self):
        self.voice_recognition = VoiceRecognition_and_SpeechToText()
        self.tasks = Tasks()
        self.jarvis = Jarvis()
        self.music = self.tasks.MusicPlayer()
        self.movie = self.tasks.MoviePlayer()


    def run(self):
        self.jarvis.greet()

        while True:
            user_voice = self.voice_recognition.take_command()

            if "wikipedia" in user_voice:
                self.tasks.search_wikipedia(user_voice)
                self.tasks.ask_user()

            elif "youtube" in user_voice:
                self.tasks.open_youtube()
                self.tasks.ask_user()

            elif "google" in user_voice:
                self.tasks.open_google()
                self.tasks.ask_user()

            elif "notepad" in user_voice:
                self.tasks.open_notepad()
                self.tasks.ask_user()

            elif "command prompt" in user_voice:
                self.tasks.open_command_prompt()
                self.tasks.ask_user()

            elif "open camera" in user_voice:
                self.tasks.open_camera()
                self.tasks.ask_user()

            elif "play music" in user_voice:
                folder_path = "C:\\Songs"  
                self.music.load_songs_from_folder(folder_path)
                self.music.run()
                self.tasks.ask_user()

            elif "close movie" in user_voice:
                self.tasks.stop_movie()
                self.tasks.ask_user()

            elif "play movie" in user_voice:
                self.movie.run()
                self.tasks.ask_user()

            elif "the time" in user_voice:
                self.tasks.get_current_time()
                self.tasks.ask_user()

            elif "send message" in user_voice:
                self.tasks.send_whatsapp_message()
                self.tasks.ask_user()

            elif "instagram" in user_voice:
                self.tasks.open_instagram()
                self.tasks.ask_user()

            elif "whatsapp" in user_voice:
                self.tasks.open_whatsapp()
                self.tasks.ask_user()

            elif "facebook" in user_voice:
                self.tasks.open_facebook()
                self.tasks.ask_user()

            elif "ip address" in user_voice:
                self.tasks.ip_address()
                self.tasks.ask_user()

            elif "help" in user_voice:
                self.tasks.help()
                self.tasks.ask_user()

            elif "exit" in user_voice:
                break

            

if _name_ == "_main_":
    execution = Execution()
    execution.run()
