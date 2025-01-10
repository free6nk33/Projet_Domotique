#s'active si le bouton de la sonnette est appuyer ET que le badge n'est pas passer (porte pas ouverte)

from machine import Pin, PWM
from time import sleep
import time

#amaury marley nassirah bastien

def Sonnette():
    # Déclaration pin du buzzer
    buzzer = PWM(Pin(25))

    # Déclaration pin du button
    button1 = Pin(16, Pin.IN, Pin.PULL_UP)

    # Déclaration plage de fréquence du buzzer a 0
    buzzer.duty(0)

    while True:
        btnVal1 = button1.value()
        if btnVal1 == 0:
            buzzer.duty(1000)
            buzzer.freq(10)  
            sleep(0.4)
            buzzer.freq(30) 
            sleep(0.4)
            buzzer.freq(40)
            sleep(0.4)
            buzzer.freq(5)
            sleep(0.4)
            # On éteint le buzzer
            buzzer.duty(0)
            break
