import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import math

def get_graph(subway_lines):
    subway_connection = defaultdict(list)
    for line in subway_lines:
        for i,station in enumerate(subway_lines[line]):
            if i==0: #每一条线获取前一个站和后一个站
                subway_connection[station].append(subway_lines[line][i+1])
            elif i>0 and i<len(subway_lines[line])-1:
                subway_connection[station].append(subway_lines[line][i+1])
                subway_connection[station].append(subway_lines[line][i-1])
            elif i==len(subway_lines[line])-1:
                subway_connection[station].append(subway_lines[line][i-1])
            i = i+1
        if line == "2号线" or line == "10号线": ##北京地铁十号线和二号线为环形
            subway_connection[subway_lines[line][-1]].append(subway_lines[line][0])
            subway_connection[subway_lines[line][0]].append(subway_lines[line][-1])
        ## 14号线合并为一条线
    return subway_connection

def get_current_line(name,subway_lines):
    target = []
    for line in subway_lines.keys():
        if name in subway_lines[line]:
            target.append(line)
    return target

def changeline(path,subway_lines):
    current_line = list(set(get_current_line(path[0],subway_lines)) & set(get_current_line(path[1],subway_lines)))
    i = 1
    print("始发线路:"+current_line[0])
    while i < len(path)-1:
        check = list(set(get_current_line(path[i],subway_lines)) & set(get_current_line(path[i+1],subway_lines)))
        if check[0] != current_line[-1]:
            current_line.append(check[0])
            print("在"+path[i]+"换乘"+check[0])
        i = i+1
    print("到达目的地"+path[-1])
    return current_line

class A_star():
    def __init__(self,graph,geodata,subway_lines):
        self.graph = graph
        self.start = ''
        self.goal = ''
        self.geodata = geodata
        self.subway_lines = subway_lines
    
    def cost(self,path):
        cost = self.current_distance(path)+10*self.change_times(path)+self.geo_distance(self.geodata[path[-1]],self.geodata[self.goal])
        return cost
    
    def change_times(self,path):
        current_line = list(set(self.get_current_line(path[0])) & set(self.get_current_line(path[1])))
        i = 1
        while i < len(path)-1:
            check = list(set(self.get_current_line(path[i])) & set(self.get_current_line(path[i+1])))
            if check[0] != current_line[-1]:
                current_line.append(check[0])
            i = i+1
        return len(current_line)-1
    
    def current_distance(self,path):
        distance = 0
        
        for i,_ in enumerate(path[:-1]):
            distance += self.geo_distance(self.geodata[path[i]],self.geodata[path[i+1]])
            
        return distance
    
    def get_current_line(self,name):
        target = []
        for line in self.subway_lines.keys():
            if name in self.subway_lines[line]:
                target.append(line)
        return target
    
    def geo_distance(self,origin,destination):
        #求地球表面距离
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6371  # km 

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c

        return d
    
#     def pruning(self,path):
        
    def get_optimal(self,start,goal):
        self.start = start
        self.goal = goal
        pathes = [[start]]
        visited = set()
        while pathes:
            path = pathes.pop(0)
            current_station = path[-1]
            if current_station in visited : continue# ！

            if current_station == goal:
                return path

            next_stations = self.graph[current_station]

            for station in next_stations:
                if station in path: continue  # check loop

                new_path = path+[station]

                pathes.append(new_path)  #bfs

            pathes = sorted(pathes,key=lambda path:self.cost(path)) 
            visited.add(current_station)