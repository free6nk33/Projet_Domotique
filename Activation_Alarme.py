#s'active si l'un des détecteur est activée (gaz, mouvement, humidité...)
#amaury marley nassirah bastien
from machine import Pin, PWM
from time import sleep
import time


def Alarme():

    # Déclaration plage de fréquence du buzzer a 0
    buzzer.duty(0)
    
    for _ in range(5):  # Répéter 5 fois
        buzzer.duty(512)
        
        # Son aigu
        buzzer.freq(800)
        sleep(0.5)
        
        # Son grave
        buzzer.freq(600)
        sleep(0.5)
    
    # On éteint le buzzer
    buzzer.duty(0)
        
