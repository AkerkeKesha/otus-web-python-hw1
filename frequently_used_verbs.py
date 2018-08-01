# coding=utf-8
import ast
import os
import collections
import logging

import helper

'''
X Надо бы сделать человеческое ридми, где описано, как установить и использовать библиотеку) 
X Глобальные переменные - не очень хорошее дело. Всё это можно получать из аргументов или в крайнем случае задавать так же, но в if __name__ == "__main__") 
X Дебажные принты хорошо бы удалить, а информационные заменить логированием
- проблема функции generate_trees в том, что они возвращает результат в различном формате в зависимости от аргументов - то кортеж из 2 или 3 элементов, то просто деревья. 
Это очень неудобно, если потребуется ее где-то переиспользовать
X В nltk глагол – не только VB, есть и другие тэги
X Докстринги не всегда хорошо, они устаревают оч быстро и часто дублирую информацию. Вот бы ту же инфу запихать в код, а докстринги поудалять
X ужасно длинная строчка) https://github.com/AkerkeKesha/otus-web-python-hw1/blob/8ab643ea11df77229f07d7de694b3bcc9339d37d/frequently_used_verbs.py#L44
X В одном файле куча всего: и функции с бизнес-логикой и мелкие хелперы. Можно их на разные файлы разложить) 
'''


def main():
    """

    This program outputs most frequently used verbs
    and their occurences as pair
    for python projects in a directory

    """

    TOP_SIZE = 200
    PROJECTS = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]
    # source for logging : https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler('frequently_used_verbs.log')
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    words = []

    for project in PROJECTS:
        path = os.path.join('.', project)
        words += get_top_verbs_in_path(path)

    print('total %s words, %s unique' % (len(words), len(set(words))))
    for word, occurence in collections.Counter(words).most_common(TOP_SIZE):
        print(word, occurence)


def get_top_verbs_in_path(path, top_size=10):
    trees = [t for t in get_trees(path) if t]
    flattened_list = helper.transform_to_list(trees)
    functions = [f for f in flattened_list if not helper.is_special_function()]
    logging.debug('functions extracted')
    verbs = helper.flatten([get_verbs_from_function_name(function_name) for function_name in functions])
    return collections.Counter(verbs).most_common(top_size)


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if helper.is_verb(word)]


def get_trees(path, with_filenames=False, with_file_content=False):
    filenames = find_python_files(path=path, limit=100)
    logging.debug('total %s files' % len(filenames))
    trees = generate_trees(filenames=filenames, with_filenames=with_filenames, with_file_content=with_file_content)
    logging.debug('trees generated')
    return trees


def find_python_files(path, limit):
    filenames = []
    for dirname, _, files in os.walk(path, topdown=True):
        if len(filenames) >= limit:
            break
        python_files = helper.custom_file_filter(files=files, dirname=dirname, extension=".py", )
        filenames.extend(python_files)
    return filenames[:limit]


def generate_trees(filenames, with_filenames, with_file_content):
    trees = []
    for filename in filenames:
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


if __name__== "__main__":
    main()