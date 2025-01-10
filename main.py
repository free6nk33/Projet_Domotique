import threading
import time 
import os
from machine import SoftI2C, Pin, PWM, SPI, ADC
from i2c_lcd import I2cLcd
from mfrc522 import MFRC522
from time import sleep_ms, ticks_ms
import neopixel


#compteur alerte 
compteur_alert = 0

#bouton pour activer le capteur RFID
bp_rfid = Pin(13, Pin.IN)

#bouton buzzer
buzzer = PWM(Pin(26))

rdr = MFRC522(sck=18, mosi=23, miso=19, rst=22, cs=21)
pin_led = Pin(16, Pin.OUT)
servo_porte = 14
porte = PWM(Pin(servo_pin))
porte.freq(50)

servo_fenetre = 25
fenetre = PWM(Pin(servo_fenetre))
fenetre.freq(50)

min = 26   # (0°)
max = 123  # (180°)


def move_servo_fenetre(angle):
    duty = min + (max - min) * (angle / 180)
    fenetre.duty_u16(int(duty * 65535 / 1000))

def move_servo_porte(angle):
    duty = min + (max - min) * (angle / 180)
    porte.duty_u16(int(duty * 65535 / 1000))

# Paramètres LCD
DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)


# Définition des broches et initialisation des périphériques
DO_PIN = Pin(36, Pin.IN)  # Capteur de gaz
BUTTON_PIN = Pin(12, Pin.IN, Pin.PULL_UP)  # Bouton
LED_PIN = 5  # Pin des LEDs
NUM_LEDS = 4  # Nombre de LEDs


led_strip = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

adc = ADC(Pin(35))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

# Seuils pour les capteurs
VAPOR_THRESHOLD = 1000  # Seuil vapeur
GAS_THRESHOLD = 500  # Seuil gaz

# Variables globales partagées entre les threads
alarm_triggered_gaz = False
alarm_triggered_vapeur = False
button_pressed = False
color_state = (0, 0, 0)  # Couleur initiale des LEDs
lock = threading.Lock()  # Pour protéger l'accès aux variables partagées



    
def set_leds(color):
    for i in range(NUM_LEDS):
        led_strip[i] = color
    led_strip.write()

def reset_alert():
    if bp_reset.value() == 1:
        compteur_alert = 0

def read_sensors():
    global alarm_triggered_gaz, alarm_triggered_vapeur, color_state

    while True:
        adc_val = adc.read()
        with lock:  
            if adc_val > VAPOR_THRESHOLD:
                alarm_triggered_vapeur = True
                color_state = (0, 0, 255)
                lcd.putstr("Seuil vapeur:")
                lcd.putstr(str(VAPOR_THRESHOLD)) 
            elif DO_PIN.value() == 1:
                lcd.putstr("Seuil Gaz:")
                lcd.putstr(str(GAS_THRESHOLD))
                alarm_triggered_gaz = True
                color_state = (255, 0, 0)  

        time.sleep(0.1)


def handle_button():
    global alarm_triggered_gaz, alarm_triggered_vapeur, color_state
    while True:
        if BUTTON_PIN.value() == 1:
            time.sleep(0.01) 
            while BUTTON_PIN.value() == 0:
                pass  
            
            with lock:
                if alarm_triggered_gaz:
                    alarm_triggered_gaz = False
                    color_state = (0, 0, 0)
                elif alarm_triggered_vapeur:
                    alarm_triggered_vapeur = False
                    color_state = (0, 0, 0) 
                else:
                    if color_state == (255, 255, 255):
                        color_state = (0, 0, 0)
                    else:
                        color_state = (255, 255, 255)

        time.sleep(0.1)

def update_leds():
    global color_state
    while True:
        with lock:  
            set_leds(color_state)
        time.sleep(0.1)

def btn_on():
    while True:
        if bp_rfid.value() == 1:
            global porte
            porte = False
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
            lcd.clear()
            lcd.putstr("Présenter le badge")
            time.sleep(5)
            lcd.clear()
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                        #print("\nBadge détecté !")
                        #print(" - Type : %d" % tag_type)
                        #print(" - UID : %02x.%02x.%02x.%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    lcd.putstr("Badge détecté")
                    if rdr.select_tag(raw_uid) == rdr.OK:
                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                        if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                            data = rdr.read(8)
                                #print(" - Données : %s" % data)
                            if data == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                                    
                                pin_led.value(1)  
                                move_servo(0)

                                lcd.putstr("Porte ouvert")
                                porte = True
                                if porte == True:
                                    lcd.clear()
                                    lcd.putstr("Activation du capteur steam")
                                    read_sensors()
                                    detect_mouvement()
                                    if alarm_triggered_vapeur == True:
                                        update_leds()
                                        compteur_alert += 1
                                        fermer_maison()
                                        ouvrir_fenetre()
                                        buzzer.duty(0)
                                        for _ in range(2):  # Répéter 2 fois
                                            buzzer.duty(512)
                                                # Son aigu
                                            buzzer.freq(800)
                                            sleep(0.5)
                                            # Son grave
                                            buzzer.freq(600)
                                            sleep(0.5)
                                            # On éteint le buzzer
                                            buzzer.duty(0)
                                    elif alarm_triggered_gaz == True:
                                        update_leds()
                                        compteur_alert += 1
                                        fermer_maison()
                                        allumer_elisse()
                                        buzzer.duty(0)
                                        for _ in range(2):  # Répéter 2 fois
                                            buzzer.duty(512)
                                            # Son aigu
                                            buzzer.freq(800)
                                            time.sleep(0.5)
                                            # Son grave
                                            buzzer.freq(600)
                                            time.sleep(0.5)
                                            # On éteint le buzzer
                                            buzzer.duty(0)
                                if presence == True:
                                    lcd.clear()
                                    lcd.putstr("Presence détectée")

                                                
                            else:
                                pin_led.value(0) 
                                #servo.value(0)            
                            rdr.stop_crypto1()
                        else:
                            print("Erreur de lecture")
                    else:
                        print("Erreur de sélection du badge")

                time.sleep(1)
            for i in range(11):
                time.sleep(1)
                if i > 10:
                    btn_rfid_off()
                    compteur_alert = 1 + compteur_alert
    else:
        btn_rfid_off()

def btn_off():
    while True:
        if bp_moteur.value() == 0:
            lcd.clear()
            lcd.putstr("Arrêtr du programme")
            break

def allumer_elisse():
    pwm_in_p = PWM(Pin(7))
    pwm_in_p.freq(2000)  
    pwm_in_p.duty(512)  
    pwm_in_m = PWM(Pin(8))  
    pwm_in_m.freq(1000)  
    pwm_in_m.duty(256)  
    time.sleep(5)
    pwm_in_p.duty(0)
    pwm_in_m.duty(0)


def detect_mouvement():
    global presence
    presence = False
    
    detector=14 #on définit le port sur lequel on branche le détecteur

    PIR=Pin(detector,Pin.IN) #initialiser le capteur

    # Initialiser le capteur
    previous_value = None  # Variable pour stocker l'état précédent

    while True:
        value_PIR=PIR.value()        
        print(value, end=" ")

        # Vérifiez si l'état a changé
        if value != previous_value:
            if value < 1:  # Si un objet est détecté
                compteur_alert += 1
                presence=True
                fermer_maison()
                fermer_fenetre()

            else:  # Si aucun objet n'est détecté
                presence=False
                break
            previous_value = value  # Mettre à jour l'état précédent

        time.sleep(0.5)  # Délai pour éviter une boucle trop rapide
        

def fermer_maison():
    if compteur_alert == 4:
        time.sleep(10)

        pin_led.value(0)
        move_servo_porte(180)

def ouvrir_fenetre():
    if compteur_alert >= 1:
        move_servo_fenetre(180)
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

def fermer_fenetre():
    move_servo_fenetre(180)
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

mouvement_thread = threading.Thread(target=detect_mouvement)
sensor_thread = threading.Thread(target=read_sensors)
button_thread = threading.Thread(target=handle_button)
led_thread = threading.Thread(target=update_leds)
sensor_thread.start()
button_thread.start()
led_thread.start()
mouvement_thread.start()
try:
    while True:
        time.sleep(1) 
except KeyboardInterrupt:
    print("Programme arrêté.")