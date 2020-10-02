#############################################################
# @copyright Copyright (c) 2020 All Right Reserved, b<>com http://www.b-com.com/
#
# BER/SER of LoRa signal
# Author: Vincent Savaux, IRT b<>com, Rennes
# email: vincent.savaux@b-com.com
# date: 2020-08-21

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, see <http://www.gnu.org/lice
#############################################################

#############################################################
# Import some external function
#############################################################
import json
import logging
import gmpy2
from gmpy2 import mpfr
from scipy.special import comb

#############################################################
# Set precision
# at least 150 bits for SF7, up to 4000 bits for SF12
#############################################################

gmpy2.get_context().precision = 300

def main():
    # Set/initialize parameters
    sf = 7  # Spreading factor
    n_fft = 2**sf  # Corresponding FFT size
    n_hamming = 7 # Hamming codeword length
    npl = 32 # payload length in LoRa symbols
    snr_start = -1*(2*sf+1)-4  # low-bound of SNR range
    snr_end = snr_start + 30  # upper-bound of SNR range
    p_error_swer = []  # list containing the sinc word error rate
    p_error_fer = []  # list containing the frame error rate
    p_error_her = []  # list containing the header error rate

    print(snr_start,snr_end)

    for snr in range(snr_start, snr_end+1):
        # print(snr)
        sig2 = mpfr(10**(-snr/10.0))  # Noise variance
        # snr_lin = mpfr(1*10**(snr/10.0))
        error_swer0 = mpfr(0.0)  # Initialise error
        # error_nochan = mpfr(0.0) # Initialise error
        for k in range(1, n_fft):
            nchoosek = mpfr(comb(n_fft-1, k, exact=True))
            #################################################
            # Sync word Error Rate over AWGN Channel
            #################################################
            error_swer0 = error_swer0 - mpfr(nchoosek * (-1)**k / (k+1)) \
            * mpfr(gmpy2.exp(-k*n_fft/((k+1)*sig2)))
            #################################################
            # Symbol Error Rate over Rayleigh Channel
            #################################################
            # error_swer0 = error_swer0 - mpfr(nchoosek * (-1)**k*sig2 /
            #                      ((k+1)*sig2 + k*n_fft*1))
            # print(nchoosek)
        error_swer0 = mpfr(error_swer0, 32)  # Limit precision for printing/saving
        p_error_swer.append(1-(1-float(error_swer0))**2)  # sync word error rate

        pb = (2**(sf-1))/(2**sf - 1)*mpfr(error_swer0, 32) # bit error rate
        pcw = 1-(1-pb)**n_hamming - n_hamming*pb*(1-pb)**(n_hamming-1) # codeword error rate
        pcw_header = 1-(1-pb)**8 - 8*pb*(1-pb)**(8-1) # codeword error rate for header
        error_fer = 1-(1-pcw)**(npl*sf/n_hamming) # payload error rate
        error_her = 1-(1-pcw_header)**(sf) # header error rate
        p_error_fer.append(float(error_fer))
        p_error_her.append(float(error_her))
    print(p_error_swer)
    print(p_error_fer)
    print(p_error_her)
    file = open("swer_sf"+str(sf)+"_h"+str(n_hamming)+"_npl"+str(npl)+".txt", "w")
    file.write(json.dumps(p_error_swer))
    file.close()
    file = open("fer_sf"+str(sf)+"_h"+str(n_hamming)+"_npl"+str(npl)+".txt", "w")
    file.write(json.dumps(p_error_fer))
    file.close()
    file = open("her_sf"+str(sf)+"_h"+str(n_hamming)+"_npl"+str(npl)+".txt", "w")
    file.write(json.dumps(p_error_her))
    file.close()


if __name__ == "__main__":
    main()
