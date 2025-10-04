import numpy as np

from data_Lab5.sbox_aes import sbox
sbox = np.array(sbox)

HW = np.array([bin(i).count("1") for i in range(256)], dtype=np.uint8)

traces = np.load("data_Lab5/traces.npy")
plaintext = np.load("data_Lab5/plaintext.npy")

print("Does len(traces) return 50 ?", len(traces) == 50)
print("Does len(traces[0]) return 9996 ?", len(traces[0]) == 9996)

N, Npoints = traces.shape
trace_means = traces.mean(axis=0)
recovered_key_bytes = []
for byte_idx in range(16):
    Pj = plaintext[:, byte_idx]
    maxcpa = np.zeros(256)
    for k in range(256):
        xored = np.bitwise_xor(Pj, np.uint8(k))
        s_out = sbox[xored]
        Wi_k  = HW[s_out].astype(np.float64)
        Wk_mean = Wi_k.mean()
        sum1 = np.zeros(Npoints, dtype=np.float64)
        sum2 = np.zeros(Npoints, dtype=np.float64)
        sum3 = 0.0
        for i in range(N):
            hdiff_i = Wi_k[i] - Wk_mean
            tdiff_i = traces[i] - trace_means
            sum1 += hdiff_i * tdiff_i
            sum2 += tdiff_i * tdiff_i
            sum3 += hdiff_i * hdiff_i

        denom = np.sqrt(sum3) * np.sqrt(sum2)
        with np.errstate(divide='ignore', invalid='ignore'):
            rk_l = sum1 / denom
            rk_l[np.isnan(rk_l)] = 0.0

        maxcpa[k] = np.max(np.abs(rk_l))

    best_guess = int(np.argmax(maxcpa))
    recovered_key_bytes.append(best_guess)

key_hex = "".join(f"{b:02x}" for b in recovered_key_bytes)
print("\nRecovered key:", key_hex)
