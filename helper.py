import ast

from nltk import pos_tag


def transform_to_list(trees):
    """
    This function flattens tree of files
    """
    list_of_trees = []
    for tree in trees:
        lower_cased_function = [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        list_of_trees.append(lower_cased_function)
    return flatten(list_of_trees)


def is_special_function():
    """
    This function checks if a function is special or not
    """
    return f.startswith('__') and f.endswith('__')


def flatten(lst):
    """
    This function flattens a list of tuples for one level
    """
    return sum([list(item) for item in lst], [])


def is_verb(word):
    """
    This function checks whether the word is a verb or not
    """
    if not word:
        return False
    pos_info = pos_tag([word])
    return 'VB' in pos_info[0][1]

