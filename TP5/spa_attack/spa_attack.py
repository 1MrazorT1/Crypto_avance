import numpy as np

def pick_peak_indices(var, n_peaks):
    idx = np.argsort(var)[-n_peaks:]
    return np.sort(idx)

def label_peaks(array, peak_idx):
    n_array = array.shape[0]
    n_peaks = len(peak_idx)
    labels = np.zeros((n_array, n_peaks), dtype=np.int8)
    for j, idx in enumerate(peak_idx):
        vals = array[:, idx]
        med = np.median(vals)
        lab = (vals > med).astype(np.int8)
        mean1 = np.mean(vals[lab == 1]) if np.any(lab == 1) else -np.inf
        mean0 = np.mean(vals[lab == 0]) if np.any(lab == 0) else -np.inf
        # ensure label=1 corresponds to the higher-mean cluster
        if mean0 > mean1:
            lab = 1 - lab
        labels[:, j] = lab
    return labels

def majority_bits(labels):
    counts = np.sum(labels, axis=0)
    bits = (counts > (labels.shape[0] // 2)).astype(np.int8)
    return bits

def bits_to_int(bits, msb_first=True):
    if not msb_first:
        bits = bits[::-1]
    val = 0
    for b in bits:
        val = (val << 1) | int(b)
    return val

def bits_to_bytes(bits, msb_first=True):
    i = bits_to_int(bits, msb_first=msb_first)
    blen = (len(bits) + 7) // 8
    return i.to_bytes(blen, 'big')

def main(path, n_bits=256, msb_first=True):
    array = np.loadtxt(path, delimiter=None)
    n_array, n_samples = array.shape
    array = (array - array.mean(axis=1, keepdims=True)) / (array.std(axis=1, keepdims=True) + 1e-12)

    # Variance across array for each time sample
    var = np.var(array, axis=0)
    # pick peaks (limit by available samples)
    n_pick = min(n_bits, n_samples)
    peak_idx = np.argmax(var)
    print(f"Selected {len(peak_idx)} peak indices (top variance samples). Example first 20:", peak_idx[:20])
    print("Top variances for those indices (first 20):", var[peak_idx][:20])

    # Label each trace at each peak as add (1) or not (0)
    labels = label_peaks(array, peak_idx)
    # Majority vote per bit position
    bits = majority_bits(labels)
    print("Recovered bits length:", len(bits))

    # Convert bits -> integer -> hex
    key_int = bits_to_int(bits, msb_first=msb_first)
    key_hex = hex(key_int)[2:]
    if len(key_hex) % 2:
        key_hex = '0' + key_hex

    print("\nPrivate key (hex):")
    print(key_hex)
    with open("recovered_key_hex.txt", "w") as f:
        f.write(key_hex)
    print("Saved recovered_key_hex.txt")

    # Try to interpret as bytes (strip leading zeros) and print readable portion if any
    try:
        b = bits_to_bytes(bits, msb_first=msb_first)
        b = b.lstrip(b'\x00')
        print("\nAttempted UTF-8 decode of bytes (if meaningful):")
        try:
            print(b.decode('utf-8'))
        except Exception:
            # show first bytes repr if not decodable
            print(repr(b[:200]))
    except Exception as e:
        print("Could not convert bits to bytes:", e)

    print("\nIf output looks wrong: try changing n_bits or try msb_first=False")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recover_from_collected_txt.py collected_data.txt")
        sys.exit(1)
    input_path = sys.argv[1]
    # default is 256 bits (secp256k1). Change if needed.
    main(input_path, n_bits=256, msb_first=True)
