import numpy as np
import matplotlib.pyplot as plt
import krpc
import time

conn = krpc.connect(name='Hello World')
vessel = conn.space_center.active_vessel
print(vessel.name)

target_altitude = 60
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
vessel.control.sas = True

Kp = 1.1810
Ki = 0
Kd = 0.67820

SumError = 0
lastAltitude = 0

initialTime = time.time()

plot = []
deployed = False

vessel.control.activate_next_stage()
while altitude() < 500:
    vessel.control.throttle = 1.0

while vessel.available_thrust > 0:
    thisAltitude = altitude()
    ''' if thisAltitude < 100:
        if not deployed:
            deployed = True
            vessel.control.gear = True
    elif thisAltitude < 400:
        vessel.control.rcs = False
        vessel.control.sas_mode = vessel.control.sas_mode.stability_assist
        vessel.auto_pilot.target_pitch = 90.0
    else:
        vessel.control.rcs = True
        vessel.control.sas_mode = vessel.control.sas_mode.retrograde '''
    if thisAltitude < 100 and not deployed:
        deployed = True
        vessel.control.gear = True
    error = target_altitude - thisAltitude
    derivative = (thisAltitude - lastAltitude) / 0.001
    if (derivative != 0):
        vessel.control.throttle = Kp * error + Ki * SumError - Kd * derivative
        print("altitude = " + str(thisAltitude) + " throttle = " + str(vessel.control.throttle) + " error = " + str(error) + " SumError = " + str(SumError) + " derivative = " + str(derivative))
        SumError = SumError + error
        lastAltitude = thisAltitude

        timeToAppend = time.time() - initialTime

        plot.append([timeToAppend, thisAltitude, error, vessel.control.throttle])

x = []
yError = []
yAltitude = []
yThrottle = []

for point in plot:
    x.append(point[0])
    yAltitude.append(point[1])
    yError.append(point[2])
    yThrottle.append(point[3])

plt.subplot(2,2,1)
plt.plot(x, yAltitude)

plt.subplot(2,2,2)
plt.plot(x, yError)

plt.subplot(2,2,3)
plt.plot(x, yThrottle)
plt.show()