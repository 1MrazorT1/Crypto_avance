import json

with open("collected_data.txt") as f:
    data = json.load(f)
n_traces, n_steps = len(data), len(data[0])
