import numpy as np
import matplotlib.pyplot as plt


def getSavings(I=256):
    E_MUAC = 2.7 # cost of MUAC operation in pJ
    E_m = 2*3.7 
    E_d = 128*3.7 # cost of d-ram access
    E_l = 3.7 # cost of s-ram access
    N_c = 5678366720 # number of MUAC operations
    A_s = 7782400 # number of activations
    N_s = 13172180 # number of weights
    p=64

    # cost using model in s-ram
    E_As = 2*E_m*A_s + (E_l*N_c)/(np.sqrt(p))
    E_Ws = E_m*N_s + (E_l*N_c)/np.sqrt(p)
    E_Cs = E_MUAC * (N_c+3*A_s)

    E_HWs = (E_Cs+E_Ws+E_As)*10**-12 # cost of using model on 100 images

    # cost of using model in d-ram
    E_Ad = 2*E_m*A_s + (E_d*N_c)/(np.sqrt(p))
    E_Wd = E_m*N_s + (E_d*N_c)/np.sqrt(p)
    E_Cd = E_MUAC * (N_c+3*A_s)

    E_HWd = (E_Cd+E_Wd+E_Ad)*10**-12 # cost of using model on 100 images


    xi = 108*10**-3 # energy cost of transmitting in mW
    R = 10**5 # data rate in bps
    I_s = I**2*4.86 # image size in bits
    I_sr = I**2*0.3 # prompt size in bits
    C_i = (I_s/R)*xi # cost of transmitting 100 images in mW
    C_ir = (I_sr/R)*xi # cost of transmitting 100 prompts in mW
    E_i = E_d*10**-12*I_s # cost of accessing images from d-ram

    # savings
    savings = C_i - C_ir - E_i - E_HWd
    return savings

def main():
    maxImgSize = 512
    savings = [getSavings(imgSize) for imgSize in range(maxImgSize)]
    thresh = min(range(len(savings)), key=lambda i: abs(savings[i]))
    print(thresh)
    plt.plot([x for x in range(maxImgSize)], savings, label="Energy saved using prompts")
    plt.vlines(x=thresh, ymin=min(savings), ymax=savings[thresh], colors=['tab:orange'], ls="--", label="Energy savings threshold")
    plt.xlabel("Pixels per dimension")
    plt.ylabel("Energy saving [J]")
    plt.legend()
    plt.savefig("imageSizeThreshold.pdf")

    


if __name__ == "__main__":
    main()