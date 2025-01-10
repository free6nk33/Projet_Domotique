from time import sleep_ms, ticks_ms
from machine import SoftI2C, Pin, PWM, SPI
from i2c_lcd import I2cLcd
from mfrc522 import MFRC522
import time



# Paramètres LCD
DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

# Capteur PIR
detector = 25
PIR = Pin(detector, Pin.IN)

# Paramètres RFID
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
rdr = MFRC522(sck=18, mosi=23, miso=19, rst=26, cs=5)  # Vérifiez que `cs=5` est la bonne broche pour votre CS.

# LED et Servo
pin_led = Pin(17, Pin.OUT)
servo_pin = 13
pwm = PWM(Pin(servo_pin))
pwm.freq(50)

# Servomoteur limites
servo_min = 26   # (0°)
servo_max = 123  # (180°)

# Fonction pour bouger le servomoteur
def move_servo(angle):
    duty = servo_min + (servo_max - servo_min) * (angle / 180)
    pwm.duty_u16(int(duty * 65535 / 1000))

# Initialisation
lcd.clear()
lcd.putstr('Nobody is here')
previous_pir_value = None  # État précédent du capteur PIR
move_servo(180)  # Fermer le servomoteur par défaut
pin_led.value(0)  # Éteindre la LED par défaut

print("\nPrésenter le badge")

while True:
    # Détection de mouvement avec PIR
    pir_value = PIR.value()

    if pir_value != previous_pir_value:
        if pir_value == 1:  # Mouvement détecté
            lcd.clear()
            lcd.putstr('Someone is Here')
        else:  # Aucun mouvement détecté
            lcd.clear()
            lcd.putstr('Nobody is here')
        
        previous_pir_value = pir_value

    # Lecture du badge RFID
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            print("\nBadge détecté !")
            print(" - UID : %02x.%02x.%02x.%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))

            if rdr.select_tag(raw_uid) == rdr.OK:
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                    data = rdr.read(8)
                    
                    if data == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                        print("Badge valide ! Accès autorisé.")
                        pin_led.value(1)  # Allumer la LED
                        move_servo(0)  # Ouvrir le servomoteur
                        lcd.clear()
                        lcd.putstr("Access Granted")
                        time.sleep(2)
                        pin_led.value(0)  # Éteindre la LED
                        move_servo(180)  # Fermer le servomoteur
                        lcd.clear()
                        lcd.putstr('Nobody is here')
                    else:
                        print("Badge non reconnu. Accès refusé.")
                        lcd.clear()
                        lcd.putstr("Access Denied")
                        pin_led.value(0)
                    
                    rdr.stop_crypto1()
                else:
                    print("Erreur de lecture du badge")
            else:
                print("Erreur de sélection du badge")
    
    time.sleep(0.5)  # Délai pour réduire la charge du processeur

