import ast
import os

from nltk import pos_tag


def transform_to_list(trees):
    list_of_trees = []
    for tree in trees:
        lower_cased_function = [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        list_of_trees.append(lower_cased_function)
    return flatten(list_of_trees)


def is_special_function():
    return f.startswith('__') and f.endswith('__')


def flatten(lst):
    return sum([list(item) for item in lst], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return 'VB' in pos_info[0][1]


def custom_file_filter(files, dirname, extension=".py"):
    return [os.path.join(dirname, file)
                for f in files if f.endswith(extension)]

