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
    ancestor2 = np.zeros(n, dtype)
    for i in range(n):
        ancestor[i]["x"] = i
        ancestor2[i]["x"] = i

    begin = np.random.randint(0, n-1)
    end = np.random.randint(0, n-1)
    if begin > end:
        tmp = begin
        begin = end
        end = tmp
    transport = first[begin:end]["y"]

    transport2 = np.zeros(begin-0 + n - end)
    transport2[0:begin] = first[0:begin]["y"]
    transport2[transport2.shape[0]-n+end:] = first[end:]["y"]

    ancestor2[0:begin]["y"] = first[0:begin]["y"]
    ancestor2[end:]["y"] = first[end:]["y"]
    j = begin
    for i in range(n):
        if second[i]["y"] in transport2:
            continue
        ancestor2[j]["y"] = second[i]["y"]
        j += 1

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
        ancestor = mutation(ancestor)
    if np.random.random() > 0.8:
        ancestor2 = mutation(ancestor2)
    return ancestor, ancestor2


def contains(ancestors, target):
    nastavi = False
    for elem in ancestors:
        if elem[1][0] == 0:
            return False
        for i in range(len(elem)):
            if elem[i][1] != target[i][1]:
                nastavi = True
                break
        if nastavi:
            nastavi = False
            continue
        return True
    return False


def genetic(n, population_n=100):
    # inicijalizacija - kodiranje jedinki
    population = init(n, population_n)
    ancestors = init_ancestors(n, population_n)
    j = 0
    # sortiranje po prilagodjenosti
    while True:
        j += 1
        for i in range(0, population_n, 2):
            population_tmp = np.array(sorted(population, key=lambda ind: fitness_score(ind) * np.random.random()))
            if fitness_score(population_tmp[0]) == 0 or j == 50:
                return population_tmp[0], j
            ancestors[i], ancestors[i+1] = crossover(population_tmp[0], population_tmp[1])
        # population = ancestors
        tmp = init(n, 2*population_n)
        tmp[:population_n, :] = population
        tmp[population_n:2*population_n, :] = ancestors
        population = tmp
        #population = np.append(population, ancestors)
        population = np.array(sorted(population, key=lambda ind: fitness_score(ind)))
        i = -1
        k = 0
        ancestors = init_ancestors(n, population_n)
        while True:
            i += 1
            if i == population.shape[0]:
                break
            if k == ancestors.shape[0]:
                break
            if not contains(ancestors, population[i]):
                ancestors[k] = population[i]
                k += 1
            else:
                pass
        ancestors[k:] = population[len(population)-(population_n-k):]
        population = ancestors


def main():
    print("Unesite n")
    n = int(input(">> "))
    queens_array, i = genetic(n)
    print(queens_array, i)
    graph.draw(n, queens_array)


if __name__ == "__main__":
    main()
