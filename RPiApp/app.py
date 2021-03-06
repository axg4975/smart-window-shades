#!/usr/bin/python
from flask import render_template, Flask
import RPi.GPIO as GPIO
import time
from flask_cors import CORS, cross_origin

""" Sets up the RPi lib to use the Board mappings """
GPIO.setmode(GPIO.BOARD)

""" Turn off warnings """
GPIO.setwarnings(False)

""" Stepper motor setup """
DIRECTION_PIN = 38
STEP_PIN = 37

""" Number of steps of the motor to reach 100% """
global FULL_REV_STEPS
FULL_REV_STEPS = 200

""" Always starts down completely """
global CURRENT
CURRENT = 100

""" Create the Flask app with CORS """
app = Flask(__name__)
CORS(app)

"""
Default page

Only used for testing when no public server is up.
"""
@app.route("/")
def index():
    return render_template('index.html')


"""
This is the main function, it controls the motors.
Path: gpio/%
% is the amount of curtain one wants open.
"""
@app.route('/gpio/<string:percent>', methods=["GET", "POST"])
@cross_origin()
def moveShades(percent):
    # Make sure percent is between 0 and 100.
    if int(percent) > 100:
        percent = "100"
    elif int(percent) < 0:
        percent = "0"

    # The following is a way to store the current state of the curtain.
    # We already assumed it starts down.
    global CURRENT
    output_percentage = int(percent) - CURRENT
    CURRENT = int(percent)

    # Change the direction, the print statement is for debugging.
    if output_percentage < 0:
        print("UP")
        GPIO.output(DIRECTION_PIN, True)
    elif output_percentage == 0:
        print("NO CHANGE")
    else:
        print("DOWN")
        GPIO.output(DIRECTION_PIN, False)

    # Run the motor
    motor_output(output_percentage)

    # Returns 200 suggesting all went well.
    return '{"status":200}'


"""
This is to set the current path
Path: gpio/set/<string:UP or DOWN>
% is the amount of curtain one wants open.
"""
@app.route('/gpio/set/current/<string:current>', methods=["GET", "POST"])
def setCurrent(current):
    global CURRENT

    if current == "up":
        CURRENT = 0
    elif current == "down":
        CURRENT = 100

    print("CURRENT IS", CURRENT)
    return '{"status":200}'


"""
This is to set the steps
Path: gpio/set/#
% is the amount of curtain one wants open.
"""
@app.route('/gpio/set/steps/<string:steps>', methods=["GET", "POST"])
@cross_origin()
def setSteps(steps):
    global FULL_REV_STEPS
    FULL_REV_STEPS = int(steps)
    print("STEPS: ", FULL_REV_STEPS)
    return '{"status":200}'


"""
This is to get the current path
Path: gpio/set/current
% is the amount of curtain one wants open.
"""
@app.route('/gpio/get/current', methods=["GET"])
@cross_origin()
def getCurrent():
    global CURRENT
    print("CURRENT GET:", CURRENT)
    return '{"data":"'+str(CURRENT)+'" , "status":200}'


"""
This is to move the motor by the steps, useful for debugging
Path: gpio/move/#
% is the amount of curtain one wants open.
"""
@app.route('/gpio/move/<string:steps>', methods=["GET", "POST"])
@cross_origin()
def move_motor_debugger(steps):
    print("MOVE MOTOR by", steps, "STEPS")
    percentage_change = steps/FULL_REV_STEPS
    global CURRENT
    CURRENT += percentage_change

    #direction
    if int(steps) < 0:
        GPIO.output(DIRECTION_PIN, True)
    else:
        GPIO.output(DIRECTION_PIN, False)

    # track the number of steps taken
    StepCounter = 0
    # wait time controls speed, 0.001 is the smallest value
    WaitTime = 0.005

    # 200 Steps = 1 Revolution
    while StepCounter < abs(int(steps)):
        # turning the gpio on and off is equivalent of taking a step
        GPIO.output(STEP_PIN, True)
        GPIO.output(STEP_PIN, False)
        StepCounter += 1

        # Wait before taking the next step...this controls rotation speed
        time.sleep(WaitTime)
    GPIO.output(STEP_PIN, False)

    return '{"status":200}'


""" Convert software to hardware output """
def motor_output(percent):
    # Convert percent to steps
    percent = abs(percent)
    steps = int(FULL_REV_STEPS * (percent / 100.0))
    print("STEPS: ", steps)

    # track the number of steps taken
    StepCounter = 0
    # wait time controls speed, 0.001 is the smallest value
    WaitTime = 0.01

    # 200 Steps = 1 Revolution
    while StepCounter < steps:
        # turning the gpio on and off is equivalent of taking a step
        GPIO.output(STEP_PIN, True)
        GPIO.output(STEP_PIN, False)
        StepCounter += 1

        # Wait before taking the next step...this controls rotation speed
        time.sleep(WaitTime)
    GPIO.output(STEP_PIN, False)


# The "host=0.0.0.0" part is essential to telling the system that we want the app visible to the
# outside world.
if __name__ == "__main__":
   # DIRECTION_PIN = int(input("Direction pin number on PI: "))
   # STEP_PIN = int(input("Step pin number on PI: "))
    GPIO.setup(DIRECTION_PIN, GPIO.OUT)
    GPIO.setup(STEP_PIN, GPIO.OUT)

#    app.run(host='0.0.0.0', port=port, ssl_context=('/etc/letsencrypt/csr/0000_csr-certbot.pem',
#                                                    '/etc/letsencrypt/keys/0000_key-certbot.pem'))
    app.run(host='0.0.0.0', port=5000)
