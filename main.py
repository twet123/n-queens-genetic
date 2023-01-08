import numpy as np
import draw


def init(n, population_n):
    population = np.zeros((population_n, n))

    for i in range(population_n):
        for j in range(n):
            population[i][j] = np.random.randint(0, n)

    return population


def fitness_score(individual):
    # fitness se racuna kao broj kraljica koje se napadaju na datoj tabli (svaka jedinka predstavlja jednu tablu)
    res = 0
    for i in range(len(individual)):
        for j in range(len(individual)):
            if i == j:
                continue

            # napadaju se u sledecim slucajevima
            # 1 - nalaze se u istoj koloni (ista im je druga koordinata)
            # 2 - nalaze se na istoj dijagonali (gledamo obe dijagonale)
            # (apsolutna vrednost razlike izmedju prvih koordinata prvog i drugog elementa
            # mora biti jednaka sa apsolutnom vrednosti razlike izmedju drugih koordinata prvog i drugog elementa)

            x1 = i
            x2 = j
            y1 = individual[i]
            y2 = individual[j]

            if y1 == y2:
                res += 1

            elif np.abs(x1 - x2) == np.abs(y1 - y2):
                res += 1

    # na ovaj nacin brojimo svako napadanje dvaput pa delimo konacnan rezultat sa 2
    return res / 2


def crossover(n, parent1, parent2):
    # nasumicni pivoting point
    crossover_point = np.random.randint(0, n)

    child1 = np.concatenate((parent1[crossover_point:], parent2[:crossover_point]))
    child2 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))

    # mutacija - 70% sanse za random promenu u detetu
    if np.random.random() > 0.3:
        mutation_point = np.random.randint(0, n)
        child1[mutation_point] = np.random.randint(0, n)

    if np.random.random() > 0.3:
        mutation_point = np.random.randint(0, n)
        child2[mutation_point] = np.random.randint(0, n)

    return child1, child2


def genetic(n, population_n=100):
    generation = 0

    # inicijalizacija - kodiranje jedinki
    population = init(n, population_n)

    while True:
        # pravljenje dece - ukrstanje
        children = np.zeros((population_n, n))
        for i in range(int(population_n / 2)):
            # sortiranje po prilagodjenosti - selekcija
            population = np.array(sorted(population, key=lambda ind: fitness_score(ind) * np.random.random()))

            child1, child2 = crossover(n, population[0], population[1])
            children[i * 2] = child1
            children[i * 2 + 1] = child2

        generation += 1

        # pustamo 5% najboljih roditelja da prezive - elitizam
        elitism_deg = int(population_n * 0.05)
        children = np.array(sorted(children, key=lambda ind: fitness_score(ind)))
        population = np.array(sorted(population, key=lambda ind: fitness_score(ind)))

        for i in range(elitism_deg):
            if fitness_score(children[len(children) - i - 1]) > fitness_score(population[i]):
                children[len(children) - i - 1], population[i] = population[i], children[len(children) - i - 1]

        print(fitness_score(children[0]))
        if fitness_score(children[0]) == 0:
            return children[0], generation

        population = children


def main():
    print("Unesite n")
    n = int(input(">> "))

    optimal_solution, generations = genetic(n, 50)

    print("Broj generacija", generations)
    print("Resenje", optimal_solution)

    draw.drawChessTable(optimal_solution, n)


if __name__ == "__main__":
    main()
