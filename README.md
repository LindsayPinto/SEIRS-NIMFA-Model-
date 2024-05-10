# SEIRS-NIMFA-Model

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)


## Installation

To use this project, you'll need to have the following Python libraries installed:

- [Tkinter](https://docs.python.org/3/library/tkinter.html): Python's standard library for Graphical User Interfaces (GUI).
- [Matplotlib](https://matplotlib.org/): Library for 2D plotting.
- [NetworkX](https://networkx.org/): Library for creating, manipulating, and studying complex networks.
- [NumPy](https://numpy.org/): Library for numerical computing in Python.
- [SciPy](https://www.scipy.org/): Library for mathematics, science, and engineering.

You can install these libraries using `pip` with the following commands:

```bash
pip install numpy
pip install matplotlib
pip install networkx
pip install scipy
```

For Tkinter, if you're using Python in a Linux environment, you may need to install it with the following command:

```bash
sudo apt-get install python3-tk
```

## Usage

1. Run the main.py file.
2. A window will open where you can load the corresponding network file you want to analyze. This network should be in JSON format and represented as an adjacency list. (In the 'data' folder, there are some examples of network topologies that can be explored)
3. Adjust the rates as needed.
4. In the first tab named Heatmap, execute the 'run' command to see the heatmap corresponding to the evolution of the nodes if each node is the initial one.
5. In the second tab named Network, you can see the step-by-step evolution of the infection. Also, the evolution of the network and the determined initial device.

## Contribution
Thank you for considering contributing to this project! If you have suggestions, ideas, or want to report a problem, please open an issue. Also, if you'd like to contribute directly with code, you can do so by opening a pull request. Be sure to follow the contribution guidelines and respect the code of conduct.

## License
This project is licensed under the MIT License - see the LICENSE file for more details.

The MIT License is an open-source license that allows people to use, modify, and distribute your software with some restrictions. If you want to provide more information about the license or include more detailed text, you can do so in the LICENSE file in your repository.


