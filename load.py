
"""
Functions to read backup config files.
"""

import os
import pathspec


def filelist(path):
    """
    Load the file at `path` and use pathspec to find all matches.
    Assumes all paths are prefixed with the user's home directory.
    """
    roots = {}
    under = '/'
    globs = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line[0] == '#':
                continue
            if line[0] == '@':
                under = os.path.expanduser('~/')+line[1:]
                continue
            if line[0] == '%':
                globs.append(line[1:])
                continue
            try:
                roots[under].append(line)
            except KeyError:
                roots[under] = [line]
    _add_globs(roots, globs)  # mutates
    return _match_files(roots)


def _add_globs(roots, globs):
    """
    Add global excludes to each root. Mutates lines lists in place.
    """
    for lines in roots.values():
        lines.extend(globs)


def _match_files(roots):
    all_files = []
    for root, lines in roots.items():
        spec = pathspec.PathSpec.from_lines('gitignore', lines)
        all_files.extend([root+path for path in spec.match_tree(root)])
    return all_files
