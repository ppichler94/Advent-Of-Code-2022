from collections import namedtuple
from mylib.aoc_basics import Day

File = namedtuple("File", ["name", "size"])


class Directory:
    def __init__(self):
        self.directories = []
        self.files = []
        self.name = "_"
        self.parent = None

    def size(self):
        size = 0
        for file in self.files:
            size += file.size
        for directory in self.directories:
            size += directory.size()
        return size


class PartA(Day):
    def parse(self, text, data):
        lines = text.splitlines()
        current_dir = Directory()
        current_dir.name = "root"
        for i in range(1, len(lines)):
            line = lines[i]
            match line.split(" "):
                case ["$", "ls"]:
                    PartA.parse_ls(lines[i+1:], current_dir)
                case ["$", "cd", ".."]:
                    current_dir = current_dir.parent
                case ["$", "cd", name]:
                    current_dir = [d for d in current_dir.directories if d.name == name][0]
        while current_dir.parent:
            current_dir = current_dir.parent
        data.root = current_dir

    def compute(self, data):
        sizes = []
        PartA.calculate_sizes(data.root, sizes)
        return sum([s for s in sizes if s <= 100000])

    @staticmethod
    def parse_ls(lines, current_dir):
        for line in lines:
            if line[0] == "$":
                return
            if line[0:3] == "dir":
                d = Directory()
                d.name = line[4:]
                d.parent = current_dir
                current_dir.directories.append(d)
            else:
                parts = line.split(" ")
                current_dir.files.append(File(parts[1], int(parts[0])))

    @staticmethod
    def calculate_sizes(directory, sizes):
        sizes.append(directory.size())
        for d in directory.directories:
            PartA.calculate_sizes(d, sizes)

    def example_answer(self):
        return 95437

    def get_example_input(self, puzzle):
        return """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


class PartB(PartA):
    def compute(self, data):
        required_size = 30000000 - (70000000 - data.root.size())
        result = PartB.find_dir_to_delete(required_size, data.root, data.root.size())
        return result

    @staticmethod
    def find_dir_to_delete(required_size, directory, size):
        for d in directory.directories:
            result = PartB.find_dir_to_delete(required_size, d, size)
            if required_size <= result < size:
                return result
        directory_size = directory.size()
        if required_size <= directory_size < size:
            return directory_size
        return size

    def example_answer(self):
        return 24933642


Day.do_day(7, 2022, PartA, PartB)
