# import the required libraries
import cv2
import pickle
import requests
import serial
from serial import Serial
import os 
from text_to_speech import  speech
import random
import dataSetGenerator
import face_trainer

def main():
    port = serial.Serial('COM5',9600)
    def telegram_bot_sendtext(bot_message): 
        bot_token = '1712484222:AAGIgFQdqBEiH4tXC5EdFVVOqgRgC_eAoeY'
        bot_chatID = '1481812139'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        return response.json()

    video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    
    # Loaading the face recogniser and the trained data into the program
    recognise = cv2.face.LBPHFaceRecognizer_create()
    recognise.read("trainner.yml")
    
    labels = {} # dictionary
    # Opening labels.pickle file and creating a dictionary containing the label ID
    # and the name
    with open("labels.pickle", 'rb') as f:##
        og_label = pickle.load(f)##
        labels = {v:k for k,v in og_label.items()}##
        # print(labels,len(labels)) 

    cnt=[0]*len(labels)

    unknown_cnt = 0
    flaggy = 0
    speech("Face recognition started")
    while True:

        if 50-max(cnt)>10:
            print("Face recognition will be done in: ",50-max(cnt)-1,"s", end="\r",sep="")
        else:
            print("Face recognition will be done in: 0",50-max(cnt)-1,"s", end="\r",sep="")
        
        #detecting unknown case
        if(flaggy == 50-max(cnt)):
            unknown_cnt+=1
        if(unknown_cnt==100):
            speech("Face recognition failed")
            print()
            speech("Unknown person arrived")
            print("Unknown person arrived")
            port.write(str.encode("Unknown person"))
            test = telegram_bot_sendtext("Unknown person arrived")
            unknown = frame[y:y+h+50,x:x+w+50]

            cv2.imwrite("unauthorized/unknown"+str(random.randint(0, 10000000))+".jpg",unknown) # saving unknown image in unauthorized folder
            video.release()
            cv2.destroyAllWindows()
            res = input("Want to collect sample? - (y/n)")
            if(res == 'y'):
                dataSetGenerator.main()
                print("collecting samples complete")
                face_trainer.main()
            exit()

        flaggy = 50-max(cnt)

        check,frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face = cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5)
        #print(face)

        for x,y,w,h in face:
            face_save = gray[y:y+h, x:x+w]
        
            # Predicting the face identified
            ID, conf = recognise.predict(face_save)
             #print(ID,conf)
            if conf >= 75 and conf <= 115:
                unknown_cnt=0
                cv2.putText(frame,labels[ID],(x-10,y-10),cv2.FONT_HERSHEY_COMPLEX ,1, (18,5,255), 2, cv2.LINE_AA )
                if(ID == len(labels)-1):

                    cnt[ID]+=1
                    if(cnt[ID]==50):

                        port.write(str.encode('0'))
                        test = telegram_bot_sendtext("Welcome home")
                        print()
                        speech("Face recognition success");
                        speech("Welcome Home");
                        print("Face recognition success\nWelcome Amrithesh\nMessage is sent to telegram\nMessage displayed in lcd\nPlaying music")
                        video.release()
                        cv2.destroyAllWindows()
                        speech("Playing music")
                        os.system("welcome_song.mp3")
                        exit()
                else:
                    cnt[ID]+=1
                    if(cnt[ID]==50):
                        message_ = labels[ID].capitalize()+" arrived"
                        port.write(str.encode(labels[ID].capitalize()))
                        test = telegram_bot_sendtext(message_)
                        print()
                        speech("Face recognition success");
                        speech(message_);
                        print(f"Face recognition success\n{message_}\nMessage is sent to telegram\nMessage displayed in lcd\nPlaying music")
                        video.release()
                        cv2.destroyAllWindows()
                        speech("Playing music")
                        os.system("welcome_song.mp3")
                        exit()
            frame = cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,255),4)

        cv2.imshow("Video",frame)
        key = cv2.waitKey(1)
        if(key == ord('q')):
            break
        
    video.release()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()
