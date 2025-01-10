from machine import Pin,PWM
import time
#amaury marley nassirah bastien

def Detecteur_Mouvement():
    Présence=False
    
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
                print('Présence détecter')
                Présence=True
                break
            else:  # Si aucun objet n'est détecté
                print('absence présence')
                Présence=False
                break
            previous_value = value  # Mettre à jour l'état précédent

        time.sleep(0.5)  # Délai pour éviter une boucle trop rapide
        
Detecteur_Mouvement()