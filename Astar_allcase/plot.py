import Astar_1step_allcase
import Astar_2step_v3
import matplotlib as plt
from AIProjectData import *
import os
current_directory = os.getcwd()


path1 = Astar_1step_allcase.path

path2 =  Astar_2step_v3.path

# colors = list(mcolors.TABLEAU_COLORS.values())
# colors.extend(['black', '#9400D3', '#FFFF00'])
# fig, ax = plt.subplots()
# ax.scatter(start[0], start[1], c = colors[0], label = 'Start', edgecolors= 'red', linewidths=0.5)
# ax.scatter(finish[0], finish[1], c = colors[1], label = 'Finish', edgecolors='red', linewidths=0.5)

# for i in range(NumberOfLevelsandStations):
#     if i != NumberOfLevelsandStations - 1:
        
#         ax.scatter([LevelPoints[i][j][0] for j in range(NumberLevel[i])], [LevelPoints[i][j][1] for j in range(NumberLevel[i])], c = colors[i+2], label = p.number_to_words(p.ordinal(i+1))+'Level', edgecolors= 'black', linewidths=0.5)
#     else:
#         ax.scatter([LevelPoints[i][j][0] for j in range(NumberLevel[i])], [LevelPoints[i][j][1] for j in range(NumberLevel[i])], c = colors[i+2], label = 'Stations', edgecolors= 'black', linewidths=0.5)


def plot(path, name):
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
    ax.set_title(f'{name}', fontweight = 'bold')
    ax.set_xlabel('Latitude', fontweight = 'bold', fontstyle = 'italic', labelpad = 5, color = 'blue')
    ax.set_ylabel('Longitude', fontweight = 'bold', fontstyle = 'italic', labelpad = 5, color = 'blue')
    # plt.savefig(f'{current_directory}/{name}.png')

    plt.show()
    # return ax

# for ax, (y, title) in zip(axes.flat, data):
#     ax.plot(x, y)
#     ax.set_title(title)

# Tăng khoảng cách giữa các subplot để tránh trùng lắp
plt.tight_layout()

# Hiển thị đồ thị
plt.show()


plot(path1, "Astar_1step_allcase")
plot(path2, "Astar_2step_v3")





