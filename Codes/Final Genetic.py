#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import math
import folium


# In[2]:


data = {'Coordinates': [(23.280126, 77.277271), (23.280795, 77.276637), (23.283971, 77.275993),
                        (23.284846, 77.276118), (23.287006, 77.276214), (23.290009, 77.273448),
                        (23.290539, 77.273309), (23.292874, 77.272337), (23.292071, 77.270811),
                        (23.286678, 77.274191), (23.285461, 77.274559), (23.284394, 77.274873),
                        (23.281605, 77.274823)],
        'Noise Level Data(db)': [-26.97354555, -26.17504835, -25.2361846, -26.69413567, -25.10133266,
                                 -25.21312952, -22.81238317, -25.13707876, -25.85065842, -26.1979723,
                                 -24.99213457, -32.41874933, -25.08525133]}


# In[3]:


def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def calculate_noise(path, data):
    return sum(data['Noise Level Data(db)'][path[i]] for i in range(len(path)))


# In[4]:


def generate_individual():
    mid_path_options = [[], [1], [2], [2, 1], [3], [3, 1], [3, 2], [3, 2, 1]]
    mid_path = random.choice(mid_path_options)
    path = [0] + mid_path + [4, 5, 6] + [7] + [8, 9, 10, 11, 12]
    return path

def crossover(parent1, parent2):
    index1 = 1
    index2 = len(parent1) - 9
    child1_middle = parent2[index1:index2]
    child2_middle = parent1[index1:index2]

    child1 = parent1[:index1] + child1_middle + parent1[index2:]
    child2 = parent2[:index1] + child2_middle + parent2[index2:]

    return child1, child2

def mutate(individual):
    index1 = random.randint(1, len(individual) - 10)
    index2 = random.randint(1, len(individual) - 10)

    mutated = individual[:]
    mutated[index1], mutated[index2] = mutated[index2], mutated[index1]

    return mutated


# In[5]:


def genetic_algorithm(data, population_size=100, generations=1000, mutation_rate=0.1, elitism=True):
    population = [generate_individual() for _ in range(population_size)]
    for generation in range(generations):
        population.sort(key=lambda individual: calculate_noise(individual, data))
        if elitism:
            new_population = [population[0]]
        else:
            new_population = []
        
        while len(new_population) < population_size:
            parent1 = random.choice(population[:population_size//2])
            parent2 = random.choice(population[:population_size//2])
            child1, child2 = crossover(parent1, parent2)

            if random.random() < mutation_rate:
                child1 = mutate(child1)

            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.append(child1)
            new_population.append(child2)

        population = new_population

    best_path = population[0]
    best_noise = calculate_noise(best_path, data)
    return best_path, best_noise


# In[6]:


def create_map(locations, noise_levels, path=None):
    center_lat = sum(loc[0] for loc in locations) / len(locations)
    center_lon = sum(loc[1] for loc in locations) / len(locations)

    my_map = folium.Map(location=[center_lat, center_lon], zoom_start=14)

    for i, (location, noise_level) in enumerate(zip(locations, noise_levels)):
        folium.Marker(location, popup=f'Location {i}: {noise_level} db').add_to(my_map)

    if path:
        for i in range(len(path) - 1):
            folium.PolyLine([locations[path[i]], locations[path[i+1]]], color="blue", weight=2.5).add_to(my_map)

    return my_map


# In[7]:


best_path, best_noise = genetic_algorithm(data)
print(f"Best path: {best_path}")
print(f"Best noise: {best_noise}")


# In[8]:


locations_map = create_map(data['Coordinates'], data['Noise Level Data(db)'], best_path)
locations_map.save('Genetic Route.html')


# In[ ]:




