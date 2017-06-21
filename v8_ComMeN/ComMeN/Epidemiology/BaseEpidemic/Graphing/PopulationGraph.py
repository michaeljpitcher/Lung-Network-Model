#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import matplotlib.pyplot as plt
import csv
import math

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def draw_single_population_graph(run_id, compartments, show_total=False, title=None):
    csv_file = open(str(run_id) + ".csv", 'r')
    csv_reader = csv.DictReader(csv_file)
    time = []
    data = {}
    for compartment in compartments:
        data[compartment] = []
    for row in csv_reader:
        time.append(float(row['timestep']))
        for compartment in compartments:
            data[compartment].append(float(row[compartment]))

    # Colours set to (sort of) mimic MATLAB
    fig, ax = plt.subplots()
    ax.set_color_cycle(['blue', 'orangered', 'goldenrod', 'purple', 'green', 'cyan'])

    for compartment in compartments:
        plt.plot(time, data[compartment])
    if show_total:
        total = []
        for n in range(0, len(time)):
            total.append(sum([data[compartment][n] for compartment in compartments]))
        plt.plot(time, total)
        plt.legend(compartments + ['total'])
    else:
        plt.legend(compartments)
    if title:
        plt.title(str(title))
    # x1, x2, y1, y2 = plt.axis()
    # plt.axis((0, math.ceil(max(time)), 0, ))
    plt.show()


def draw_multi_population_graph(run_id, compartments, title=None, axis=None):
    # Colours set to (sort of) mimic MATLAB
    fig, ax = plt.subplots()
    ax.set_color_cycle(['blue', 'orangered', 'goldenrod', 'purple', 'green', 'cyan', 'black', 'grey'])

    print "reading data...."
    csv_file = open(str(run_id) + ".csv", 'r')
    csv_reader = csv.DictReader(csv_file)
    data = {}
    for row in csv_reader:
        node_id = int(row['node_id'])
        if node_id not in data.keys():
            data[node_id] = []
        data[node_id].append(row)

    time = [row['timestep'] for row in data[1]]

    legend_labels = []

    print "drawing graph..."
    for node_id in data:
        for compartment in compartments:
            compartment_data = [row[compartment] for row in data[node_id]]
            plt.plot(time, compartment_data)
            legend_labels.append(compartment + '_' + str(node_id))
    plt.legend(legend_labels)
    if title:
        plt.title(str(title))
    if axis:
        plt.axis((axis[0], axis[1], axis[2], axis[3]))
    plt.show()

def plot_incidence_rates(incidence):

    for cause in incidence.keys():
        data = incidence[cause]
        timesteps = sorted(data.keys())
        time = []
        values = []
        for t in timesteps:
            time.append(t)
            values.append(data[t])
        plt.plot(time, values)
    plt.show()
