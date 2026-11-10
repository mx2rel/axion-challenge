import math
import numpy as np

q0 = np.array([1,0])
q1 = np.array([0,1])

I = np.array([[1,0],[0,1]])
X = np.array([[0,1], [1,0]])
Z = np.array([[1,0], [0,-1]])
H = 1/math.sqrt(2) * np.array([[1,1], [1,-1]])

def R(ang):
    return np.array([[math.cos(ang/2),- math.sin(ang/2)], [math.sin(ang/2),math.cos(ang/2)]])

CNOT = np.array([[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]])


def measure(toMeasure, measurements=500, display=False):
    probabilities = np.abs(toMeasure) ** 2
    q_count = int(math.log(len(toMeasure), 2))
    labels = [format(i, f"0{q_count}b") for i in range(len(toMeasure))]
    results = np.random.choice(labels, size=measurements, p=probabilities)
    unique, counts = np.unique(results, return_counts=True)
    counts_dict = dict(zip(unique, counts))
    resultsDict = {f"|{label}>": int(counts_dict.get(label, 0)) for label in labels}

    if display:
        return "".join(f"{k}: {v}\n" for k, v in resultsDict.items())
    return resultsDict

stan_H = H @ (H @ q0)
print(f"Wynik Test 1 (H*H|0>):\n{measure(stan_H, measurements=100, display=True)}")

stan_Bella = CNOT @ (np.kron(H,I)@np.kron(q0,q0))
print(f"Wynik Test 2 (Stan Bella):\n{measure(stan_Bella, measurements=1000,display=True)}")