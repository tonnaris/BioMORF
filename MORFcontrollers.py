import numpy as np
from ControllerBlocks import Relu

class Motormapping_angle():
    def __init__(self):
        self.input = [-0.2,0.2]

        self.output_tjoint = [1800,2200]
        self.output_cjoint = [2500,3000]
        self.output_fjoint = [1500,2000]

        self.slope_tjoint = 1.0 * (self.output_tjoint[1] - self.output_tjoint[0]) / (self.input[1] - self.input[0])
        self.slope_cjoint = 1.0 * (self.output_cjoint[1] - self.output_cjoint[0]) / (self.input[1] - self.input[0])
        self.slope_fjoint = 1.0 * (self.output_fjoint[1] - self.output_fjoint[0]) / (self.input[1] - self.input[0])

        
    def map(self,control_input):

        leg0 = [ int(self.output_tjoint[0] + self.slope_tjoint * (control_input[0]*control_input[3] - self.input[0])), 
                int(self.output_cjoint[1] + self.slope_cjoint * (Relu(-control_input[1]) - self.input[0])),
                int(self.output_fjoint[0] + self.slope_fjoint * (Relu(control_input[2]) - self.input[0]))]

        leg1 = [ int(self.output_tjoint[0] + self.slope_tjoint * (-control_input[0]*control_input[3] - self.input[0])), 
                int(self.output_cjoint[1] + self.slope_cjoint * (Relu(control_input[1]) - self.input[0])),
                int(self.output_fjoint[0] + self.slope_fjoint * (Relu(-control_input[2]) - self.input[0]))]

        leg2 = [ int(self.output_tjoint[0] + self.slope_tjoint * (control_input[0]*control_input[3] - self.input[0])), 
                int(self.output_cjoint[1] + self.slope_cjoint * (Relu(-control_input[1]) - self.input[0])),
                int(self.output_fjoint[0] + self.slope_fjoint * (Relu(control_input[2]) - self.input[0]))]

        leg3 = [ int(self.output_tjoint[0] + self.slope_tjoint * (control_input[0]*control_input[4] - self.input[0])), 
                int(self.output_cjoint[1] + self.slope_cjoint * (Relu(control_input[1]) - self.input[0])),
                int(self.output_fjoint[0] + self.slope_fjoint * (Relu(-control_input[2]) - self.input[0]))]

        leg4 = [ int(self.output_tjoint[0] + self.slope_tjoint * (-control_input[0]*control_input[4] - self.input[0])), 
                int(self.output_cjoint[1] + self.slope_cjoint * (Relu(-control_input[1]) - self.input[0])),
                int(self.output_fjoint[0] + self.slope_fjoint * (Relu(control_input[2]) - self.input[0]))]

        leg5 = [ int(self.output_tjoint[0] + self.slope_tjoint * (control_input[0]*control_input[4] - self.input[0])), 
                int(self.output_cjoint[1] + self.slope_cjoint * (Relu(control_input[1])- self.input[0])),
                int(self.output_fjoint[0] + self.slope_fjoint * (Relu(-control_input[2]) - self.input[0]))]

        return leg0 + leg1 + leg2 + leg3 + leg4 + leg5
