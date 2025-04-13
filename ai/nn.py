"""A simple neural network implementation."""

from typing import TYPE_CHECKING, Callable, Optional, Union

import numpy as np

from constants import SCREEN_HEIGHT, SCREEN_WIDTH

if TYPE_CHECKING:
    import numpy.typing as npt

    from game_state import GameState

    NDArray = npt.NDArray[np.float64]


SCREEN_DIAGONAL = np.sqrt(SCREEN_HEIGHT**2 + SCREEN_WIDTH**2)


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
        self.weights = (
            weights
            if weights is not None
            else np.random.randn(input_dim, output_dim) * he_scale(input_dim)
        )
        self.biases = biases if biases is not None else np.zeros(output_dim)
        self.activation = activation

    def forward(self, inputs: "NDArray"):
        values = np.dot(inputs, self.weights) + self.biases
        return self.activation(values)


class NeuralNetwork:
    def __init__(self, *layers: "DenseLayer"):
        self.layers = layers

    def predict(self, inputs: Union["NDArray", "GameState"]):
        """Calculate NN output."""
        # parse game state to inputs for the NN
        if not isinstance(inputs, np.ndarray):
            inputs = self.get_inputs(inputs)

        for layer in self.layers:
            inputs = layer.forward(inputs)

        return np.argmax(inputs)

    @staticmethod
    def get_inputs(game_state: "GameState") -> "NDArray":
        """Gets the NN inputs from game state."""
        inputs = []

        inputs.append((game_state.ship_angle - 180) / 180)
        inputs.append(game_state.asteroid_dist / SCREEN_DIAGONAL)
        inputs.append((game_state.asteroid_angle - 180) / 180)
        inputs.append(game_state.asteroid_relative_velocity.x / SCREEN_WIDTH)
        inputs.append(game_state.asteroid_relative_velocity.y / SCREEN_HEIGHT)

        return np.array(inputs)
