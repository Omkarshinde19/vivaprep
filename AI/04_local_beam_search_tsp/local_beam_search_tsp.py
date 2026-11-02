# Local Beam Search for the Travelling Salesman Problem
import random

city_names = "ABCDEF"
distances = [[0, 10, 15, 20, 18, 12],
             [10, 0, 35, 25, 17, 28],
             [15, 35, 0, 30, 28, 20],
             [20, 25, 30, 0, 22, 16],
             [18, 17, 28, 22, 0, 14],
             [12, 28, 20, 16, 14, 0]]
beam_width = 4
total_iterations = 5


def tour_cost(tour):
    cost = 0
    for position in range(6):
        cost = cost + distances[tour[position - 1]][tour[position]]
    return cost


random.seed(1)
beam = []
for count in range(beam_width):
    beam.append(tuple([0] + random.sample([1, 2, 3, 4, 5], 5)))
best_tour = min(beam, key=tour_cost)

for iteration in range(1, total_iterations + 1):
    successors = set()
    for tour in beam:
        for first in range(1, 6):
            for second in range(first + 1, 6):
                new_tour = list(tour)
                new_tour[first], new_tour[second] = new_tour[second], new_tour[first]
                successors.add(tuple(new_tour))
    beam = sorted(successors, key=tour_cost)[:beam_width]
    if tour_cost(beam[0]) < tour_cost(best_tour):
        best_tour = beam[0]
    print("Iteration", iteration, "| Beam best:", tour_cost(beam[0]), "| Global best:", tour_cost(best_tour))

route = [city_names[city] for city in best_tour]
print("Best tour:", route, "back to A | Distance:", tour_cost(best_tour))
