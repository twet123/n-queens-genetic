import numpy as np


def init(n, population_n):
    dtype = np.dtype([("x", np.uint8), ("y", np.uint8)])
    population = np.zeros((population_n, n), dtype)

    for i in range(population_n):
        for j in range(n):
            population[i][j]["x"] = np.random.randint(0, n - 1)
            population[i][j]["y"] = np.random.randint(0, n - 1)

    return population


def fitness_score(individual):
    # fitness se racuna kao broj kraljica koje se napadaju na datoj tabli (svaka jedinka predstavlja jednu tablu)
    res = 0
    for i in range(len(individual)):
        for j in range(len(individual)):
            if i == j:
                continue

            # napadaju se u sledecim slucajevima
            # 1 - nalaze se u istoj koloni (ista im je prva koordinata)
            # 2 - nalaze se u istom redu (ista im je druga koordinata)
            # 3 - nalaze se u na istoj dijagonali (gledamo obe dijagonale)
            # (apsolutna vrednost razlike izmedju prvih koordinata prvog i drugog elementa
            # mora biti jednaka sa apsolutnom vrednoscu razlike izmedju drugih koordianata prvog i drugog elementa)

            if individual[i]["x"] == individual[j]["x"]:
                res += 1

            elif individual[i]["y"] == individual[j]["y"]:
                res += 1

            elif np.abs(individual[i]["x"] - individual[j]["x"]) == np.abs(individual[i]["y"] - individual[j]["y"]):
                res += 1

    # na ovaj nacin brojimo svako napadanje dvaput pa delimo konacnan rezultat sa 2
    return res / 2


def genetic(n, population_n=100):
    # inicijalizacija - kodiranje jedinki
    population = init(n, population_n)

    # sortiranje po prilagodjenosti
    population = np.array(sorted(population, key=lambda ind: fitness_score(ind) * np.random.random()))

    print(population)


def main():
    print("Unesite n")
    n = int(input(">> "))

    queens_array = genetic(n)


if __name__ == "__main__":
    main()
