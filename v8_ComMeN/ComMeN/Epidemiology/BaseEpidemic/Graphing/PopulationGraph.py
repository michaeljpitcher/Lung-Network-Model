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


def draw_population_graph(run_id, compartments, show_total=False, title=None):
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