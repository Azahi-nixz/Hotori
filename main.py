
import random

secret_text = "Hello World My name is Azahi"

# Possible genes (characters)
pool = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ")

# original parents
gen1_1 = "gbdhsawUfsag tradHjoac bgtra"
gen1_2 = "smAha aZsafasdjeyadgev csHwe"

# Genetic algorithm settings
POPULATION_SIZE = 100
TOURNAMENT_SIZE = 5
MAX_REPRODUCTIONS = 100_000

# Approximately one mutation event per child on average
MUTATION_RATE = 1 / max(1, len(secret_text))


# Make parents the same length as the target
def normalize_parent(parent):
    genes = list(parent[:len(secret_text)])

    while len(genes) < len(secret_text):
        genes.append(random.choice(pool))

    return "".join(genes)


# Measure how many characters match in the correct positions
def fitness(candidate):
    return sum(
        a == b
        for a, b in zip(candidate, secret_text)
    )


# Create a random candidate
def random_candidate():
    return "".join(
        random.choice(pool)
        for _ in secret_text
    )


# Select a parent using a small competition
def select_parent(population):
    contestants = random.sample(
        population,
        min(TOURNAMENT_SIZE, len(population))
    )

    return max(contestants, key=fitness)


# Combine two parents to create a child
def crossover(parent_a, parent_b):
    child = []

    for a, b in zip(parent_a, parent_b):
        child.append(random.choice([a, b]))

    return "".join(child)


# Randomly change characters
def mutate(candidate):
    genes = list(candidate)

    for i in range(len(genes)):
        if random.random() < MUTATION_RATE:
            genes[i] = random.choice(pool)

    return "".join(genes)


# Initialize the population
population = [
    normalize_parent(gen1_1),
    normalize_parent(gen1_2)
]

population += [
    random_candidate()
    for _ in range(POPULATION_SIZE - len(population))
]


# Continuously produce one child per iteration
for attempt in range(MAX_REPRODUCTIONS):

    # Find and print the best current candidate
    best = max(population, key=fitness)

    preview = best if len(best) <= 80 else best[:80] + "..."

    print(
        f"Reproduction {attempt}: "
        f"{preview!r} | Fitness: "
        f"{fitness(best)}/{len(secret_text)}",
        flush=True
    )

    # Stop if the target has been found
    if best == secret_text:
        print(
            f"\nFound '{secret_text}' after "
            f"{attempt} reproduction attempts!"
        )
        break

    # Choose two parents from the current population
    parent_a = select_parent(population)
    parent_b = select_parent(population)

    # Create and mutate their child
    child = crossover(parent_a, parent_b)
    child = mutate(child)

    # Check whether this child is the solution
    if child == secret_text:
        print(
            f"\nFound '{secret_text}' after "
            f"{attempt + 1} reproduction attempts!"
        )
        break

    # A child survives if it is at least as fit
    # as the weakest candidate in the population
    population.sort(key=fitness, reverse=True)

    if fitness(child) >= fitness(population[-1]):
        population[-1] = child

else:
    best = max(population, key=fitness)

    print(
        f"\nReproduction limit reached. Best candidate: "
        f"{best!r} | Fitness: "
        f"{fitness(best)}/{len(secret_text)}"
    )
