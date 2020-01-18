import numpy as np
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import math
from utils import A_star,changeline,get_graph
import sys

start = sys.argv[1]
goal = sys.argv[2]

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
 

with open('./stationdata.txt') as f:
    tmp = f.read()
    station_geodata = eval(tmp)
    f.close()
with open('./subway_line.txt') as f:
    tmp = f.read()
    subway_line = eval(tmp)
    f.close()

try:
    station_geodata[start]
except KeyError:
    print("起始站无效,请重新输入")
    raise

try:
    station_geodata[goal]
except KeyError:
    print("目的地无效,请重新输入")
    raise


## 这四个地铁站的地理位置有错
station_geodata['奥林匹克公园'] = tuple((np.array(station_geodata['奥体中心'])+np.array(station_geodata['森林公园南门']))/2)
station_geodata['高碑店'] = tuple((np.array(station_geodata['传媒大学'])+np.array(station_geodata['四惠东']))/2)
station_geodata['国展'] = tuple((np.array(station_geodata['孙河'])+np.array(station_geodata['花梨坎']))/2)
station_geodata['果园'] = tuple((np.array(station_geodata['通州北苑'])+np.array(station_geodata['九棵树']))/2)

subway_connection = get_graph(subway_line)
subway_connection_graph = nx.Graph(subway_connection)
plt.figure(figsize=(30,30))
nx.draw(subway_connection_graph,station_geodata,with_labels=True,node_size=50)
plt.savefig("./bjsubway_graph.png")

search_optimal = A_star(graph=subway_connection,geodata=station_geodata,subway_lines=subway_line)
path = search_optimal.get_optimal(start,goal)
changeline(path,subway_line)
print('需要经过')
for station in path:
    print(station)