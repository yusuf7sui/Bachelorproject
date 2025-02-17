'''
TODO: Add extended data for validation and scenarios later.
'''

"""
list of lists for the rcpsp in following order
duration, resource, and list of predecessors
"""
base_data = [[0, 0, []],
        [2, 2, [0]],
        [5, 2, [0]],
        [8, 6, [0]],
        [1, 5, [1]],
        [10, 5, [2]],
        [9, 3, [2, 3]],
        [2, 4, [0]],
        [3, 7, [4, 5]],
        [8, 3, [5]],
        [6, 2, [8]],
        [6, 4, [10]],
        [9, 4, [8, 9]],
        [2, 4, [7]],
        [8, 4, [6, 13]],
        [6, 1, [14]],
        [10, 1, [13]],
        [5, 3, [16]],
        [8, 2, [12, 15]],
        [3, 3, [17]],
        [0, 0, [11, 18, 19]]
        ]

RESOURCE_CAPACITY = 10