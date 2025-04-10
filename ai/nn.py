"""A simple neural network implementation."""

from typing import TYPE_CHECKING, Callable, Optional

import numpy as np

if TYPE_CHECKING:
    import numpy.typing as npt

    NDArray = npt.NDArray[np.float64]


def relu(x: "NDArray") -> "NDArray":
    """ReLU activation function - max(0, x)."""
    return np.maximum(0, x)


def softmax(x: "NDArray") -> "NDArray":
    """Softmax activation function - e ^ x_0 / sum(e ^ x_i)."""
    exp_x = np.exp(x - np.max(x))
    return exp_x / np.sum(exp_x)


def he_scale(dim: int) -> "NDArray":
    """He (Kaiming) scale constant - good for scaling values before applying ReLU."""
    return np.sqrt(2.0 / dim)


# Ideally there'll be separate classes for input/dense/output layers and each
# one will be created with just size + activation function (no adjacent layer dimensions)
class DenseLayer:
    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        activation: Callable[["NDArray"], "NDArray"],
        weights: Optional["NDArray"] = None,
        biases: Optional["NDArray"] = None,
    ):
        self.weights = weights or np.random.randn(input_dim, output_dim) * he_scale(
            input_dim
        )
        self.biases = biases or np.zeros(output_dim)
        self.activation = activation

    def forward(self, inputs: "NDArray"):
        values = np.dot(inputs, self.weights) + self.biases
        return self.activation(values)


class NeuralNetwork:
    def __init__(self, *layers: "DenseLayer"):
        self.layers = layers

    def predict(self, inputs: "NDArray"):
        for layer in self.layers:
            inputs = layer.forward(inputs)

        return inputs[0]
