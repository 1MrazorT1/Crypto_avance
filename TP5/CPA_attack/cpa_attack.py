import numpy as np

traces = np.load("data_Lab5/traces.npy")
plaintext = np.load("data_Lab5/plaintext.npy")

print("Does len(traces) return 50 ?", len(traces) == 50)
print("Does len(traces[0]) return 9996 ?", len(traces[0]) == 9996)

#