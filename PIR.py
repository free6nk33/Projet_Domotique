
from machine import Pin,PWM
import time

detector=25 #on définit le port sur lequel on branche le détecteur

PIR=Pin(detector,Pin.IN) #initialiser le capteur

while True:
    value=PIR.value()
    print(value, end=" ")
    if value < 1:	#si un objet proche entre dans le champ de vision du capteur
        print('someone is here')	#envoyer un message annonçant la présence d'un objet
    else:			#sinon 
        print('nobody is here') # envoyer un message annonçant l'absence d'un objet
    time.sleep(0.5)	# délai lors de l'annonce des messages