# -*- coding: utf-8 -*-

__author__ = 'Petter Bøe Hørtvedt'
__email__ = 'petterho@nmbu.no'

from src.personal_projects.Dijkstra.test_nodes import path_dict


class Path:
    def __init__(self, shortest_from, total_length):
        self.shortest_from = shortest_from
        self.length = total_length

    def __len__(self):
        return len(self.length)


class PriorityQueue:
    def __init__(self):
        self.priority_queue = []

    def __len__(self):
        return len(self.priority_queue)

    def __getitem__(self, item):
        return self.priority_queue[item]

    def __setitem__(self, key, value):
        # Not sure about this
        self.priority_queue.append(value)


class Dijkstra:
    def __init__(self, nodes, start, stop):
        self.nodes = nodes
        self.position = None
        self.start = start
        self.stop = stop

        self.shortest_way_dict = {}
        for key in nodes:
            if key == start:
                self.shortest_way_dict[key] = {'distance': 0}
            else:
                self.shortest_way_dict[key] = {'distance': float('inf')}
