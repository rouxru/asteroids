import random

import numpy as np

from ai.nn import DenseLayer, NeuralNetwork

MUTATION_RATE = 0.1
"""Determines how likely an individual is to mutate."""

MUTATION_STRENGTH = 0.5
"""How much a mutation changes an individual."""


class GeneticGym:
    """
    The ships we'd like to train have multisport cards and can visit this gym to get buff.
    More formally this is a genetic algorithm to train neural networks.
    """

    def __init__(self, population_size: int):
        self.population_size = population_size
        self.population = [self._ship_factory() for _ in range(population_size)]

    def _ship_factory(self) -> "NeuralNetwork":
        """Builds a new random individual - a neural network that's the brain of a ship."""
        from ai.nn import relu, softmax

        return NeuralNetwork(
            DenseLayer(5, 8, activation=relu),
            DenseLayer(8, 8, activation=relu),
            DenseLayer(8, 4, activation=softmax),
        )

    def calc_fitness(self, ship: "NeuralNetwork") -> float:
        """Calculate the fitness of an individual."""
        # let the neural network play the game, fitness will be some combination of score
        # and distance travelled to prevent the ship from camping in the center
        raise NotImplementedError

    def eval_population(self) -> list[float]:
        """Evaluates each individual of the current population."""
        return list(map(self.calc_fitness, self.population))

    def get_mating_pool(self, fitness_scores: list[float]) -> list["NeuralNetwork"]:
        """Selects a part of the population that's fit to breed."""
        sorted_indices = np.argsort(fitness_scores)[::-1]
        num_survivors = self.population_size // 2  # cut the homeless in half
        return [self.population[i] for i in sorted_indices[:num_survivors]]

    def crossover(
        self, parent1: "NeuralNetwork", parent2: "NeuralNetwork"
    ) -> "NeuralNetwork":
        """Crossover two individuals to create a new one."""
        child_layers = []

        for l1, l2 in zip(parent1.layers, parent2.layers):
            weights = (l1.weights + l2.weights) / 2
            biases = (l1.biases + l2.biases) / 2
            new_layer = DenseLayer(
                input_dim=l1.weights.shape[0],
                output_dim=l1.weights.shape[1],
                activation=l1.activation,
                weights=weights.copy(),
                biases=biases.copy(),
            )
            child_layers.append(new_layer)

        return NeuralNetwork(*child_layers)

    def mutate(self, nn: "NeuralNetwork"):
        """Mutates an individual to hopefully make it better or at least a bit different."""
        for layer in nn.layers:
            # mutate weights
            mutation_mask = np.random.rand(*layer.weights.shape) < MUTATION_RATE
            layer.weights += (
                mutation_mask
                * np.random.randn(*layer.weights.shape)
                * MUTATION_STRENGTH
            )

            # mutate biases
            mutation_mask_bias = np.random.rand(*layer.biases.shape) < MUTATION_RATE
            layer.biases += (
                mutation_mask_bias
                * np.random.randn(*layer.biases.shape)
                * MUTATION_STRENGTH
            )

    def next_generation(self):
        """Creates the next population."""
        fitness_scores = self.eval_population()
        parents = self.get_mating_pool(fitness_scores)

        new_population = parents.copy()
        # crossover the population until a fixed population size
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(parents, 2)
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_population.append(child)

        self.population = new_population
        print(f"Max fitness: {max(fitness_scores)}")
