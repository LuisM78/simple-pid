#!/usr/bin/env python

import time
import matplotlib.pyplot as plt
from simple_pid import PID
import numpy as np

class WaterBoiler:
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """

    def __init__(self):
        self.water_temp = 20

    def update(self, boiler_power, dt):
        if boiler_power > 0.1:
            boiler_power = 1
            # Boiler can only produce heat, not cold
            self.water_temp += 1.5 * boiler_power * dt
        else:
            boiler_power = 0
            # Boiler can only produce heat, not cold
            self.water_temp += 1.5 * boiler_power * dt

        # Some heat dissipation
        self.water_temp -= .50 * dt
        return self.water_temp


if __name__ == '__main__':
    boiler = WaterBoiler()
    water_temp = boiler.water_temp

    pid = PID(5, 0.01, 0.1, setpoint=water_temp)
    pid.output_limits = (0, 1)

    start_time = time.time()
    last_time = start_time
    start_time5 = start_time4 = start_time3 = start_time2 = last_time

    # Keep track of values for plotting
    setpoint, y, x = [], [], []
    condition1 = True
    condition2 = False
    condition3 = False
    condition4 = False
    condition5 = False

    while time.time() - start_time < 220:
        current_time = time.time()
        dt = current_time - last_time

        power = pid(water_temp)
        print(power)
        water_temp = boiler.update(power, dt)

        x += [current_time - start_time]
        y += [water_temp]
        setpoint += [pid.setpoint]

        if current_time - start_time > 1 and condition1:
            pid.setpoint = 30
            if abs(water_temp - pid.setpoint) < 0.2:
                print('temperature reached, keeping for another 30')
                start_time2 = time.time() 
                condition2 = True
                condition1 = False             
        if current_time - start_time2 > 35 and condition2:
            pid.setpoint = 45
            if abs(water_temp - pid.setpoint) < 0.2:
                print('temperature reached, keeping for another 50')
                start_time3 = time.time() 
                condition3 = True
                condition2 = False
        if current_time - start_time3> 10 and condition3:
            pid.setpoint = 25
            if abs(water_temp - pid.setpoint) < 0.2:
                print('temperature reached, keeping for another 20')
                start_time4 = time.time() 
                condition4 = True
                condition3 = False
        if current_time - start_time4 > 20 and condition4:
            pid.setpoint = 25
            if abs(water_temp - pid.setpoint) < 0.2:
                print('temperature reached, keeping for another 20')
                start_time5 = time.time() 
                condition5 = True
                condition4 = False
        if current_time - start_time5 > 10 and condition5:
            pid.setpoint = 20
 
        last_time = current_time

    plt.plot(x, y, label='measured')
    plt.plot(x, setpoint, label='target')
    plt.xticks(np.arange(min(x), max(x)+1, 5.0))
    plt.xlabel('time')
    plt.ylabel('temperature')
    plt.legend()
    plt.show()
