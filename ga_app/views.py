import random
from django.shortcuts import render
from django.http import JsonResponse


# Define the polynomial function we want to solve f(x) = 0
def polynomial(coefficients, x):
    # coefficients.reverse()
    i = len(coefficients)
    result = 0
    # print(i)
    for j in range(len(coefficients)):
        # print(coefficients[j])
        # print(i)
        result += coefficients[j] * x ** i
        i -= 1
    # return coefficients[0] * x ** 4 + coefficients[1] * x ** 3 + coefficients[2] * x ** 2 + coefficients[3] * x + \
    #     coefficients[4]
    #
    return result


# Fitness function: the closer f(x) is to 0, the higher the fitness
def fitness(coefficients, x):
    return 1 / (1 + abs(polynomial(coefficients, x)))


# Generate an initial population of random solutions
def generate_population(size, x_min, x_max):
    return [random.uniform(x_min, x_max) for _ in range(size)]


# Select two parents from the population using roulette wheel selection
def select_parents(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    selection_probs = [fitness / total_fitness for fitness in fitness_scores]
    return random.choices(population, weights=selection_probs, k=2)


# Perform crossover to create a child from two parents
def crossover(parent1, parent2):
    return (parent1 + parent2) / 2


# Apply mutation to a child solution
def mutate(child, mutation_rate, x_min, x_max):
    if random.random() < mutation_rate:
        child += random.uniform(-1, 1)
        child = max(min(child, x_max), x_min)
    return child


# Genetic Algorithm to solve the polynomial
def genetic_algorithm(coefficients, pop_size, generations, x_min, x_max, mutation_rate):
    print("HIIII")
    population = generate_population(pop_size, x_min, x_max)

    for generation in range(generations):
        fitness_scores = [fitness(coefficients, x) for x in population]
        best_index = fitness_scores.index(max(fitness_scores))
        best_solution = population[best_index]
        best_fitness = fitness_scores[best_index]

        # Display progress
        print(
            f"Generation {generation + 1}: x = {best_solution:.5f}, f(x) = {polynomial(coefficients, best_solution):.5f}")

        new_population = []
        while len(new_population) < pop_size:
            parent1, parent2 = select_parents(population, fitness_scores)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate, x_min, x_max)
            new_population.append(child)

        population = new_population
    print(best_solution)
    return best_solution


# Django view to handle polynomial root finding
def index(request):
    if request.method == "POST":
        try:
            # Retrieve coefficients from the POST request
            # Parameters for the Genetic Algorithm
            mutation_rate = 0.1  # Probability of mutation
            num_variables = int(request.POST.get("num_variables"))
            num_generations = int(request.POST.get("num_generations"))
            population_size = int(request.POST.get("population_size"))
            x_min = int(request.POST.get("x_min"))
            x_max = int(request.POST.get("x_max"))

            print("Hello", request.POST)
            coefficients = [float(request.POST.get(f"a{i}", 0)) for i in range(num_variables + 1)]
            # print(num_variables, coefficients)
            # Run the genetic algorithm and print the best solution found
            best_solution = genetic_algorithm(coefficients, population_size, num_generations, x_min, x_max,
                                              mutation_rate)
            # print("HI")
            result_value = polynomial(coefficients, best_solution)
            print(f"\nBest solution: x = {best_solution:.5f}, f(x) = {polynomial(coefficients, best_solution):.5f}")

            # # Parameters for the Genetic Algorithm
            # population_size = 40
            # num_generations = 100
            # x_min, x_max = -10, 10
            # mutation_rate = 0.1
            #
            # # Run the genetic algorithm
            # best_solution = genetic_algorithm(coefficients, population_size, num_generations, x_min, x_max,
            #                                   mutation_rate)
            # result_value = polynomial(coefficients, best_solution)

            # Return the result
            return JsonResponse({
                "best_x": best_solution,
                "result": result_value
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    # Render a form or main page for GET requests
    return render(request, "index.html")
