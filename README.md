# DevInterp

[![PyPI version](https://badge.fury.io/py/devinterp.svg)](https://badge.fury.io/py/devinterp) ![Python version](https://img.shields.io/pypi/pyversions/devinterp) ![Contributors](https://img.shields.io/github/contributors/timaeus-research/devinterp)



## A Python Library for Developmental Interpretability Research

DevInterp is a python library for conducting research on developmental interpretability, a novel AI safety research agenda rooted in Singular Learning Theory (SLT). DevInterp proposes tools for detecting, locating, and ultimately _controlling_ the development of structure over training.

[Read more about developmental interpretability](https://www.lesswrong.com/posts/TjaeCWvLZtEDAS5Ex/towards-developmental-interpretability).

> :warning: This library is still in early development. Don't expect things to work on a first attempt. We are actively working on improving the library and adding new features. If you have any questions or suggestions, please feel free to open an issue or submit a pull request.

## Installation

To install `devinterp`, simply run:

```bash
pip install devinterp
```

**Requirements**: Python 3.9 or higher.

## Getting Started

To see DevInterp in action, check out our example notebooks:


- [Introduction](https://www.github.com/timaeus-research/devinterp/examples/introduction.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/timaeus-research/devinterp/examples/introduction.ipynb)
- [Normal Crossing Demo](https://www.github.com/timaeus-research/devinterp/examples/normal_crossing.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/timaeus-research/devinterp/examples/normal_crossing.ipynb)
- [MNIST Demo](https://www.github.com/timaeus-research/devinterp/examples/mnist.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/timaeus-research/devinterp/examples/mnist.ipynb)
- [Deep Linear Networks](https://www.github.com/timaeus-research/devinterp/examples/dlns.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/timaeus-research/devinterp/examples/dlns.ipynb)
- [Toy Models of Superposition](https://www.github.com/timaeus-research/devinterp/examples/tms.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/timaeus-research/devinterp/examples/tms.ipynb)


### Minimal Example

```python
from devinterp.slt import estimate_learning_coeff_with_summary
from devinterp.optim import SGLD

# Assuming you have a PyTorch Module and DataLoader
learning_coeff = estimate_learning_coeff(model, trainloader, ...)

# If you want to see mean, std, and learning coeff estimate per chain
learning_coeff_summary = estimate_learning_coeff_with_summary(model, trainloader, ...)

```

## Features

- Estimate the learning coefficient.
  - Supported optimizers: 
    - [`SGLD`](https://www.github.com/timaeus-research/devinterp/src/devinterp/optim/sgld.py)
    - [`SGNHT`](https://www.github.com/timaeus-research/devinterp/src/devinterp/optim/sgnht.py)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on how to contribute.
