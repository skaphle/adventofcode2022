#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 7: No Space Left On Device"""


class Directory:
    """Holds information and links like a directory."""

    def __init__(self, name: str, parent):
        self.name = name
        self.parent = parent
        self.content = {}
        self._size = -1

    @property
    def size(self):
        """Return cumulative size of all content."""
        if self._size < 0:
            self._calculate_size()
        return self._size

    def _calculate_size(self):
        if len(self.content) == 0:
            self._size = 0
        else:
            self._size = sum(c if isinstance(c, int) else c.size for c in
                             self.content.values())

    def find(self, name):
        """Find dir/file NAME in this directory or subdirectories"""
        if name == self.name:
            return self
        if name in self.content:
            return self.content[name]
        for i in self.content.values():
            if not isinstance(i, Directory):
                continue
            ret = i.find(name)
            if ret is not None:
                return ret
        return None

    def read_input(self, input_string: str):
        """Build dir/file tree with this dir as root from commands in INPUT_STRING."""
        current_dir = self
        for line in input_string.splitlines():
            if line.startswith('$ cd'):
                dirname = line.split()[2]
                if dirname == '/':
                    current_dir = self
                elif dirname == '..':
                    current_dir = current_dir.parent
                else:
                    if dirname not in current_dir.content:
                        current_dir.content[dirname] = Directory(dirname, current_dir)
                    current_dir = current_dir.content[dirname]
            elif line.startswith('$ ls'):
                continue
            elif line.startswith('dir'):
                dirname = line.split()[1]
                if dirname not in current_dir.content:
                    current_dir.content[dirname] = Directory(dirname, current_dir)
            else:
                size, filename = line.split()
                current_dir.content[filename] = int(size)

    def list_directory_sizes(self) -> list:
        """Create a list of the size of all directories under this one."""
        size_list = [self.size]
        for item in self.content.values():
            if isinstance(item, Directory):
                size_list.extend(item.list_directory_sizes())
        return size_list


if __name__ == '__main__':
    # goal: read a directory tree from shell output, sum sizes
    #
    # structure:
    # - read in input
    # - fill some kind of directory tree object
    # - sum sizes for all directories in the tree
    # - make a list, remove those less than 100k, sum
    #
    # directory tree object:
    # - make a class for directory, another for files
    # - directory contains list of content, size function
    #
    # read input:
    # - line starts with '$ cd X': create/move to dir X
    # - line starts with '$ ls': fill content with next lines
    # - line starts with 'dir' or anything: fill content of current dir

    # test cases:
    EXAMPLE_1 = """$ cd /
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
7214296 k"""
    TEST_DIRS_1 = ['e', 'a', 'd', '/']
    TEST_EXPECTED_1 = [584, 94853, 24933642, 48381165]

    test_root_dir = Directory('/', None)
    test_root_dir.read_input(EXAMPLE_1)
    for num, e in enumerate(TEST_EXPECTED_1):
        assert test_root_dir.find(TEST_DIRS_1[num]).size == e, f'Expected {e}'
    test_sizes = test_root_dir.list_directory_sizes()
    test_sum_sizes = sum(s for s in test_sizes if s <= 100000)
    assert test_sum_sizes == 95437, 'Expected 95437'

    # actual puzzle
    with open('input.txt', encoding='utf-8') as f_in:
        input_text = f_in.read()
    root_dir = Directory('/', None)
    root_dir.read_input(input_text)
    sizes = root_dir.list_directory_sizes()
    sum_sizes = sum(s for s in sizes if s <= 100000)
    print(f'Sum of total sizes of small directories: {sum_sizes}')

    # part 2: find directory to delete
    TOTAL_DISK_SPACE = 70000000
    NEED_UNUSED_SPACE = 30000000

    # test
    test_need_free = test_root_dir.size + NEED_UNUSED_SPACE - TOTAL_DISK_SPACE
    assert test_need_free == 8381165
    test_smallest_to_delete = min(s for s in test_sizes if s > test_need_free)
    assert test_smallest_to_delete == 24933642

    # puzzle
    need_free = root_dir.size + NEED_UNUSED_SPACE - TOTAL_DISK_SPACE
    smallest_to_delete = min(s for s in sizes if s > need_free)
    print(f'Total size of dir to be deleted: {smallest_to_delete}')
