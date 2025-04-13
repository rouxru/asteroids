import random
from typing import Optional

import numpy as np

from ai.nn import DenseLayer, NeuralNetwork

SAVE_PATH = "./ai/best_ship.pkl"

MUTATION_RATE = 0.1
"""Determines how likely an individual is to mutate."""

MUTATION_STRENGTH = 0.5
"""How much a mutation changes an individual."""


class GeneticGym:
    """
    The ships we'd like to train have multisport cards and can visit this gym to get buff.
    More formally this is a genetic algorithm to train neural networks.
    """

    _ELITES_COUNT = 2
    """
    The best individuals of a population are called 'elites', it might be useful to keep
    their genes for the next population.
    """

    _mutation_rate: Optional[float] = None
    _mutation_strength: Optional[float] = None

    def __init__(self, population_size: int):
        self.gen_num = 0
        self.population_size = population_size
        self.population = [self._ship_factory() for _ in range(population_size)]

    # annealing mutation rates for diversity early and refinement later
    @property
    def mutation_rate(self) -> float:
        """Determines how likely an individual is to mutate."""
        if not self._mutation_rate:
            self._mutation_rate = max(0.01, MUTATION_RATE * 0.99**self.gen_num)
        return self._mutation_rate

    @property
    def mutation_strength(self) -> float:
        """How much a mutation changes an individual."""
        if not self._mutation_strength:
            self._mutation_strength = max(0.01, MUTATION_STRENGTH * 0.98**self.gen_num)
        return self._mutation_strength

    def _ship_factory(self) -> "NeuralNetwork":
        """Builds a new random individual - a neural network that's the brain of a ship."""
        from ai.nn import DenseLayer, relu, softmax

        return NeuralNetwork(
            DenseLayer(5, 12, activation=relu),
            DenseLayer(12, 8, activation=relu),
            DenseLayer(8, 4, activation=softmax),
        )

    def calc_fitness(self, ship: "NeuralNetwork") -> float:
        """Calculate the fitness of an individual."""
        from main import Game

        game = Game()
        i, score = game.sim(ship)

        return score + i / 10

    def eval_population(self) -> list[float]:
        """Evaluates each individual of the current population."""
        return list(map(self.calc_fitness, self.population))

    def get_mating_pool(
        self, fitness_scores: list[float], tournament_k: int = 3
    ) -> list["NeuralNetwork"]:
        """Selects a part of the population that's fit to breed."""
        sorted_indices = np.argsort(fitness_scores)[::-1]
        elites = [self.population[i] for i in sorted_indices[: self._ELITES_COUNT]]

        # 'tournament' selection
        selected = elites.copy()
        while len(selected) < self.population_size // 2:
            contenders = random.sample(range(self.population_size), tournament_k)
            best = max(contenders, key=lambda idx: fitness_scores[idx])
            if fitness_scores[best]:
                selected.append(self.population[best])

        return selected

    def crossover(
        self, parent1: "NeuralNetwork", parent2: "NeuralNetwork"
    ) -> "NeuralNetwork":
        """Crossover two individuals to create a new one."""
        child_layers = []

        for l1, l2 in zip(parent1.layers, parent2.layers):
            mask = np.random.rand(*l1.weights.shape) < 0.5
            weights = (
                np.where(mask, l1.weights, l2.weights)
                + np.random.randn(*l1.weights.shape) * 0.01
            )
            mask = np.random.rand(*l1.biases.shape) < 0.5
            biases = (
                np.where(mask, l1.biases, l2.biases)
                + np.random.randn(*l1.biases.shape) * 0.01
            )
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
            mutation_mask = np.random.rand(*layer.weights.shape) < self.mutation_rate
            layer.weights += (
                mutation_mask
                * np.random.randn(*layer.weights.shape)
                * self.mutation_strength
            )

            # mutate biases
            mutation_mask_bias = (
                np.random.rand(*layer.biases.shape) < self.mutation_rate
            )
            layer.biases += (
                mutation_mask_bias
                * np.random.randn(*layer.biases.shape)
                * self.mutation_strength
            )

    def next_generation(self) -> tuple[float, float]:
        """Creates the next population."""
        fitness_scores = self.eval_population()
        parents = self.get_mating_pool(fitness_scores)

        new_population = parents[: self._ELITES_COUNT].copy()
        # crossover the population until a fixed population size
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(parents, 2)
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_population.append(child)

        self.population = new_population
        self.gen_num += 1
        self._mutation_rate = self._mutation_strength = None
        return (max(fitness_scores), float(np.mean(fitness_scores)))

    def train(
        self,
        generations: int = 100,
        *,
        save_result: bool = False,
        display_champion: bool = True,
    ):
        for i in range(generations):
            max_fitness, avg_fitness = self.next_generation()
            print(
                f"gen = {self.gen_num}, max_fitness = {max_fitness}, avg_fitness = {avg_fitness}"
            )

        champion = self.population[0]

        if save_result:
            import pickle

            with open(SAVE_PATH, "wb") as f:
                pickle.dump(champion, f)

        if display_champion:
            from main import Game

            input("Done, press ENTER to start the simulation.")
            game = Game()
            game.start(ship_ai=self.population[0])


if __name__ == "__main__":
    GeneticGym(population_size=100).train(generations=50, save_result=True)
