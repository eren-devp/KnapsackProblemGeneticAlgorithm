from random import choice, uniform


class Item:
    def __init__(self, name, worth, size):
        self.name = name
        self.worth = worth
        self.size = size


class Genome:
    def __init__(self):
        self.genome: list[Item] = []
        self.used_capacity = 0
        self.total_worth = 0

    def append(self, append_item: Item):
        self.genome.append(append_item)
        self.used_capacity += append_item.size
        self.total_worth += append_item.worth

    def __contains__(self, other: Item):
        for i in self.genome:
            if i.name == other.name:
                return True

        return False


class GeneticAlgorithm:
    def __init__(self, population_size: int, generation_count: int, max_capacity: int, inherit_count: int, fitness_goal: int, mutation_chance: float):
        self.population_size = population_size
        self.generation_count = generation_count
        self.max_capacity = max_capacity
        self.inherit_count = inherit_count
        self.fitness_goal = fitness_goal
        self.result: Genome = None
        self.mutation_chance = mutation_chance

    def create_population(self) -> list[Genome]:
        population: list[Genome] = []

        for i in range(self.population_size):
            exit_attempt = 0
            genome = Genome()

            while exit_attempt < 2:
                item_to_add = choice(ITEMS)
                if genome.__contains__(item_to_add) or (genome.used_capacity + item_to_add.size) > self.max_capacity:
                    exit_attempt += 1
                else:
                    genome.append(item_to_add)
                    break  # To make it fun. Since it already starts with high worth lists without this.

            population.append(genome)

        return population

    def crossing_over(self, population: list[Genome]) -> list[Genome]:
        new_population: list[Genome] = []

        for _ in range(self.population_size):
            genome = Genome()
            exit_attempt = 0

            breeds = [choice(population), choice(population)]

            if self.mutation_chance >= uniform(0, 1):  # Mutation
                while exit_attempt < 3:
                    item_to_add = choice(ITEMS)
                    if genome.__contains__(item_to_add) or (
                            genome.used_capacity + item_to_add.size) > self.max_capacity:
                        exit_attempt += 1
                    else:
                        genome.append(item_to_add)
            else:
                while exit_attempt < 10:
                    selected_breed = choice(breeds)

                    item_to_add_genome = choice(selected_breed.genome)
                    if genome.__contains__(item_to_add_genome) or (
                            genome.used_capacity + item_to_add_genome.size) > self.max_capacity:
                        exit_attempt += 1
                    else:
                        genome.append(item_to_add_genome)

            new_population.append(genome)

        return new_population

    def evolve(self, pop: list[Genome], count=0):
        print(count)

        pop_sorted = sorted(pop, key=lambda x: x.total_worth, reverse=True)
        print('worth:', pop_sorted[0].total_worth)

        if pop_sorted[0].total_worth >= self.fitness_goal or count >= self.generation_count:
            self.result = pop_sorted[0]
        else:
            self.evolve(self.crossing_over(pop_sorted[0:self.inherit_count]), count+1)


ITEMS = [
    Item('Book', 50, 15),
    Item('Laptop', 1500, 350),
    Item('Dress', 350, 40),
    Item('Monitor', 900, 200),
    Item('Socks', 15, 5),
    Item('Keyboard', 300, 100),
    Item('Headphones', 150, 450),
    Item('Phone', 400, 950),
    Item('Tshirt', 100, 25),
    Item('Shoes', 450, 250),
    Item('Tablet', 300, 75),
    Item('Coat', 75, 150),
    Item('Gloves', 25, 75)
]


POPULATION_SIZE = 100
MAX_GENERATION_SIZE = 150
MAX_CAPACITY = 1900
INHERIT_COUNT = 30
DESIRED_FITNESS = 4100
MUTATION_CHANCE = 0.1

genetic = GeneticAlgorithm(POPULATION_SIZE, MAX_GENERATION_SIZE, MAX_CAPACITY, INHERIT_COUNT, DESIRED_FITNESS, MUTATION_CHANCE)
population = genetic.create_population()
genetic.evolve(population)

result = genetic.result
print('\n\nResults:\n')
for item in result.genome:
    print(f'Item name: {item.name}')
    print(f'Item worth: {item.worth}')
    print(f'Item size: {item.size}\n')

print(f'Total worth: {result.total_worth}')
print(f'Total size: {result.used_capacity}')
