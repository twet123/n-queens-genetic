import random

import numpy as np
import graph

def init_ancestors(n, population_n):
    dtype = np.dtype([("x", np.int8), ("y", np.int8)])
    return np.zeros((population_n, n), dtype)


def init(n, population_n):
    dtype = np.dtype([("x", np.int8), ("y", np.int8)])
    population = np.zeros((population_n, n), dtype)

    for i in range(population_n):
        perm = np.random.permutation(n)
        for j in range(n):
            population[i][j]["x"] = j
            population[i][j]["y"] = perm[j]

    return population


def fitness_score(individual):
    res = 0
    for i in range(len(individual)):
        for j in range(len(individual)):
            if i == j:
                continue

            if individual[i]["x"] == individual[j]["x"]:
                res += 1

            elif individual[i]["y"] == individual[j]["y"]:
                res += 1

            elif np.abs(individual[i]["x"] - individual[j]["x"]) == np.abs(individual[i]["y"] - individual[j]["y"]):
                res += 1

    return res / 2


def mutation(individual):
    n = np.shape(individual)[0]
    a = np.random.randint(0, n-1)
    b = n - a - 1
    tmp = individual[a]["y"]
    individual[a]["y"] = individual[b]["y"]
    individual[b]["y"] = tmp
    return individual


def crossover(first, second):
    dtype = np.dtype([("x", np.int8), ("y", np.int8)])
    n = np.shape(first)[0]
    ancestor = np.zeros(n, dtype)
    for i in range(n):
        ancestor[i]["x"] = i
    begin = np.random.randint(0, n-1)
    end = np.random.randint(0, n-1)
    if begin > end:
        tmp = begin
        begin = end
        end = tmp
    transport = first[begin:end]["y"]
    for i in range(begin, end):
        ancestor[i]["y"] = first[i]["y"]

    j = 0
    for i in range(n):
        if j == begin:
            j = end
        if second[i]["y"] in transport:
            continue
        ancestor[j]["y"] = second[i]["y"]
        j += 1
    if np.random.random() > 0.8:
        return mutation(ancestor)
    return ancestor


def genetic(n, population_n=100):
    # inicijalizacija - kodiranje jedinki
    population = init(n, population_n)
    ancestors = init_ancestors(n, population_n)
    j = 0
    # sortiranje po prilagodjenosti
    while True:
        j += 1
        for i in range(population_n):
            population_tmp = np.array(sorted(population, key=lambda ind: fitness_score(ind) * np.random.random()))
            if fitness_score(population_tmp[0]) == 0:
                return population_tmp[0], j
            ancestors[i] = crossover(population_tmp[0], population_tmp[1])
        population = ancestors
        ancestors = init_ancestors(n, population_n)
    # print(population)


def main():
    print("Unesite n")
    n = int(input(">> "))
    queens_array, i = genetic(n, 100)
    print(queens_array, i)
    graph.draw(n, queens_array)


if __name__ == "__main__":
    main()