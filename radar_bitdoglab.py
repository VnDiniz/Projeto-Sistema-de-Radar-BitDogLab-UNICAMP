import machine
import time
import utime
from machine import Pin, PWM, SoftI2C
import ssd1306  # Biblioteca para o display OLED
import neopixel

# Inicializa o I2C para o display OLED
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Classe para o sensor HC-SR04
class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)

    def distance_cm(self):
        # Gera um pulso de 10us no pino de trigger
        self.trigger.low()
        time.sleep_us(2)
        self.trigger.high()
        time.sleep_us(10)
        self.trigger.low()

        # Espera o retorno do pulso no pino de echo
        while self.echo.value() == 0:
            pass
        start = utime.ticks_us()

        while self.echo.value() == 1:
            pass
        end = utime.ticks_us()

        # Calcula o tempo de voo do pulso
        duration = utime.ticks_diff(end, start)

        # Distância calculada em cm
        distance = (duration / 2) * 0.0343
        return distance

# Configurações do servo e sensor HC-SR04
servo_pin = PWM(Pin(10))
servo_pin.freq(50)

sensor = HCSR04(trigger_pin=17, echo_pin=16)

# Configuração da comunicação serial
uart = machine.UART(0, baudrate=115200)

# Configuração da buzina
buzzer_pin = Pin(21)
buzzer_pwm = PWM(buzzer_pin)
buzzer_pwm.freq(2000)    # Frequência do som da buzina
buzzer_pwm.duty_u16(0)   # Inicializa a buzina desligada

# Função para ajustar a intensidade da buzina com base na distância
def adjust_buzzer_intensity(distance):
    max_distance = 20       # Distância máxima em cm para ativar a buzina
    max_intensity = 10000   # Intensidade máxima da buzina (0 a 65535) #5000

    if distance <= max_distance:
        # Mapeia a distância inversamente proporcional à intensidade
        intensity = int((1 - (distance / max_distance)) * max_intensity)
        # print(((1 - (distance / max_distance)) * max_intensity))
        # print(intensity)  # para debugar
        buzzer_pwm.duty_u16(intensity)   # para debugar
        time.sleep(0.01) 
        buzzer_pwm.duty_u16(0)
    else:
        buzzer_pwm.duty_u16(0)  # Desliga a buzina

# Função para mover o servo
def move_servo(angle):
    min_duty = 1638
    max_duty = 8192
    duty = min_duty + int((angle / 180) * (max_duty - min_duty))
    servo_pin.duty_u16(duty)

# Função para exibir no display
def display_data(data):
    oled.fill(0)   # Limpa o display
    oled.text(data, 0, 0)
    oled.show()

def clear_matriz():
    # Configuração da matriz (pino e número de LEDs)
    led_pin = 7
    num_leds = 25

    # Inicializa a matriz de LEDs e desliga todos
    matriz_leds = neopixel.NeoPixel(machine.Pin(led_pin), num_leds)
    matriz_leds.fill((0, 0, 0))  # Desliga todos os LEDs (RGB: 0,0,0)
    matriz_leds.write()

# Loop principal
clear_matriz()
while True:
    # Subir de 0 até 180 graus
    for angle in range(0, 181, 2):
        move_servo(angle)
        time.sleep(0.1)  # Tempo de espera entre os movimentos
        distance = sensor.distance_cm()

        # Ajusta a intensidade da buzina
        adjust_buzzer_intensity(distance)

        # Envia dados de ângulo e distância via serial
        data = f"{angle},{distance:.2f}"
        print(data + "\n")
        display_data(data)
        #buzzer_pwm.duty_u16(0)
        time.sleep(0.1)
        

    # Descer de 180 até 0 graus
    for angle in range(180, -1, -2):
        move_servo(angle)
        time.sleep(0.1)
        distance = sensor.distance_cm()

        # Ajusta a intensidade da buzina
        adjust_buzzer_intensity(distance)

        # Envia dados de ângulo e distância via serial
        data = f"{angle},{distance:.2f}"
        print(data + "\n")
        display_data(data)

        time.sleep(0.1)
