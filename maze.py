from numpy.random import randint, seed
from collections import deque


class Node(object):
    '''Node object to create graph linking nodes directly through their neighbours attribute'''
    def __init__(self):
        super(Node, self).__init__()
        self.neighbours = []

    @classmethod
    def link_nodes(cls,s,e):
        s.neighbours.append(e)
        e.neighbours.append(s)

    @classmethod
    def create_maze(cls,nodes):
        used_nodes, nodes_remaining, node_segments = set([nodes[0]]), set(nodes[1:]), list()
        while nodes_remaining:
            node_segment = deque([nodes_remaining.pop()])
            while True:
              last_node = node_segment[-1]
              n = len(last_node.neighbours)
              next_node = last_node.neighbours[randint(n)]
              if next_node in node_segment:
                while node_segment[-1] is not next_node:
                  node_segment.pop()
              else:
                node_segment.append(next_node)
                if next_node in used_nodes:
                  break

            node_set = set(node_segment)
            used_nodes |= node_set
            nodes_remaining -= node_set
            node_segments.append(node_segment)

        return node_segments

class Node2D(Node):
    def __init__(self, x, y):
        super(Node2D, self).__init__()
        self.x = x
        self.y = y

    @classmethod
    def create_grid(cls,height,width):
        node_grid = [[Node2D(x,y) for x in range(width)] for y in range(height)]
        for x in range(width-1):
            for y in range(height):
                cls.link_nodes(node_grid[y][x],node_grid[y][x+1])
        for x in range(width):
            for y in range(height-1):
                cls.link_nodes(node_grid[y][x],node_grid[y+1][x])


        return [n for row in node_grid for n in row]

def test_simple_node_link():
    a, b = Node(), Node()
    Node.link_nodes(a,b)
    for n in [a,b]:
        assert(len(n.neighbours) == 1)

def test_direct_maze():
    s = randint(1000)
    print('seed: {}'.format(s))
    seed(s)

    node_number = 50
    nodes = [Node() for i in range(node_number)]
    for s, e in [(s,e) for s in nodes for e in nodes if s is not e]:
        Node.link_nodes(s,e)
    segments = Node.create_maze(nodes)
    link_count = sum([len(s)-1 for s in segments])
    assert(link_count == node_number - 1)

def test_grid():
    width, height = 4, 3
    node_grid = Node2D.create_grid(height, width)

    node_count = width * height
    assert(len(node_grid) == node_count)
    double_counted_neighbour_count = sum([len(n.neighbours) for n in node_grid])
    assert(double_counted_neighbour_count // 2 == (width - 1) * height + width * (height - 1))

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        import re
        for test_name in [v for v in dir() if re.match('^test_',v)]:
            print('Running: {}'.format(test_name))
            eval(test_name + '()')
            print('         {}: OK'.format(test_name))
    else:
        print('Command line utility')
