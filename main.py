import cv2

from playsound import playsound

from plyer import notification

import smtplib

#ifttt

from twilio.rest import Client


def notify_firealert():
    notification.notify(
        title="Fire Alert!!!",
        message="This Place Is Under Fire.",
        app_icon="fire.ico",
        timeout=10
    )


def email_firealert():
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()
    
    s.login("@gmail.com", "pwd")

    message = "Fire Alert!!!"

    s.sendmail("@gmail.com", "@gmail.com", message)

    s.quit()


def sms_firealert():
    account_sid = "ACf133ff1109bcf"
    auth_token = 'a6bfddb155b1ee72'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Fire Alert!!!", from_="+1", to="+91")

    print(message.sid)


def mark(img):
    image = cv2.imread(img)
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # apply a Gaussian blur to the image then find the brightest
    # region
    gray = cv2.GaussianBlur(gray,(41,41),0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    # print(maxVal)
    if(maxVal>100):
        image = orig.copy()
        cv2.circle(image, maxLoc, 60, (255, 0, 0), 2)
        # display the results of our newly improved method
        cv2.imshow("Output", image)
        cv2.imwrite("casedetected%d.jpg" % (count-1), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


fire_cascade = cv2.CascadeClassifier('trained_fire.xml')

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX

tot_fire = 0
count = 0


while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    for (x, y, w, h) in fire:
        notify_firealert()
        success,image = cap.read()
        while success:
            cv2.imwrite("case%d.jpg" % count, image)     # save frame as JPEG file      
            success,image = cap.read()
            print('Read a new frame: ', success)
            count += 1
            break
        mark("case%d.jpg" % (count-1))
        playsound('fire_alert.mp3')
        email_firealert()
        sms_firealert()
        print("All Emergency Alerts Are Sent!")

        tot_fire = tot_fire+1
    cv2.putText(frame, "Fire Cases Till Now: "+str(tot_fire),
                (100, 50), font, 1, (0, 0, 255), 2, cv2.LINE_4)
    cv2.imshow('Output', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
