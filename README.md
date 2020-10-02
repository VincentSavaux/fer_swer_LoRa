# fer_swer_LoRa
## General Description

The script ber_LoRa returns the theoretical sync word, header, payload, and frame error rate (FER) that can be achieved by a LoRa signal over Rayleigh and Rice channels. The error rate values are given in function of the SNR in the range *snr_start* and *snr_end*. 

The theoretical results have been obtained from the following references: 

O. Afisiadis, A. Burg, and A. Balatsoukas-Stimmingy "*Coded LoRa Frame Error Rate Analysis*", ArXiv, arXiv:1911.10245v1 [eess.SP] 22 Nov 2019

C. F. Dias, E. R. de Lima, and G. Fraidenraich, “*Bit Error Rate Closed-
Form Expressions for LoRa Systems under Nakagami and Rice Fading
Channels*,” Sensors, vol. 19, no. 20, pp. 1 – 11, October 2019. 

Computing the error rate requires arbritary precision floating point, up to hundreds or thousands of bits, which can be obtained by using the package *gmpy2*. 
