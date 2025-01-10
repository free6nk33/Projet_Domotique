#cameron
import esp
from machine import Pin, PWM


#Config Pin pour faire tourner le moteur
pwm_in_p = PWM(Pin(12))
freq = pwm_in_p.freq()
pwm_in_p.freq(2000)
duty = pwm_in_p.duty()

pwm_in_m = PWM(Pin(14))
freq = pwm_in_m.freq()
pwm_in_m.freq(1000)
duty = pwm_in_m.duty()
pwm_in_m.duty(256)


