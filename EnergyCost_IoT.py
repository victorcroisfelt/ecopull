import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

E_MUAC = 3.7 # cost of MUAC operation in pJ
E_m = 2*3.7 
E_d = 128*3.7 # cost of d-ram access
E_l = 3.7 # cost of s-ram access
p=64
xi = 108*10**-3 # energy cost of transmitting in mW (108mW)
# xi = 186*3.3*10**-3
CodeRate = 3/4
R = 10**5 # data rate in bps


def getRateSavings(rate):

    # small model
    N_c = 477388800 # number of MUAC operations
    A_s = 3542400 # number of activations
    N_s = 18456 # number of weights
    I=[640,480]

    # cost using model in s-ram
    E_As = 2*E_m*A_s + (E_l*N_c)/(np.sqrt(p))
    E_Ws = E_m*N_s + (E_l*N_c)/np.sqrt(p)
    E_Cs = E_MUAC * (N_c+3*A_s)

    E_HWs = (E_Cs+E_Ws+E_As)*10**-12 # cost of using model on 1 image

    # cost of using model in d-ram
    E_Ad = 2*E_m*A_s + (E_d*N_c)/(np.sqrt(p))
    E_Wd = E_m*N_s + (E_d*N_c)/np.sqrt(p)
    E_Cd = E_MUAC * (N_c+3*A_s)

    E_HWd = (E_Cd+E_Wd+E_Ad)*10**-12 # cost of using model on 1 image
    
    I_s = I[0]*I[1]*4.86 # image size in bits
    I_sr = I[0]*I[1]*0.072 # prompt size in bits
    C_i = (I_s/rate)*xi # cost of transmitting 1 image in mW
    C_ir = (I_sr/rate)*xi # cost of transmitting 1 prompt in mW
    E_i = E_d*10**-12*I_s # cost of accessing images from d-ram
    # print(I, E_HWd, C_ir)
    # savings
    savings = C_i - C_ir - E_i - E_HWd
    return savings, (C_ir+E_i+E_HWd)/C_i 






def getSavings(I=[640,480]):

    # small model
    N_c = 477388800 # number of MUAC operations
    A_s = 3542400 # number of activations
    N_s = 18456 # number of weights

    # cost using model in s-ram
    E_As = 2*E_m*A_s + (E_l*N_c)/(np.sqrt(p))
    E_Ws = E_m*N_s + (E_l*N_c)/np.sqrt(p)
    E_Cs = E_MUAC * (N_c+3*A_s)

    E_HWs = (E_Cs+E_Ws+E_As)*10**-12 # cost of using model on 1 image

    # cost of using model in d-ram
    E_Ad = 2*E_m*A_s + (E_d*N_c)/(np.sqrt(p))
    E_Wd = E_m*N_s + (E_d*N_c)/np.sqrt(p)
    E_Cd = E_MUAC * (N_c+3*A_s)

    E_HWd = (E_Cd+E_Wd+E_Ad)*10**-12 # cost of using model on 1 image
    
    I_s = I[0]*I[1]*4.86 # image size in bits
    I_sr = I[0]*I[1]*0.072 # prompt size in bits
    C_i = (I_s/R)*xi # cost of transmitting 1 image in mW
    C_ir = (I_sr/R)*xi # cost of transmitting 1 prompt in mW
    E_i = E_d*10**-12*I_s # cost of accessing images from d-ram
    # print(I, E_HWd, C_ir)
    # savings
    savings = C_i - C_ir - E_i - E_HWd
    return savings, (C_ir+E_i+E_HWd)/C_i 


def main():

    generalSavings = getSavings()
    print(generalSavings)
    maxRate = 3000
    rateSavings = np.asarray([getRateSavings(rate*10**3) for rate in range(100,maxRate)])
    # rateSavings = np.asarray(getRateSavings([rate*10**3 for rate in range(100,1000)]))
    thresh = min(range(len(rateSavings[:,0])), key=lambda i: abs(rateSavings[i,0]))
    print(thresh*10**3)
    plt.plot([x*10**3 for x in range(100,maxRate)], rateSavings[:,0], label="Energy saved using prompts")
    plt.vlines(x=(thresh*10**3), ymin=min(min(rateSavings[:,0]),0), ymax=rateSavings[thresh][0], colors=['tab:orange'], ls="--", label="Energy savings threshold")
    plt.xlabel("Datarate")
    plt.ylabel("Energy saving [J]")
    plt.legend()
    plt.savefig("Results/dataRateThreshold.pdf")
    plt.clf()
    plt.plot([x*10**3 for x in range(100,thresh)], rateSavings[100:thresh,1]*100)
    plt.xlabel("Datarate")
    plt.ylabel("Relative energy cost [%]")
    # plt.legend()
    plt.savefig("Results/datarateRelativeCost.pdf")
    plt.clf()

if __name__ == "__main__":
    main()