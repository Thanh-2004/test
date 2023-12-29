import os
# os.chdir(r'C:\Users\Lenovo\Downloads')
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import inflect
from assistedFunctions import *
# Data collected 
restaurants = pd.read_csv('foodhygienedata.csv', encoding_errors= 'ignore')

coordinates = [(restaurants['latitude'][i] / (10**4), restaurants['longitude'][i] / (10**4)) for i in range(len(restaurants['latitude'])) if restaurants['longitude'][i] / (10**4) > 32]
coordinates = list(set(coordinates))
copy_coordinates = coordinates.copy()

# INPUT FOR THE NUMBER OF LEVELS AND STATIONS, NUMBER OF POINTS IN EACH LEVELS AND NUMBER OF STATIONS

# NumberOfLevelsandStations = int(input()) + 1
# NumberLevel = [] # NumberLevel[i] is the number of points in level (i+1) where NumberLevel[-1] is the number of stations
# # LevelPoints[i] is the list of points in level (i+1)
# for i in range(NumberOfLevelsandStations):
#     NumberLevel.append(int(input()))
NumberLevel = [10, 10, 10, 10, 7, 7, 7, 7, 5, 5, 25]
NumberOfLevelsandStations = len(NumberLevel)
LevelPoints = []
    
start, finish = coordinates[1831], (38,33.8)
del coordinates[1831]

# DATA POINTS GENERATION
seed, i = 0, 0
while i in range(NumberOfLevelsandStations):
    rng0 = np.random.default_rng(seed)
    position = list(rng0.integers(0, len(coordinates), NumberLevel[i]))
    if len(set(position)) != NumberLevel[i]: 
        seed += 1
        if i != 0:
            for j in range(i):
                coordinates.extend(LevelPoints[j])
            LevelPoints.clear()
        i = 0
    else: 
        # Making sure that the removal of elements in coordinates works.
        position.sort(reverse=True)
        LevelPoints.append([coordinates[k] for k in position])
        for k in position:
            coordinates.remove(coordinates[k])
        i += 1
        
# BOUNDS FOR THE FUEL CONSTRAINT
    # Lower Bound: this is just an infimum of the range of values that the fuel_constraint can take
lowerBound = haversine((start, finish))
    # Upper Bound: In order for our solution path to consist of at least a petrol station, the fuel constraint must be smaller than the length of the OptimalPath from "start" to "finish" when the "stations" are not considered. An arbitrary solution might be that optimal path. So the length(arbitrarySolution) >= length(OptimalPath) >= fuel_constraint
arbitrarySolution = [(start, LevelPoints[0][0])]
for i in range(NumberOfLevelsandStations-2):
    arbitrarySolution.append((LevelPoints[i][0], LevelPoints[i+1][0]))
arbitrarySolution.append((LevelPoints[-2][0], finish))
upperBound = sum(haversine_transformation(arbitrarySolution))

# print(lowerBound)
# print(upperBound)

# CREATION OF THE NEW DATA SET
    # Creating the MultiIndex
p = inflect.engine()
outside, inside = ['Start', 'Finish'], ['Start', 'Finish']

for i in range(NumberOfLevelsandStations-1):
    outside.extend([p.number_to_words(p.ordinal(i+1)) + 'Level']*NumberLevel[i])
    inside.extend([(p.number_to_words(p.ordinal(i+1)) + 'Level{}').format(j) for j in range(1, NumberLevel[i]+1)])
    
outside.extend(['Stations']*NumberLevel[-1])
inside.extend(['Station{}'.format(i) for i in range(1, NumberLevel[-1]+1)])

    # Creating the data needed
    # Here, the distances_to_finish list consists of distance from a point to the finish point with the order [start, finish, FL1, FL2, ..., FL(n1), SL1, SL2, ..., SL(n2), ...., Station1, Station2, ..., Station(n)]
distances_to_finish = [haversine((start, finish)), haversine((finish, finish))]
distances_to_finish.extend(haversine_transformation([(finish, point) for point in [i for item in LevelPoints for i in item]]))
# point is in the flatten list of LevelPoints
    # flatten_coor consists of coordinates of each point with the same order as that of the distances_to_finish list.
flatten_coor = [start, finish]
flatten_coor.extend([i for item in LevelPoints for i in item])
    # The info list's element is of the form (lat, long, distance_to_finish) with the same order like the flatten_coor list.
info = []
for i in range(len(flatten_coor)):
    info.append((flatten_coor[i][0], flatten_coor[i][1], distances_to_finish[i]))
    
    # Forming things together
hier_index = list(zip(outside, inside))
multiIndex = pd.MultiIndex.from_tuples(hier_index)
data = pd.DataFrame(info, multiIndex, ['Latitude', 'Longitude', 'Distances to finish point'])
# data.to_csv('updatedData.csv')

# VISUALIZATION
    # List of colors to use (MAXIMUM OF 10 COLORS FOR 9 LEVELS AND STATIONS)

path = ['Start', 'firstLevel5', 'Station23', 'secondLevel5', 'thirdLevel6', 'fourthLevel9', 'fifthLevel7', 'sixthLevel2', 'seventhLevel2', 'eighthLevel5', 'Station24', 'ninthLevel4', 'tenthLevel4', 'Station5', 'Finish']

colors = list(mcolors.TABLEAU_COLORS.values())
colors.extend(['black', '#9400D3', '#FFFF00'])
fig, ax = plt.subplots()
ax.scatter(start[0], start[1], c = colors[0], label = 'Start', edgecolors= 'red', linewidths=0.5)
ax.scatter(finish[0], finish[1], c = colors[1], label = 'Finish', edgecolors='red', linewidths=0.5)

for i in range(NumberOfLevelsandStations):
    if i != NumberOfLevelsandStations - 1:
        
        ax.scatter([LevelPoints[i][j][0] for j in range(NumberLevel[i])], [LevelPoints[i][j][1] for j in range(NumberLevel[i])], c = colors[i+2], label = p.number_to_words(p.ordinal(i+1))+'Level', edgecolors= 'black', linewidths=0.5)
    else:
        ax.scatter([LevelPoints[i][j][0] for j in range(NumberLevel[i])], [LevelPoints[i][j][1] for j in range(NumberLevel[i])], c = colors[i+2], label = 'Stations', edgecolors= 'black', linewidths=0.5)




x_point = []
y_point = []
level = 0
for i in range (1, len(path) - 1):
    if "Station" not in path[i]:
        level += 1
        x_point.append(data.loc[p.number_to_words(p.ordinal(level)) + 'Level'].loc[path[i]]["Latitude"])
        y_point.append(data.loc[p.number_to_words(p.ordinal(level)) + 'Level'].loc[path[i]]["Longitude"])
    else:
        x_point.append(data.loc["Stations"].loc[path[i]]["Latitude"])
        y_point.append(data.loc["Stations"].loc[path[i]]["Longitude"])

x_point.insert(0,start[0])
y_point.insert(0,start[1])
x_point.append(finish[0])
y_point.append(finish[1])
 
ax.scatter(x_point, y_point, s=100, color='red', edgecolors='black', label='Các Điểm')
ax.plot(x_point, y_point, marker='o', linestyle='-', color='blue', label='Đường Đi')

ax.text(start[0], start[1], 'Start', color = 'black')
ax.text(finish[0], finish[1], 'Finish', color = 'black')

ax.legend()
ax.set_title('Map of Possible Paths', fontweight = 'bold')
ax.set_xlabel('Latitude', fontweight = 'bold', fontstyle = 'italic', labelpad = 5, color = 'blue')
ax.set_ylabel('Longitude', fontweight = 'bold', fontstyle = 'italic', labelpad = 5, color = 'blue')
plt.show()

