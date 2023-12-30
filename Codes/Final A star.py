#!/usr/bin/env python
# coding: utf-8

# In[7]:


import heapq
import math
from collections import defaultdict
import folium


# In[8]:


data = {'Coordinates': [(23.280126, 77.277271), (23.280795, 77.276637), (23.283971, 77.275993),
                        (23.284846, 77.276118), (23.287006, 77.276214), (23.290009, 77.273448),
                        (23.290539, 77.273309), (23.292874, 77.272337), (23.292071, 77.270811),
                        (23.286678, 77.274191), (23.285461, 77.274559), (23.284394, 77.274873),
                        (23.281605, 77.274823)],
        'Noise Level Data(db)': [-26.97354555, -26.17504835, -25.2361846, -26.69413567, -25.10133266,
                                 -25.21312952, -22.81238317, -25.13707876, -25.85065842, -26.1979723,
                                 -24.99213457, -32.41874933, -25.08525133]}


# In[9]:


def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.insert(0, current)
    return path
def calculate_noise(path, data):
    return sum(data['Noise Level Data(db)'][path[i]] for i in range(len(path)))


# In[10]:


def a_star_algorithm(data, start, end):
    open_set = [(0, start)]
    closed_set = set()

    g_scores = defaultdict(lambda: float('inf'))
    g_scores[start] = 0

    f_scores = defaultdict(lambda: float('inf'))
    f_scores[start] = euclidean_distance(data['Coordinates'][start], data['Coordinates'][end])

    came_from = {}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == end:
            return reconstruct_path(came_from, current)

        closed_set.add(current)

        for i, (coord, noise_level) in enumerate(zip(data['Coordinates'], data['Noise Level Data(db)'])):
            if i == current or i in closed_set:
                continue

            tentative_g_score = g_scores[current] + noise_level
            if tentative_g_score < g_scores[i]:
                came_from[i] = current
                g_scores[i] = tentative_g_score
                f_scores[i] = tentative_g_score + euclidean_distance(data['Coordinates'][i], data['Coordinates'][end])
                heapq.heappush(open_set, (f_scores[i], i))

    return None


# In[11]:


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


# In[12]:


start_location = 0
end_location = 7
a_star_path = a_star_algorithm(data, start_location, end_location)
print(f"A* path: {a_star_path}")

a_star_noise = calculate_noise(a_star_path, data)
print(f"A* noise: {a_star_noise}")


# In[14]:


a_star_map = create_map(data['Coordinates'], data['Noise Level Data(db)'], a_star_path)
a_star_map.save('A star Route.html')


# In[ ]:





# In[ ]:




