
import speech_recognition as sr
import final

def main():
    r = sr.Recognizer()
    text=""
    with sr.Microphone() as source:
        while True:
            try:
                print("Say the code")
                r.adjust_for_ambient_noise(source,duration=2)
                audio = r.listen(source)
                text = r.recognize_google(audio)
                break
            except:
                print("Sorry could not recognize what you said")
        print("Ur code : {}".format(text))
        if "unlock" in text:
            final.main()

if __name__ == "__main__":
    main()
