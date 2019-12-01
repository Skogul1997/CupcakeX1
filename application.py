import matplotlib.pyplot as plt
from numpy import array
import numpy as np
from flask import Flask, request

app = Flask(__name__)


def fileread(file):
    data1 = file.readlines()
    data1 = list(map(lambda x: float(x), data1))
    y = array(data1).astype(np.float)
    return(y)


def tonic(l, fs=100.0):
    from scipy.signal import butter, lfilter, freqz  # NOISE CANCELLATION
    order = 2
    cutoff = 30.0

    def butter_lowpass(cutoff, fs, order=2):
        normal_cutoff = cutoff/fs
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(data_b, cutoff, fs, order1=2):
        b, a = butter_lowpass(cutoff, fs, order=order1)
        y = lfilter(b, a, data_b)
        return y

    b, a = butter_lowpass(cutoff, fs, order)
    z = butter_lowpass_filter(l, cutoff, fs, order)

    cutoff_1 = 0.5
    b, a = butter_lowpass(cutoff_1, fs, order)
    b = butter_lowpass_filter(z, cutoff_1, fs, order)
    return (b)


def threshold(b):
    b = b[250::]
    q0 = sum(b)/len(b)
    q1 = q0*0.9
    return (q0, q1)


def stress(l, q0, q1):
    sparse_list = []
    for i in range(len(l)):
        if l[i] <= q1:
            sparse_list.append('2')
        else:
            sparse_list.append('1')
    return(sparse_list)


@app.route("/name", methods=["POST"])
def display():
    return {"status": "Hello"}, 400


@app.route("/calculateStress", methods=["POST"])
def calculate():
    calm = fileread(request.files["calm"])
    other = fileread(request.files["normal"])
    [q0, q1] = threshold(tonic(calm))
    k = tonic(other)
    ant = stress(k, q0, q1)
    return {"result": ant}, 400


if __name__ == "__main__":
    app.run(debug=True)
