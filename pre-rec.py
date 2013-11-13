#!/bin/python3
import sys
from subprocess import Popen, PIPE
from codecs import BOM_UTF8
from operator import eq


#=================================================================================#
def filter_files_objects(tree_cont, different_files=None):
    req_exts = ['.c', '.h', '.cpp', '.hpp', '.test']
    filtered_files_objects = {}

    # отфильтроввываем по расширению
    for line in [line.decode() for line in tree_cont]:
        mode, type_, object_, file_name = line.split(maxsplit=3)  # maxsplit, т.к. имя может содержать пробелы.
        file_name = file_name.rstrip()
        if any([file_name.endswith(ext) for ext in req_exts]):
            filtered_files_objects[file_name] = object_

    # возвращаем различающиеся между сниками файлы
    if different_files:
        filtered_dif_files_objects = {}
        for fn, o in filtered_files_objects.items():
            if any([eq(fn, dfn) for dfn in different_files]):
                filtered_dif_files_objects[fn] = o
        return filtered_dif_files_objects
    else:
        return filtered_files_objects


def encoding_verify(triplet):
    result_files = []  # имена файлов не прошедших проверку на кодировку
    oldcommit, newcommit, ref = triplet
    is_new_branch = True if eq(oldcommit, '0'*40) else False

    command = 'git ls-tree -r --full-tree {}'.format(newcommit)
    proc = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)  # без shell=True команду git не найдёт.
    tree_cont = proc.stdout.readlines()  # формат вывода результата git ls-tree - <mode> SP <type> SP <object> TAB <file>

    if not is_new_branch:
        command = 'git diff --name-only {} {}'.format(oldcommit, newcommit)
        proc = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        different_files = proc.stdout.readlines()  # требуются для нахождения только различных блобов
        different_files = [line.decode().rstrip() for line in different_files]
        req_files_objects = filter_files_objects(tree_cont, different_files)
    else:
        req_files_objects = filter_files_objects(tree_cont)

    for file_name, object_ in req_files_objects.items():
        command = 'git cat-file blob {}'.format(object_)
        proc = Popen(command, stdout=PIPE, stderr=PIPE, shell=True, bufsize=3)
        blob_cont = proc.communicate()[0]
        if not blob_cont.startswith(BOM_UTF8):
            result_files.append(file_name)

    return result_files


#=================================================================================#
if __name__ == '__main__':
    input_info = sys.stdin.read().strip().split()  # берём на вводе параметры от GIT'a.
    branch_count = len(input_info)//3  # на одну ветку по три элемента - oldcommit, newcommit, ref
    if branch_count > 1:  # если проталкивается(push) несколько веток одновременно.
        triplets, ind = [], 0
        for step in range(branch_count):
            triplets.append([el for el in input_info[ind:ind+3]])
            ind += 3
    else:
        triplets = [input_info]

    files_without_bom = []
    for triplet in triplets:
        files = encoding_verify(triplet)
        files_without_bom.extend(files)

    if files_without_bom:
        exit('There are files without '
             'utf-8 with BOM encoding: {}'.format(files_without_bom))
