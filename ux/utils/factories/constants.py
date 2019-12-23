LOCS__ABCDE = ['a', 'b', 'c', 'd', 'e']
SRCS_TGTS__ONE_SHOT__ABCDE = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]
SRCS_TGTS__FORWARD_BACK__ABCDE = [
    ('a', 'b'), ('b', 'c'), ('c', 'd'),
    ('d', 'c'), ('c', 'b'),
    ('b', 'c'), ('c', 'd'), ('d', 'e')
]
