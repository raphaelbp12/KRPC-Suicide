import numpy as np
import matplotlib.pyplot as plt
import krpc
import time

conn = krpc.connect(name='Hello World')
vessel = conn.space_center.active_vessel
print(vessel.name)

target_altitude = 2000
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
vessel.control.sas = True

Kp = 1.1810
Ki = 0
Kd = 0.52820

SumError = 0
lastAltitude = 0

vessel.control.activate_next_stage()

initialTime = time.time()

plot = []

while vessel.available_thrust > 0:
    error = target_altitude - altitude()
    derivative = (altitude() - lastAltitude) / 0.001
    if (derivative != 0):
        vessel.control.throttle = Kp * error + Ki * SumError - Kd * derivative
        print("altitude = " + str(altitude()) + " throttle = " + str(vessel.control.throttle) + " error = " + str(error) + " SumError = " + str(SumError) + " derivative = " + str(derivative))
        SumError = SumError + error
        lastAltitude = altitude()

        timeToAppend = time.time() - initialTime

        plot.append([timeToAppend, altitude(), error, vessel.control.throttle])

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