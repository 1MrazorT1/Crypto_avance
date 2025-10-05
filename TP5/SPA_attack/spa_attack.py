import numpy as np

traces = np.array(eval(open("collected_data.txt", "r").read()))
mean = traces.mean(axis=0)
threshold = mean.mean()
bits = (mean >= threshold).astype(int)
for order in ("msb", "lsb"):
    if order == "msb":
        b = bits
    else:
        b = bits[::-1] #reverrsing bits
    bits = "".join(map(str, b)).lstrip("0") #removing zeros in the beginning
    private_key = int(bits, 2)
    flag = private_key.to_bytes((private_key.bit_length() + 7)//8, "big")
    if "crypto{" in flag:
        print("Flag found:", flag)
