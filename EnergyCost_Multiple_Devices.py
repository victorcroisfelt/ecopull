import numpy as np

class Device:
    def __init__(self, retransmission) -> None:
        # self.numbImages = np.random.randint(10,100)
        self.numbImages = 10
        self.ImgImportance = np.random.randint(0,100,self.numbImages)
        self.E_MUAC = 3.7 # cost of MUAC operation in pJ
        self.E_m = 2*3.7 
        self.E_d = 128*3.7 # cost of d-ram access
        self.E_l = 3.7 # cost of s-ram access
        self.p=64
        self.xi = 108*10**-3 # energy cost of transmitting in mW (108mW)
        self.R = 10**5 # data rate in bps
        self.successfulTransmissions = 0
        self.transmissionAttempts = 0
        self.finished = False
        self.imagesToTransmit = 5
        self.retransmission = retransmission

    def processCost_Data(self):
        N_c = 477388800 # number of MUAC operations for compression model
        A_s = 3542400 # number of activations for compression model
        N_s = 18456 # number of weights for compression model
        I=[640,480] # image size
        # cost of using model in d-ram
        E_Ad = 2*self.E_m*A_s + (self.E_d*N_c)/(np.sqrt(self.p))
        E_Wd = self.E_m*N_s + (self.E_d*N_c)/np.sqrt(self.p)
        E_Cd = self.E_MUAC * (N_c+3*A_s)
        I_s = I[0]*I[1]*4.86 # image size in bits
        E_i = self.E_d*10**-12*I_s # cost of accessing images from d-ram

        E_HWd = (E_Cd+E_Wd+E_Ad)*10**-12 # cost of using model on 1 image

        return (E_HWd+E_i)*self.imagesToTransmit
    
    def processCost_Behaviour(self):
        N_c = 117000000 # number of MUAC operations for inference model
        A_s = 4309000 # number of activations for inference model
        N_s = 976000 # number of weights for inference model

        I=[640,480] # image size
        # cost of using model in d-ram
        E_Ad = 2*self.E_m*A_s + (self.E_d*N_c)/(np.sqrt(self.p))
        E_Wd = self.E_m*N_s + (self.E_d*N_c)/np.sqrt(self.p)
        E_Cd = self.E_MUAC * (N_c+3*A_s)
        I_s = I[0]*I[1]*4.86 # image size in bits
        E_i = self.E_d*10**-12*I_s # cost of accessing images from d-ram

        E_HWd = (E_Cd+E_Wd+E_Ad)*10**-12 # cost of using model on 1 image

        return (E_HWd+E_i)*self.numbImages
    
    def chooseSlot(self, length):
        self.transmissionAttempts += 1
        if not self.retransmission and self.transmissionAttempts == self.imagesToTransmit:
            self.finished = True
        return np.random.randint(0,length)

    def transmit(self, prob):
        attempt = True if np.random.random()<prob else False
        if attempt:
            self.transmissionAttempts += 1
            if not self.retransmission and self.transmissionAttempts == self.imagesToTransmit:
                self.finished = True

        return attempt

    def success(self):
        self.successfulTransmissions += 1
        if self.successfulTransmissions == self.imagesToTransmit:
            self.finished = True

    def transmissionCost(self):
        I=[640,480] # image size
        I_sr = I[0]*I[1]*0.072 # prompt size in bits
        C_I = (I_sr/self.R)*self.xi # cost of transmitting 1 prompt in mW
        return C_I*self.transmissionAttempts

    def getTotalCost(self):
        modelCost = self.processCost_Behaviour() + self.processCost_Data()
        transmissionCost = self.transmissionCost()
        return modelCost + transmissionCost


def main():
    numbDevices = 10
    numbSlots = 10
    retransmissions = True
    transmissionProb = 0.1 # only used when there is 1 slot per frame

    devices = [Device(retransmissions) for _ in range(numbDevices)]
    done = False
    finished = [False for _ in range(numbDevices)]
    # We simulate the transmission in slots and frames by iterating through frames one at a time and checking which slots each device is trying to transmit in.
    # Each device has a certain amount of data they want to transmit given by the number of their starting images are relevant. 
    # Each device will try to transmit an image until all relevant images are transmitted.
    # A transmission is only successfull if there are no other transmissions in the slot.
    # In the case of only one slot per frame, the devices transmit with a probability instead of choosing a random slot.
    while False in finished:
        slots = np.full([numbSlots,numbDevices], False)
        for i, device in enumerate(devices):
            if device.finished:
                finished[i] = True
                continue
            if numbSlots > 1:
                slots[device.chooseSlot(numbSlots),i] = True
            else:
                slots[0,i] = device.transmit(transmissionProb)
        for slot in slots:
            if sum(slot) == 1:
                devices[np.argmax(slot)].success()

    costs = [device.getTotalCost() for device in devices]
    print(costs)

    successes = [device.successfulTransmissions for device in devices]
    print(successes)

    attempts = [device.transmissionAttempts for device in devices]
    print(attempts)
    return 0


if __name__ == "__main__":

    main()

