import ast
import os
import collections

from nltk import pos_tag


PATH = ''
TOP_SIZE = 200
PROJECTS = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]


def main():
    """
        This program outputs most frequently used verbs in the verb itself and occurence duo
        for given project names in a directory
    """
    words = []

    for project in PROJECTS:
        path = os.path.join('.', project)
        words += get_top_verbs_in_path(path)

    print('total %s words, %s unique' % (len(words), len(set(words))))
    for word, occurence in collections.Counter(words).most_common(TOP_SIZE):
        print(word, occurence)


def get_top_verbs_in_path(path, top_size=10):
    """
    This function return top 10 verbs in a given path to filenames
    :param path: string path to files
    :param top_size: max number of verbs to display
    :return: list of most commons verbs
    """
    trees = [t for t in get_trees(path) if t]
    flattened_list = flatten([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees])
    functions = [f for f in flattened_list if not is_special_function()]
    print('functions extracted')
    verbs = flatten([get_verbs_from_function_name(function_name) for function_name in functions])
    return collections.Counter(verbs).most_common(top_size)


def is_special_function():
    """
    This function checks if a function is special or not
    :return: True/False
    """
    return (f.startswith('__') and f.endswith('__'))


def get_trees(path, with_filenames=False, with_file_content=False):
    """
    This function generates trees of all filenames in a given path
    """
    filenames = find_python_files(path=path, limit=100)
    print('total %s files' % len(filenames))
    trees = []
    path = PATH
    for filename in filenames:
        trees = generate_trees(filename, tree, with_filenames, with_file_content)
    print('trees generated')
    return trees


def find_python_files(path, limit):
    """
    This function scans a directory to find a particular extension file
    :param path: the directory to scan
    :param limit: max number of files
    :return: list: list of filenames(strings)
    """
    filenames = []
    for dirname, _, files in os.walk(path, topdown=True):
        if len(filenames) >= limit:
            break
        python_files = custom_file_filter(files=files, dirname=dirname, extension=".py", )
        filenames.extend(python_files)
    return filenames[:limit]


def custom_file_filter(files, dirname, extension=".py"):
    """
    This function searches for particular files, by default .py files.
    :param files: name of files
    :param dirname: target directory name
    :param extension: particular extension
    :return: path to the files
    """
    return [os.path.join(dirname, file)
                for f in files if f.endswith(extension)]


def generate_trees(filename, tree, with_filenames, with_file_content):
    """
    This function returns generates tree of filenames
    """
    trees = []
    with open(filename, 'r', encoding='utf-8') as attempt_handler:
        main_file_content = attempt_handler.read()
    try:
        tree = ast.parse(main_file_content)
    except SyntaxError as e:
        print(e)
        tree = None
    if with_filenames:
        if with_file_content:
            trees.append((filename, main_file_content, tree))
        else:
            trees.append((filename, tree))
    else:
        trees.append(tree)
    return trees


def flatten(lst):
    """
    This function flattens a list of tuples for one level
    """
    return sum([list(item) for item in lst], [])


def get_verbs_from_function_name(function_name):
    """
    This function gives only verbs given a function name
    """
    return [word for word in function_name.split('_') if is_verb(word)]


def is_verb(word):
    """
    This function checks whether the word is a verb or not
    """
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


if __name__== "__main__":
    main()