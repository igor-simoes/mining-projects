import os
import fnmatch


def find_files_by_pattern(pattern, directory, remove_distinct=False):
    """
    Description:
        Get a list of files in a directory that matches with the pattern.
    Params:
        @pattern -> regex string
        @directory -> directory string
        @remove_distinct (optional) -> if True, keep only the match files
    Return:
        List of path of files that matches with the pattern
    """
    if not os.path.isdir(directory):
        raise Exception(f'Directory {directory} not found')

    paths = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            if fnmatch.fnmatch(name, pattern):
                paths.append(file_path)
            else:
                if remove_distinct:
                    os.remove(file_path)
    return paths
