import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# Parameters
E_MUAC = 3.7 # cost of MUAC operation in pJ
E_m = 2*3.7 
E_d = 128*3.7 # cost of d-ram access
E_l = 3.7 # cost of s-ram access
p=64
xi = 108*10**-3 # energy cost of transmitting in mW (108mW)
# xi = 186*3.3*10**-3
CodeRate = 3/4
R = 10**5 # data rate in bps
# R = 300000 * CodeRate

# Discussion:
# The transmit power stated as xi is based on a WPAN (Zigbee chip) which has a very short range (10-100 meters).
# If we instead use WLAN (WiFi), WNAN (Zigbee-NAN), or WWAN (SIGFOX, or LoRa) the power cost will increase as the transmissions must reach further.
# WiFi ZG2100M/ZG2101M: 115 mA at 3.3V
# LoRa Lambda: 18-125 mA at 3.3V
# SIGFOX ATA8520E: 32.7 mA at 3.3V but only 600bps
# WNAN 38 mA at 3.3V. 100 kbps
# There is also the question of which ECC they use. The higher the ECC, the less of the available data rate is used for actual data.
#
# Lets say you are using a smart hunting camera -- it has to be wireless and battery driven, and the ranges of the transmission will be long so it is possible that you would choose something like LoRa.
# Based on the specification of LoRa modem, and a independent test using LoRa (900 MHz CF, 125MHz BW, 4/5 coding rate, spread factor 7), the observed data rate is 600 bps with a transmit power of 80 mA.
#

def getPowerThreshold(cost):
    N_c = 5678366720 # number of MUAC operations
    A_s = 7782400 # number of activations
    N_s = 13172180 # number of weights
    I = 256 # image size in sqrt(pixels) (assumes square image)

    # Cost of using model in d-ram
    E_Ad = 2*E_m*A_s + (E_d*N_c)/(np.sqrt(p))
    E_Wd = E_m*N_s + (E_d*N_c)/np.sqrt(p)
    E_Cd = E_MUAC * (N_c+3*A_s)

    E_HWd = (E_Cd+E_Wd+E_Ad)*10**-12 # cost of using model on 1 image
    I_s = I**2*4.86 # image size in bits
    I_sr = I**2*0.3 # prompt size in bits
    C_i = I_s*cost # cost of transmitting 1 image in mW
    C_ir = I_sr*cost # cost of transmitting 1 prompt in mW
    # C_i = (I_s/dataRate)*transmissionPower # cost of transmitting 1 image in mW
    # C_ir = (I_sr/dataRate)*transmissionPower # cost of transmitting 1 prompt in mW
    E_i = E_d*10**-12*I_s # cost of accessing images from d-ram

    savings = C_i - C_ir - E_i - E_HWd

    return savings


def getSavings_ErasureChannel(prob):
    N_c = 5678366720 # number of MUAC operations
    A_s = 7782400 # number of activations
    N_s = 13172180 # number of weights
    I = 256 # image size in sqrt(pixels) (assumes square image)

    # Cost using model in s-ram
    E_As = 2*E_m*A_s + (E_l*N_c)/(np.sqrt(p))
    E_Ws = E_m*N_s + (E_l*N_c)/np.sqrt(p)
    E_Cs = E_MUAC * (N_c+3*A_s)

    E_HWs = (E_Cs+E_Ws+E_As)*10**-12 # cost of using model on 1 image

    # Cost of using model in d-ram
    E_Ad = 2*E_m*A_s + (E_d*N_c)/(np.sqrt(p))
    E_Wd = E_m*N_s + (E_d*N_c)/np.sqrt(p)
    E_Cd = E_MUAC * (N_c+3*A_s)

    E_HWd = (E_Cd+E_Wd+E_Ad)*10**-12 # cost of using model on 1 image

    I_s = I**2*4.86 # image size in bits
    I_sr = I**2*0.3 # prompt size in bits
    C_i = (I_s/R)*xi # cost of transmitting 1 image in mW
    C_ir = (I_sr/R)*xi # cost of transmitting 1 prompt in mW
    E_i = E_d*10**-12*I_s # cost of accessing images from d-ram

    numbTransmissions = 1/(1-prob) # expected number of attempts until successful transmission given failure prob

    # Savings
    savings = (C_i*numbTransmissions) - (C_ir*numbTransmissions) - E_i - E_HWd
    return savings, ((C_ir*numbTransmissions)+E_i+E_HWd)/(C_i*numbTransmissions) 


def getSavings_threshold(P_i):
    """
    Get the savings when sending only a subset of images (the images with a high enough similarity measure).
    """

    N_c = 117000000 # number of MUAC operations for inference model
    A_s = 4309000 # number of activations for inference model
    N_s = 976000 # number of weights for inference model
    N_c2 = 5678366720 # number of MUAC operations for compression model
    A_s2 = 7782400 # number of activations for compression model
    N_s2 = 13172180 # number of weights for compression model
    I = 256 # image size in sqrt(pixels) (assumes square image)

    # Cost using model in s-ram
    E_As = 2*E_m*A_s + (E_l*N_c)/(np.sqrt(p))
    E_Ws = E_m*N_s + (E_l*N_c)/np.sqrt(p)
    E_Cs = E_MUAC * (N_c+3*A_s)

    E_HWs = (E_Cs+E_Ws+E_As)*10**-12 # cost of using model on 1 image

    # Cost of using inference model in d-ram
    E_Ad = 2*E_m*A_s + (E_d*N_c)/(np.sqrt(p))
    E_Wd = E_m*N_s + (E_d*N_c)/np.sqrt(p)
    E_Cd = E_MUAC * (N_c+3*A_s)

    # Cost of using compression model in d-ram
    E_Ad2 = 2*E_m*A_s2 + (E_d*N_c2)/(np.sqrt(p))
    E_Wd2 = E_m*N_s2 + (E_d*N_c2)/np.sqrt(p)
    E_Cd2 = E_MUAC * (N_c2+3*A_s2)

    E_HWd = (E_Cd+E_Wd+E_Ad)*10**-12 # cost of using inference model on 1 image
    E_HWd2 = (E_Cd2+E_Wd2+E_Ad2)*10**-12 # cost of using compression model on 1 image

    I_s = I**2*4.86 # image size in bits
    I_sr = I**2*0.3 # prompt size in bits

    C_i = (I_sr/R)*xi + E_HWd2 # cost of transmitting 1 prompt in mW
    C_ir = C_i * (1-P_i)
    E_i = E_d*10**-12*I_s # cost of accessing images from d-ram

    savings = C_i - C_ir - E_HWd
    return savings, (C_ir+E_HWd)/C_i 


def getSavings(I=256):
    # N_c = 5678366720 # number of MUAC operations
    # A_s = 7782400 # number of activations
    # N_s = 13172180 # number of weights

    # small model
    N_c = 477388800 # number of MUAC operations
    A_s = 3542400 # number of activations
    N_s = 18456 # number of weights

    # Cost using model in s-ram
    E_As = 2*E_m*A_s + (E_l*N_c)/(np.sqrt(p))
    E_Ws = E_m*N_s + (E_l*N_c)/np.sqrt(p)
    E_Cs = E_MUAC * (N_c+3*A_s)

    E_HWs = (E_Cs+E_Ws+E_As)*10**-12 # cost of using model on 1 image

    # Cost of using model in d-ram
    E_Ad = 2*E_m*A_s + (E_d*N_c)/(np.sqrt(p))
    E_Wd = E_m*N_s + (E_d*N_c)/np.sqrt(p)
    E_Cd = E_MUAC * (N_c+3*A_s)

    E_HWd = (E_Cd+E_Wd+E_Ad)*10**-12 # cost of using model on 1 image
    
    I_s = I**2*4.86 # image size in bits
    I_sr = I**2*0.3 # prompt size in bits
    C_i = (I_s/R)*xi # cost of transmitting 1 image in mW
    C_ir = (I_sr/R)*xi # cost of transmitting 1 prompt in mW
    E_i = E_d*10**-12*I_s # cost of accessing images from d-ram

    # Savings
    savings = C_i - C_ir - E_i - E_HWd
    return savings, (C_ir+E_i+E_HWd)/C_i 


def main():
    maxImgSize = 512
    savings = np.asarray([getSavings(imgSize) for imgSize in range(1,maxImgSize)])
    # realtiveSavings = 1-(savings[400][1])
    # print(realtiveSavings)
    # exit()
    thresh = min(range(len(savings[:,0])), key=lambda i: abs(savings[i,0]))
    print(thresh)
    
    plt.plot([x for x in range(1,maxImgSize)], savings[:,0], label="Energy saved using prompts")
    
    plt.vlines(x=thresh, ymin=min(savings[:,0]), ymax=savings[thresh][0], colors=['tab:orange'], ls="--", label="Energy savings threshold")
    
    plt.xlabel("Pixels per dimension")
    plt.ylabel("Energy saving [J]")
    
    plt.legend()
    
    plt.savefig("results/HiFiC/imageSizeThreshold.pdf")

    plt.clf()

    maxImgSize = 1024
    savings = np.asarray([getSavings(imgSize) for imgSize in range(1,maxImgSize)])
    
    plt.plot([x for x in range(374,maxImgSize)], savings[373:,1]*100)
    
    plt.xlabel("Pixels per dimension")
    plt.ylabel("Relative energy cost [%]")
    
    plt.savefig("results/HiFiC/imageSizeRelativeCost.pdf")

    plt.clf()

    savings_threshold = np.asarray([getSavings_threshold(prob/20000) for prob in range(1, 20000)])
    thresh = min(range(len(savings_threshold[:,0])), key=lambda i: abs(savings_threshold[i,0]))
    print(thresh/20000)
    
    plt.plot([100-x/200 for x in range(1,20000)], savings_threshold[:,0], label="Energy saved using prompts")
    plt.vlines(x=100-thresh/200, ymin=min(savings_threshold[:,0]), ymax=savings_threshold[thresh][0], colors=['tab:orange'], ls="--", label="Energy savings threshold")
    
    plt.xlabel("Percentage of prompts transmitted")
    plt.ylabel("Energy saving [J]")
    
    plt.legend()

    plt.savefig("results/HiFiC/probThreshold.pdf")

    plt.clf()
    
    plt.plot([100-x/200 for x in range(thresh,20000)], savings_threshold[thresh-1:,1]*100)
    
    plt.xlabel("Percentage of prompts transmitted")
    plt.ylabel("Relative energy cost [%]")
    # plt.legend()
    plt.savefig("results/HiFiC/probRelativeCost.pdf")

    plt.clf()
    
    savings_erasure = np.asarray([getSavings_ErasureChannel(prob/10000) for prob in range(1, 8000)])
    thresh = min(range(len(savings_erasure[:,0])), key=lambda i: abs(savings_erasure[i,0]))
    print(thresh/10000)

    plt.plot([x/100 for x in range(1,8000)], savings_erasure[:,0], label="Energy saved using prompts")
    # plt.vlines(x=thresh/100, ymin=min(savings_erasure[:,0]), ymax=savings_erasure[thresh][0], colors=['tab:orange'], ls="--", label="Energy savings threshold")
    
    plt.xlabel("Erasure probability")
    plt.ylabel("Energy saving [J]")
    # plt.legend()
    
    plt.savefig("results/HiFiC/erasureProbThreshold.pdf")

    plt.clf()
    
    plt.plot([x/100 for x in range(1,8000)], savings_erasure[:,1]*100)
    
    plt.xlabel("Erasure probability")
    plt.ylabel("Relative energy cost [%]")
    
    # plt.legend()
    plt.savefig("results/HiFiC/erasureProbRelativeCost.pdf")

    plt.clf()
    
    xmin = 100
    xmax = 500
    ymin = 500
    ymax = 3000

    savings_power_thresh = getPowerThreshold(np.asarray([[(power*10**-3) / (rate*10**2) for power in range(xmin, xmax)] for rate in range(ymin,ymax)]))
    # savings_power_thresh = np.asarray([[getPowerThreshold(power*10**-3, rate*10**2) for power in range(1, 10000)] for rate in range(1,10000)])
    print(savings_power_thresh[-1,0])

    divnorm=colors.TwoSlopeNorm(vmin=np.min(savings_power_thresh), vcenter=0., vmax=np.max(savings_power_thresh))
    pos= plt.imshow(savings_power_thresh, origin="lower", extent=[xmin, xmax, (ymin*10**2)*10**-3, (ymax*10**2)*10**-3], aspect="auto", cmap="seismic", norm=divnorm)
    
    plt.colorbar(pos)
    
    plt.xlabel("Transmit power [mW]")
    plt.ylabel("Data rate [kbps]")
    
    plt.savefig("results/HiFiC/savings_power_thresh.pdf")

if __name__ == "__main__":
    main()