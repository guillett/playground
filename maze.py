from numpy.random import randint, seed
from collections import deque


class Node(object):
    """Node object to create graph linking nodes directly through their neighbours attribute"""
    def __init__(self):
        super(Node, self).__init__()
        self.neighbours = []

    @classmethod
    def linkNodes(cls,*nodes):
        for s, e in [(s,e) for s in nodes for e in nodes if s is not e]:
            s.neighbours.append(e)

    @classmethod
    def createMaze(cls,nodes):
        used_nodes, nodes_remaining, node_segments = set([nodes[0]]), set(nodes[1:]), list()
        while len(nodes_remaining)>0:
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

def test_simple_node():
    node_number = 5
    nodes = [Node() for i in range(node_number)]
    Node.linkNodes(*nodes)
    for n in nodes:
        assert(len(n.neighbours) == node_number - 1)

def test_direct_maze():
    s = randint(1000)
    print('seed: {}'.format(s))
    seed(s)

    node_number = 50
    nodes = [Node() for i in range(node_number)]
    Node.linkNodes(*nodes)
    segments = Node.createMaze(nodes)
    link_count = sum([len(s)-1 for s in segments])
    assert(link_count == node_number - 1)

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
