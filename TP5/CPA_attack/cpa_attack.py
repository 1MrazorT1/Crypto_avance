import numpy as np

traces = np.load("data_Lab5/traces.npy")
plaintext = np.load("data_Lab5/plaintext.npy")

print("Does len(traces) return 50 ?", len(traces) == 50)
print("Does len(traces[0]) return 9996 ?", len(traces[0]) == 9996)

from data_Lab5.sbox_aes import sbox
sbox = np.array(sbox)

Hamming_weights = np.array([bin(i).count("1") for i in range(256)])
N, Npoints = traces.shape
trace_means = traces.mean(axis=0)
recovered_key_bytes = []
for index_of_byte in range(16):
    Pj = plaintext[:, index_of_byte]
    maxcpa = np.zeros(256)
    for k in range(256):
        xored = Pj ^ k
        s = sbox[xored]
        Wi_k  = Hamming_weights[s]
        Wk_mean = Wi_k.mean()
        sum1 = np.zeros(Npoints)
        sum2 = np.zeros(Npoints)
        sum3 = 0
        for i in range(N):
            hdiff_i = Wi_k[i] - Wk_mean
            tdiff_i = traces[i] - trace_means
            sum1 += hdiff_i * tdiff_i
            sum2 += tdiff_i * tdiff_i
            sum3 += hdiff_i * hdiff_i
        denom = np.sqrt(sum3) * np.sqrt(sum2)
        rk_l = sum1 / denom
        maxcpa[k] = np.max(np.abs(rk_l))
    greatest_value = int(np.argmax(maxcpa))
    recovered_key_bytes.append(greatest_value)

recovered_key = bytes(recovered_key_bytes).hex()
print("Is the recovered key the same as the one given in the lab ?", recovered_key == "98a90ac6a2bc26493c3be04b113555d4")
