#!/usr/bin/env python3

from CPG import CPG

import numpy as np
def main():
    cpg_walk = CPG()
    cpg_walk.set_frequency()
    cpg_breathe = CPG()
    cpg_breathe.set_frequency()
    
    motion = "set"
    motion_before = "set"
    speed = "sigma"
    sigma = 0.03
    MOTOR1_DATA = 0  
    MOTOR2_DATA = 0

    breathe_state_0 = True
    breathe_state_1 = True

    arduino_control = [0,0]
    signal_leg = [0,0,0,0,0]
    count_change = 0
    count_motion = 0
    set_sequence = False
    pump = False

    #----------------------------------------------------------------------------
    # the breathing freq. will start from set_alpha to max_alpha with change speed of rate_alpha
    # increse alpha: fast breathing  / decreses alpha: slow breathing
    set_alpha = 0.01 
    alpha = set_alpha
    min_alpha = set_alpha
    max_alpha = 0.1
    rate_alpha = 0.000002
    
    # the deuration will start from set_shif_cpg_breathe to max_shif_cpg_breathe with change speed of rate_cpg_breathe
    # increse shif_cpg_breathe: let less air flow in and let more air flow out/ decreses shif_cpg_breathe: let more air flow in and let less air flow out
    # 0 mean 50% air flow in and 50% air flow out 
    set_shif_cpg_breathe = 0.00
    shif_cpg_breathe = set_shif_cpg_breathe
    min_shif_cpg_breathe = set_shif_cpg_breathe
    max_shif_cpg_breathe = 0.15
    rate_cpg_breathe = 0.0002


    #----------------------------------------------------------------------------


    while True:

        if motion != "set":
            if motion != "stop" and count_change < 1:
                signal_leg[0] *= count_change
                signal_leg[1] *= count_change
                signal_leg[2] *= count_change
                count_change += 0.005
            cpg_walk_data = np.array(cpg_walk.update())

        if motion == "set":
            count_change = 0
            sigma = 0.03
            dynamixel_positon = mapping.map([0,0,0,1,1]) 
            cpg_walk = CPG()
            cpg_walk.set_frequency(sigma * np.pi)
        elif motion == "forward":
            signal_leg[0] = cpg_walk_data[0]
            signal_leg[1] = cpg_walk_data[1] 
            signal_leg[2] = -cpg_walk_data[1]
            signal_leg[3] = 1
            signal_leg[4] = 1
        elif motion == "backward":
            signal_leg[0] = -cpg_walk_data[0]
            signal_leg[1] = cpg_walk_data[1] 
            signal_leg[2] = -cpg_walk_data[1]
            signal_leg[3] = 1
            signal_leg[4] = 1
        elif motion == "left":
            signal_leg[0] = cpg_walk_data[0]
            signal_leg[1] = cpg_walk_data[1] 
            signal_leg[2] = -cpg_walk_data[1]
            signal_leg[3] = 0.5
            signal_leg[4] = 1
        elif motion == "right":
            signal_leg[0] = cpg_walk_data[0]
            signal_leg[1] = cpg_walk_data[1] 
            signal_leg[2] = -cpg_walk_data[1]
            signal_leg[3] = 1
            signal_leg[4] = 0.5
        elif motion == "stop":
            if count_change > 0:
                count_change -= 0.005
                if motion_before == "forward":
                    signal_leg[0] = cpg_walk_data[0] * count_change
                    signal_leg[1] = cpg_walk_data[1] * count_change
                    signal_leg[2] = -cpg_walk_data[1]* count_change
                    signal_leg[3] = 1
                    signal_leg[4] = 1
                elif motion_before == "backward":
                    signal_leg[0] = -cpg_walk_data[0]* count_change
                    signal_leg[1] = cpg_walk_data[1] * count_change
                    signal_leg[2] = -cpg_walk_data[1]* count_change
                    signal_leg[3] = 1
                    signal_leg[4] = 1
                elif motion_before == "left":
                    signal_leg[0] = cpg_walk_data[0]* count_change
                    signal_leg[1] = cpg_walk_data[1] * count_change
                    signal_leg[2] = -cpg_walk_data[1]* count_change
                    signal_leg[3] = 0.5
                    signal_leg[4] = 1
                elif motion_before == "right":
                    signal_leg[0] = cpg_walk_data[0]* count_change
                    signal_leg[1] = cpg_walk_data[1] * count_change
                    signal_leg[2] = -cpg_walk_data[1]* count_change
                    signal_leg[3] = 1
                    signal_leg[4] = 0.5
                    
        if motion != "stop":
            motion_before = motion

        if speed == "+sigma":
            sigma += 0.0001
            if sigma >= 0.06: sigma = 0.06
            cpg_walk.set_frequency(sigma * np.pi)
        elif speed == "-sigma":
            sigma -= 0.0001
            if sigma <= 0.01: sigma = 0.01
            cpg_walk.set_frequency(sigma * np.pi)

        if motion == "set":
            arduino_control = [0,0]
            alpha = set_alpha
            shif_cpg_breathe = set_shif_cpg_breathe
            cpg_breathe = CPG()
            cpg_breathe.set_frequency()
        elif motion == "stop":
            alpha -= rate_alpha
            if alpha <= min_alpha: alpha = min_alpha
            shif_cpg_breathe -= rate_cpg_breathe
            if shif_cpg_breathe <= min_shif_cpg_breathe: shif_cpg_breathe = min_shif_cpg_breathe
            cpg_breathe.set_frequency(alpha * np.pi)
        else:
            alpha += rate_alpha
            if alpha >= max_alpha: alpha = max_alpha
            shif_cpg_breathe += rate_cpg_breathe
            if shif_cpg_breathe >= max_shif_cpg_breathe: shif_cpg_breathe = max_shif_cpg_breathe
            cpg_breathe.set_frequency(alpha * np.pi)

            
        if motion != "set":
            cpg_breathe_data_0 = np.array(cpg_breathe.update())[0] + shif_cpg_breathe
            cpg_breathe_data_1 = np.array(cpg_breathe.update())[1] + shif_cpg_breathe

            if breathe_state_0 == True and cpg_breathe_data_0 >= 0:
                MOTOR1_DATA = 0
                breathe_state_0 = False
            elif breathe_state_0 == False and cpg_breathe_data_0 < 0:
                MOTOR1_DATA = 1
                breathe_state_0 = True

            if breathe_state_1 == True and cpg_breathe_data_1 >= 0:
                MOTOR2_DATA = 0
                breathe_state_1 = False
            elif breathe_state_1 == False and cpg_breathe_data_1 < 0:
                MOTOR2_DATA = 1
                breathe_state_1 = True
       
           
