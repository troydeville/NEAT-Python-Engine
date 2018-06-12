import RPi.GPIO as GPIO
from Engine import Engine

#################################################################################
#
# This project was created for processing a NEAT model on the Raspberry Pi.
# To create a model, use the "NEAT-swift" implementation on github:
#             "https://github.com/troydeville/NEAT-swift"
# Simply load a configuration file, which is generated
#   by printing the Genome's description, and run inputs.
#
# The model is just a text file with the genome's description pasted in it.
#
#################################################################################

# Component Definitions ->  [ 000, 001, 010, 011, 100, 101, 110, 111 ] LSB Right
LED = 25
SWITCH_1 = 14
SWITCH_2 = 15

# GPIO Setup
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(SWITCH_1, GPIO.IN)
GPIO.setup(SWITCH_2, GPIO.IN)

# NEAT-Python-Engine
engine = Engine("model.txt")

def main():

    # Get input from switches
    msbOn = GPIO.input(SWITCH_1)
    lsbOn = GPIO.input(SWITCH_2)

    msb = 0.0
    lsb = 0.0

    if msbOn:
        msb = 1.0

    if lsbOn:
        lsb = 1.0

    result = engine.run([msb, lsb])

    if result[0] > 0.5:
        GPIO.output(LED, GPIO.HIGH)
    else:
        GPIO.output(LED, GPIO.LOW)



# Run here
while True:
    main()




