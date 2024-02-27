import numpy as np
import matplotlib.pyplot as plt


E_MUAC = 3.7 # cost of MUAC operation in pJ
E_m = 2*3.7 
E_d = 128*3.7 # cost of d-ram access
E_l = 3.7 # cost of s-ram access
p=64
xi = 108*10**-3 # energy cost of transmitting in mW
R = 10**5 # data rate in bps


def getSavings_ErasureChannel(prob):
    N_c = 5678366720 # number of MUAC operations
    A_s = 7782400 # number of activations
    N_s = 13172180 # number of weights
    I = 400 # image size in sqrt(pixels) (assumes square image)

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

    I_s = I**2*4.86 # image size in bits
    I_sr = I**2*0.3 # prompt size in bits
    C_i = (I_s/R)*xi # cost of transmitting 1 image in mW
    C_ir = (I_sr/R)*xi # cost of transmitting 1 prompt in mW
    E_i = E_d*10**-12*I_s # cost of accessing images from d-ram

    numbTransmissions = 1/(1-prob) # expected number of attempts until successful transmission given failure prob


    # savings
    savings = (C_i*numbTransmissions) - (C_ir*numbTransmissions) - E_i - E_HWd
    return savings, ((C_ir*numbTransmissions)+E_i+E_HWd)/(C_i*numbTransmissions) 


def getSavings_threshold(P_i):
    # get the savings when sending only a subset of images (the images with a high enough similarity measure)
    N_c = 117000000 # number of MUAC operations
    A_s = 4309000 # number of activations
    N_s = 976000 # number of weights 

    I = 256 # image size in sqrt(pixels) (assumes square image)

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

    I_s = I**2*4.86 # image size in bits
    I_sr = I**2*0.3 # prompt size in bits

    C_i = (I_sr/R)*xi # cost of transmitting 1 prompt in mW
    C_ir = C_i * (1-P_i)
    E_i = E_d*10**-12*I_s # cost of accessing images from d-ram

    savings = C_i - C_ir - E_HWd
    return savings, (C_ir+E_HWd)/C_i 


def getSavings(I=256):
    N_c = 5678366720 # number of MUAC operations
    A_s = 7782400 # number of activations
    N_s = 13172180 # number of weights

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

    I_s = I**2*4.86 # image size in bits
    I_sr = I**2*0.3 # prompt size in bits
    C_i = (I_s/R)*xi # cost of transmitting 1 image in mW
    C_ir = (I_sr/R)*xi # cost of transmitting 1 prompt in mW
    E_i = E_d*10**-12*I_s # cost of accessing images from d-ram

    # savings
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
    plt.savefig("Results/imageSizeThreshold.pdf")

    maxImgSize = 1024
    savings = np.asarray([getSavings(imgSize) for imgSize in range(1,maxImgSize)])
    plt.clf()
    plt.plot([x for x in range(374,maxImgSize)], savings[373:,1]*100)
    plt.xlabel("Pixels per dimension")
    plt.ylabel("Relative energy cost [%]")
    # plt.legend()
    plt.savefig("Results/imageSizeRelativeCost.pdf")
    plt.clf()


    savings_threshold = np.asarray([getSavings_threshold(prob/20000) for prob in range(1, 20000)])
    thresh = min(range(len(savings_threshold[:,0])), key=lambda i: abs(savings_threshold[i,0]))
    print(thresh/20000)
    plt.plot([100-x/200 for x in range(1,20000)], savings_threshold[:,0], label="Energy saved using prompts")
    plt.vlines(x=100-thresh/200, ymin=min(savings_threshold[:,0]), ymax=savings_threshold[thresh][0], colors=['tab:orange'], ls="--", label="Energy savings threshold")
    plt.xlabel("Percentage of prompts transmitted")
    plt.ylabel("Energy saving [J]")
    plt.legend()
    plt.savefig("Results/probThreshold.pdf")

    plt.clf()
    plt.plot([100-x/200 for x in range(thresh,20000)], savings_threshold[thresh-1:,1]*100)
    plt.xlabel("Percentage of prompts transmitted")
    plt.ylabel("Relative energy cost [%]")
    # plt.legend()
    plt.savefig("Results/probRelativeCost.pdf")


    plt.clf()
    savings_erasure = np.asarray([getSavings_ErasureChannel(prob/10000) for prob in range(1, 8000)])
    thresh = min(range(len(savings_erasure[:,0])), key=lambda i: abs(savings_erasure[i,0]))
    print(thresh/10000)
    plt.plot([x/100 for x in range(1,8000)], savings_erasure[:,0], label="Energy saved using prompts")
    # plt.vlines(x=thresh/100, ymin=min(savings_erasure[:,0]), ymax=savings_erasure[thresh][0], colors=['tab:orange'], ls="--", label="Energy savings threshold")
    plt.xlabel("Erasure probability")
    plt.ylabel("Energy saving [J]")
    # plt.legend()
    plt.savefig("Results/erasureProbThreshold.pdf")

    plt.clf()
    plt.plot([x/100 for x in range(1,8000)], savings_erasure[:,1]*100)
    plt.xlabel("Erasure probability")
    plt.ylabel("Relative energy cost [%]")
    # plt.legend()
    plt.savefig("Results/erasureProbRelativeCost.pdf")

if __name__ == "__main__":
    main()