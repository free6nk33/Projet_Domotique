#Amir,Mohammed,Adam,Aimé
from machine import Pin, ADC
import time
import neopixel

DO_PIN = Pin(36, Pin.IN)  # Capteur de gaz
BUTTON_PIN = Pin(18, Pin.IN, Pin.PULL_UP)  # Bouton
LED_PIN = 32  # Pin des LEDs
NUM_LEDS = 4  # Nombre de LEDs

led_strip = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

adc = ADC(Pin(35))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

VAPOR_THRESHOLD = 1000  # Seuil vapeur
GAS_THRESHOLD = 500  # Seuil gaz

alarm_triggered = False
button_pressed = False
color_state = (0, 0, 0)  # Couleur initiale des LEDs

def set_leds(color):
    """
    Allume la bande de LEDs avec la couleur spécifiée.
   
    :param color: Tuple représentant la couleur en format RGB.
    """
    for i in range(NUM_LEDS):
        led_strip[i] = color
    led_strip.write()

set_leds((0, 0, 0))

while True:
    """
    Boucle principale qui lit les valeurs du capteur de vapeur et du capteur de gaz,
    et met à jour la couleur des LEDs en fonction de l'état des capteurs.
    """
    adc_val = adc.read()

    if adc_val > VAPOR_THRESHOLD:
        """
        Si la valeur lue par le capteur de vapeur dépasse le seuil,
        on déclenche l'alarme et on change la couleur des LEDs en bleu.
        """
        alarm_triggered = True
        color_state = (0, 0, 255)  # Bleu

    elif DO_PIN.value() == 1:
        """
        Si le capteur de gaz détecte du gaz (valeur 1),
        on déclenche l'alarme et on change la couleur des LEDs en rouge.
        """
        alarm_triggered = True
        color_state = (255, 0, 0)  # Rouge

    if BUTTON_PIN.value() == 0:
        """
        Si le bouton est pressé, un anti-rebond est appliqué et la fonction
        correspondante est exécutée selon l'état de l'alarme.
        """
        time.sleep(0.01)
        while BUTTON_PIN.value() == 0:
            pass  

        if alarm_triggered:
            """
            Si l'alarme est activée, la pression du bouton éteint les LEDs.
            """
            alarm_triggered = False
            color_state = (0, 0, 0)  # Éteindre les LEDs
        else:
            """
            Si aucune alarme n'est activée, on alterne entre lumière blanche
            et LEDs éteintes.
            """
            if color_state == (255, 255, 255):
                color_state = (0, 0, 0)  # Éteindre les LEDs
            else:
                color_state = (255, 255, 255)  # Lumière blanche

    set_leds(color_state)

    time.sleep(0.1)
