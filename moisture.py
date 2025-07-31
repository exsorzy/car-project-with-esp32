from machine import Pin, ADC
import time

MOISTURE_SENSOR_PIN = 34
RELAY_PIN = 27

moisture_sensor = ADC(Pin(MOISTURE_SENSOR_PIN))
moisture_sensor.atten(ADC.ATTN_11DB)

relay = Pin(RELAY_PIN, Pin.OUT)
relay.value(1)

MOISTURE_THRESHOLD = 3000

def read_moisture():
    value = moisture_sensor.read()
    print("Moisture level:", value)
    return value

def control_pump(moisture_level):
    if moisture_level > MOISTURE_THRESHOLD:
        print("Soil is dry. Turning pump ON.")
        relay.value(0)
    else:
        print("Soil is moist. Turning pump OFF.")
        relay.value(1)

try:
    while True:
        moisture = read_moisture()
        control_pump(moisture)
        time.sleep(5)
except KeyboardInterrupt:
    print("Auto-watering system stopped.")
    relay.value(1)
