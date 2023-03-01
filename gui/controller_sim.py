from arm_sim.init_robot import EiT_arm
from xbox_controller import XboxController
import asyncio
import time


class Controller(XboxController):
    def __init__(self, form):
        self.arm = EiT_arm() #arm model corresponds to our physical arm
        self.form = form

        self.arm_twin = EiT_arm() #

        reader = self._readDataThread()
        sender = self._sendDataThread()
        asyncio.run(reader)
        asyncio.run(sender)

        form.onButton.clicked.connect(self._onClick)
        form.offButton.clicked.connect(self._offClick)

        super().__init__()        


    async def _readDataThread(self):        
        while True:
            ##read data from simulation
            time.sleep(0.1)             
                
                    
    async def _sendDataThread(self):
        while True:
            ##send data to simulation
            time.sleep(0.1)


    def _onClick():
        read()        

    def _offClick():
        #send
        q = [90, 60, 90, 90, 45]
        claw = 73
        self.send(q, claw)