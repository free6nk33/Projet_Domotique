import machine
import time
from mfrc522 import MFRC522
from machine import Pin, PWM

rdr = MFRC522(sck=18, mosi=23, miso=19, rst=22, cs=21)
# - D22  (RST) 
# - D23 (MOSI)
# - D19 (MISO)
# - D18 (SCK)
# - D21 (SDA)


pin_led = Pin(17, Pin.OUT)

# - D17 (LED)



# SERVO MOTEUR
#-----------------------------------
servo_pin = 13
pwm = PWM(Pin(servo_pin))
pwm.freq(50)

min = 26   # (0°)
max = 123  # (180°)

def move_servo(angle):
    duty = min + (max - min) * (angle / 180)
    pwm.duty_u16(int(duty * 65535 / 1000))
#-----------------------------------


print("\n Presenter le badge")

while True:
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            #print("\nBadge détecté !")
            #print(" - Type : %d" % tag_type)
            #print(" - UID : %02x.%02x.%02x.%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))

            if rdr.select_tag(raw_uid) == rdr.OK:
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                    data = rdr.read(8)
                    #print(" - Données : %s" % data)

                    if data == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                        
                        pin_led.value(1)  
                        move_servo(0)
                        time.sleep(2)
                        pin_led.value(0)
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





