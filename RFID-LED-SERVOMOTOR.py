'''    
    GROUPE 3

    Thibaud
    Cameron
    Antoine
    Célian

'''

from mfrc522 import MFRC522
from machine import Pin, PWM
import time


# CONNEXION MODULE RFID
rdr = MFRC522(sck=18, mosi=23, miso=19, rst=22, cs=21)
# - D22  (RST) 
# - D23 (MOSI)
# - D19 (MISO)
# - D18 (SCK)
# - D21 (SDA)

# CONNEXION MODULE LED
pin_led = Pin(17, Pin.OUT)
# - D17 (LED)

# CONNEXION MODULE SERVO
servo_pin = 13
# - D13 (SERVO)

# initialisation du servo
pwm = PWM(Pin(servo_pin))
pwm.freq(50)
min = 26   # (0°)
max = 123  # (180°)

#--------------------------------------------
#               FUNCTIONS                   |
#--------------------------------------------
def move_servo(angle):
    duty = min + (max - min) * (angle / 180)
    pwm.duty_u16(int(duty * 65535 / 1000))

def allumer_led():
    pin_led.value(1)
    
def eteindre_led():
    pin_led.value(0)
#--------------------------------------------



def main():
    '''
    Ce script gère la lecture et la gestion des badges RFID via un lecteur de badge, si le badge est valide alors des actions sont effectuées dans le cas contraire rien ne se passe.
    Dans ce script on utilise 3 modules sur les 4 que nous avions pour les interconnecter.

    Entrées :
        - badge RFID présenté au lecteur
        
    Sorties :
        YES -> action (allumer une LED et déplacer un servo-moteur)
        NO -> aucune action (rien ne se passe aucune LED allumée ou servo déplacé)
    '''

    print("\n Presenter le badge")

    while True:

        # attente de la lecture du badge
        (stat) = rdr.request(rdr.REQIDL)
        
        # lecture du badge
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:

                if rdr.select_tag(raw_uid) == rdr.OK:
                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                    if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                        data = rdr.read(8)

                        # si le badge est valide alors on effectue les actions
                        if data == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                            
                            allumer_led() 
                            move_servo(0)
                            
                            time.sleep(2)
                            eteindre_led()
                            move_servo(180)
                            
                        else:
                            pin_led.value(0) 
                            #servo.value(0)
                        
                        rdr.stop_crypto1()
                    else:
                        print("Erreur de lecture")
                else:
                    print("Erreur de sélection du badge")
        time.sleep(1)


if __name__ == '__main__':
    main()
