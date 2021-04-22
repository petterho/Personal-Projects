# -*- coding: utf-8 -*-

__author__ = 'Petter Bøe Hørtvedt'
__email__ = 'petterho@nmbu.no'

from src.personal_projects.Dijkstra.test_nodes import path_dict
from functools import total_ordering


@total_ordering
class Node:
    def __init__(self, parents, offsprings):
        self.parents = parents
        self.offsprings = offsprings
        self.shortest_from = None
        self.length = float('inf')

    def __len__(self):
        return self.length

    def __eq__(self, other):
        return len(self) == len(other)

    def __lt__(self, other):
        return len(self) < len(other)

    def __repr__(self):
        return f'Length: {self.length}'





class Dijkstra:
    def __init__(self, paths):
        self.priority_list = []
        self._make_priority_list(paths)

    def _make_priority_list(self, paths):
        self.priority_list = []
        for name, path in paths.items():
            self.priority_list.append(Node(name, path))

    def sort_priority_list(self):
        self.priority_list = sorted(self.priority_list)

if __name__ == '__main__':
    dij = Dijkstra(path_dict)
