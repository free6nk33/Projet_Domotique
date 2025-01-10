# XHARDA Mondi, PAINO Elowan, LEROY Mateo, BOSCO Mathieu


import machine   # Ce module permet d avoir acces aux fonctionnalites du microcontroleur
import time   #  Ce module permet d avoir acces à plusieurs fonctionalites liee au temps
import dht  # Cette librairie permet de fournir une interface pour lire le capteur d humidité et de temperature
from machine import I2C, Pin, PWM # On importe les classes pour la communication avec l ecran, configurer les broches, et pour controler le servomoteur
from i2c_lcd import I2cLcd  # On importe des fonctionnalités supplementaires pour controler l ecran


DHT = dht.DHT11(machine.Pin(17))  # Configuration du capteur DHT11

# Configuration de l'écran LCD
DEFAULT_I2C_ADDR = 0x27 # Indication de l'adresse par defaut I2C de l'ecran LCD
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) # Serial Clock Line connectee a la broche GPIO 22, Serial Data Line, connectee a la broche GPIO 21, Frequence de communication I2C a 400 kHz
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16) # On declare les dimensions de l'ecran en plus

# Configuration du servomoteur
servo = PWM(Pin(16), freq=50) # Creation d un objet Pulse Width Modulation qui utilise la broche GPIO 16 pour le signal du controle du servomoteur et on lui definit la frequence à 50 Hz

def set_servo_position(degrees):
    """
    Cette fonction set_servo_position est utilisée pour contrôler la position d'un servomoteur.
    
    Paramètre d'entrée :
    degrees : L'angle désiré pour le servomoteur, généralement entre 0 et 180 degrés.
    """
    duty = int(((degrees / 180) * 115) + 20) # Cette formule convertit l'angle en une valeur de rapport cyclique en entier appropriée pour le servomoteur.
    servo.duty(duty) # Applique le rapport cyclique calculé au servomoteur.

# Fonction pour ouvrir la fenêtre
def open_window():
    set_servo_position(90)  # On ajuste l'angle

# Fonction pour fermer la fenêtre
def close_window():
    set_servo_position(0)  # On ajuste l'angle

# Initialisation : fenêtre fermée
close_window()

while True:
    try:
        '''
        while True: Cette boucle infinie assure que le programme s'exécute continuellement. Elle est utilisee pour que le capteur prenne des mesures et mette a jour l'affichage regulierement.
        
        try: Le bloc try est place à l'interieur de la boucle while pour gerer les erreurs potentielles. Il englobe toutes les operations qui pourraient generer des erreurs, comme la lecture du capteur ou l'affichage sur l'ecran LCD.
             
        
        
        
        Logique d'ouverture de la fenetre :
        
        Si
            Le capteur d'humidite detecte un pourcentage d'humidite superieur ou egal a 60% on ouvre la fenetre et on affiche OPEN sur l'ecran
        Sinon
            On ferme la fenetre et on affiche CLOSED
        
        
        
        
        
        On empeche le programme de se terminer brutalement en cas d'erreur inattendue
        
        '''
        DHT.measure() # On lance la fonction pour que le capteur commence a mesurer, DHT -> (Digital-output relative Humidity & Temperature sensor)
        temperature = DHT.temperature() # On affecte la temperature recupere grace qux mesures a une variable
        humidity = DHT.humidity() # On affecte l'humidite recupere grace qux mesures a une variable
        
        # Affichage sur la console
        print(f'Temperature: {temperature}°C, Humidity: {humidity}%') # On affiche les resultats dans la console pour verifier les erreurs
        
        # Affichage sur l'écran LCD
        lcd.clear() # On efface tout que c'il y a sur l'ecran LED pour s'assurer du bon affichage et d'eviter les erreurs
        lcd.move_to(0, 0) # On indique qu'on veux se mettre à la premiere ligne, premiere colone
        lcd.putstr(f'T={temperature}C') # On affiche la temperature
        lcd.move_to(0, 1) # On indique qu'on veux se mettre à la deuxieme ligne, premiere colone
        lcd.putstr(f'H={humidity}%') # On affiche l'humidite
        
        # Logique d'ouverture de la fenêtre
        if humidity >= 60:
            open_window()
            lcd.move_to(10, 1)
            lcd.putstr('OPEN')
        else:
            close_window()
            lcd.move_to(10, 1)
            lcd.putstr('CLOSED')
        
    except Exception as e: # On capture toutes les exceptions qui heritent de la classe Exception, ce qui inclut la plupart des exceptions standard en Python
        print("Erreur:", str(e)) # On affiche un message d'erreur générique suivi de la description spécifique de l'exception
    
    time.sleep(2) # On definit un temps de supension des fonctions pour ne pas surcharger la carte
