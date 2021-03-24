import os
import sys
import jsonpickle

class Node(object):
    _children = []
    _paths = []
    _character = ''
    _parent = None

    def __init__(self, parent, character):
        self._parent = parent
        self._character = character
        self._children = []
        self._paths = []

    def AddPath(self, path):
        if path not in self._paths:
            self._paths.append(path)

    def AddChild(self, child):
        if child not in self._children:
           self._children.append(child)

    def GetCharacter(self):
        return self._character

    def NextChild(self, character, search):
        if len(self._children) > 0:
            for child in self._children:
                if character == child.GetCharacter():
                    return child
        if not search:
            new_child = Node(self, character)
            self.AddChild(new_child)
            return new_child
        else:
            return None

    def Size(self):
        return len(self._children)

    def PrintOptions(self):
        if len(self._children) > 0:
            paths = []
            for child in self._children:
                paths.extend(child.PrintOptions())
            return paths
        else:
            return self._paths

    def __str__(self):
        return "Node {}".format(self._character)

    def __eq__(self, obj):
        return isinstance(obj, Node) and obj.GetCharacter() == self.GetCharacter()


def main():
    sys.setrecursionlimit(5000)
    root = None
    json_file = 'test_data'
    count = 0
    if not os.path.exists(json_file):
        directories = ['C:\\Users']
        root = Node(None, '')
        while(len(directories) > 0):
            curr_dir = directories[0]
            directories.pop(0)
            for r, d, f in os.walk(curr_dir):
                directories.extend(d)
                for file in f:
                    last = root
                    count += 1
                    for c in file:
                        next_node = last.NextChild(c, False)
                        if next_node is not None:
                            last = next_node
                    last.AddPath(os.path.join(curr_dir, file))
        with open(json_file, 'w') as f:
            f.write(jsonpickle.encode(root))
    else:
        with open(json_file, 'r') as f:
            root = jsonpickle.decode(f.read())
    search_term = sys.argv[1]
    print("Searching for {st}.....\r\n".format(st=search_term))
    options = root
    results = ""
    for c in search_term:
        next_option = options.NextChild(c, True)
        if next_option is None:
            print("Best match is {r}".format(r=results))
            break
        else:
            results += c
            options = next_option
    print("Options:\r\n")
    paths = options.PrintOptions()
    if len(paths) > 20:
        val = input("There are {count} items in the list. Display them all? y|n:\t".format(count=len(paths)))
        if val.lower() != 'y':
            exit()
    print(*paths, sep = "\r\n")

if __name__ == '__main__':
    main()