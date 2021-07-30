import pyttsx3
engine = pyttsx3.init()

def speech(str):
    # rate = engine.getProperty('rate')  
    # print (rate)                  
    engine.setProperty('rate', 125)    

    engine.say(str)
    engine.runAndWait()