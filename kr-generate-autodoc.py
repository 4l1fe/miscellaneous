# -*- coding: utf-8 -*-
import sys
import os
import shutil
import argparse
import textwrap
import api_sphinx_examples
from os.path import join
from ftplib import FTP
from operator import eq as equal

sys.path.append(os.getcwd())
import sbis_root


classes_list, methods_list = list(), list()


def parse_sbis_root():  # Танина необъяснимая логика.
    sbis_root_dict = sbis_root.__dict__

    def ap_item(lst, it):
        lst.append(it)

    switch = {
        "<class 'Boost.Python.class'>": lambda: ap_item(classes_list, k),
        "<class 'type'>": lambda: ap_item(classes_list, k),
        "<class 'Boost.Python.function'>": lambda: ap_item(methods_list, k)
    }

    for k, v in sbis_root_dict.items():
        string = str(type(v))
        if (string != "<class 'type'>" and switch.get(string)) \
            or (string == "<class 'type'>" and ord(k[0]) < 128 and k[0].istitle()):
            switch.get(string)()

    classes_list.sort()
    methods_list.sort()


def create_rst_files(sphinx_dir):
    all_classes_str = ""
    req_classes = ['Record', 'RecordSet', 'IField', 'BLObject', 'IStatement', 'IDatabase', 'SqlQuery']
    sc_name = 'sections/classes'
    sm_name = 'sections/methods'
    sect_cls_dir = join(sphinx_dir, sc_name)
    sect_meth_dir = join(sphinx_dir, sm_name)
    os.makedirs(sect_cls_dir, exist_ok=True)
    os.makedirs(sect_meth_dir, exist_ok=True)

    for cl in classes_list:
        rst_file_name = join(sect_cls_dir, cl+'.rst')
        rst_file = open(rst_file_name, mode='w', encoding='utf-8')
        equals = "======"
        for _char in cl:  # Знаков = должно быть равное количество длине имени класса.
            equals += "="

        # Если текущий класс(cl) входит в req_classes, то к автогенерируемой документации класса и его методов
        # подставляем кусок кода(code_block), описанный в модуле api_sphinx_examples.
        has_classes = [equal(cl, r_cl) for r_cl in req_classes]
        if not any(has_classes):
            rst_file.write(
                ".. Класс.\n\n"
                "Класс " + cl + "\n"
                + equals + "\n"
                ".. automodule:: sbis_root\n"
                ".. autoclass:: " + cl + "\n"
                "\t:members:\n"
                "\t:private-members:\n"
                "\t:special-members:")
        else:
            rst_file.write(
                ".. Класс.\n\n"
                "Класс " + cl + "\n"
                + equals + "\n"
                ".. automodule:: sbis_root\n"
                ".. autoclass:: " + cl + "\n\n\t")
            cl_obj = getattr(sbis_root, cl)
            cl_obj_items = cl_obj.__dict__.items()
            cl_methods = [item for item in cl_obj_items if not item[0].startswith('__')]

            for cl_method_name, cl_method_obj in cl_methods:
                rst_file.write(".. automethod:: " + cl_method_name)
                rst_file.write("\n\n\t\t")
                exmp_cl_obj = getattr(api_sphinx_examples, cl, None)
                exmp_meth_obj = getattr(exmp_cl_obj, cl_method_name, None)
                code_block = getattr(exmp_meth_obj, '__doc__', None)
                if code_block:
                    code_block = code_block.splitlines()
                    code_block = '\n'.join([code_line.strip() for code_line in code_block])
                    rst_file.write(".. code-block:: python\n\n")
                    rst_file.write(textwrap.indent(code_block, '\t' * 3))
                    rst_file.write("\n\n\t")
                else:
                    rst_file.write("\n\n\t")

        all_classes_str += "\t" + "classes/" + cl + "\n"

    sect_cls_rst = open(join(sphinx_dir, 'sections\classes.rst'), mode='w', encoding='utf-8')
    template = ".. СБиС Классы.\n\n"
    template += "Классы модуля sbis-python\n"
    template += "=========================\n\n"
    template += ".. toctree::\n"
    template += "\t:maxdepth: 2\n\n"
    template += all_classes_str + "\n"
    sect_cls_rst.write(template)
    sect_cls_rst.close()

    sect_meth_rst = open(join(sphinx_dir, 'sections\methods.rst'), mode='w', encoding='utf-8')
    template = ".. СБиС Методы.\n\n"
    template += "Методы модуля sbis-python\n"
    template += "============\n\n"
    template += ".. toctree::\n"
    template += "\t:maxdepth: 2\n\n"
    template += "\tmethods/Rec\n\n"
    sect_meth_rst.write(template)
    sect_meth_rst.close()

    mth_mod = open(join(sect_meth_dir, 'Rec.rst'), mode='w', encoding='utf-8')  #TODO: переименовать
    mth_mod.write(
        "Методы модуля sbis-python\n"
        "=========================\n"
        ".. automodule:: sbis_root\n"
        "\t:members:\n"
        "\t:private-members:\n"
        "\t:special-members:")
    mth_mod.close()

    # Редактирование index.rst. Добавляем ссылки на sc_name, sm_name
    index_rst = open(join(sphinx_dir, 'index.rst'))
    template = index_rst.read()
    index_rst.close()

    replaced_text = ':maxdepth: 2\n\n'
    replaced_text += '   {}\n'.format(sm_name)  # в результате не нравится символ - \t
    replaced_text += '   {}'.format(sc_name)
    template = template.replace(':maxdepth: 2', replaced_text)

    index_rst = open(join(sphinx_dir, 'index.rst'), 'w')
    index_rst.write(template)
    index_rst.close()

    #Настраиваем conf.py, чтобы подключить автоматический вывод строк документирования
    conf = open(join(sphinx_dir, 'conf.py'), 'a')
    service_dir = os.getcwd()
    template = 'sys.path.insert(0, r"{}")\n'.format(service_dir)
    template += 'extensions = ["sphinx.ext.autodoc"]'
    conf.write(template)


def sphinx_rebuild(sphinx_dir, prepared_dir):
    os.system('sphinx-build -b html -w sphinx_errors.txt -E -a ' + sphinx_dir  + ' ' + prepared_dir)
    #shutil.copy(os.path.abspath('..\..\..\doc-source-genc\index.php'), os.path.abspath('..\..\..\docs'))


#def copy_to_dev_wi(sphinx_dir):
#    def recurseDel(ftpClient, cdir="/dev-wi.sbis.ru/docs/bl/py", rootdir="/dev-wi.sbis.ru/docs/bl/py"):
#        ftpClient.cwd(cdir)
#        lister = list()
#        ftpClient.retrlines("NLST", lambda l: lister.append(l))
#        for name in lister:
#            testToDel = cdir + '/' + name
#            try:
#                ftpClient.delete(testToDel)
#            except:
#                try:
#                    ftpClient.rmd(testToDel)
#                except:
#                    recurseDel(ftpClient, testToDel)
#        try:
#            ftpClient.rmd(testToDel)
#        except:
#            try:
#                if testToDel[:testToDel.rfind('/')] != rootdir:
#                    ftpClient.rmd(testToDel[:testToDel.rfind('/')])
#                    print('in folder:' + testToDel)#.removedirs(testToDel)
#            except:
#                pass
#        return
#
#    def recurseUpload(ftpClient, cdir="/dev-wi.sbis.ru/docs/bl/py", docs=os.path.normpath(sphinx_dir + '\docs'),
#                      rootdir="/dev-wi.sbis.ru/docs/bl/py"):
#        try:
#            ftpClient.cwd(cdir)
#        except:
#            pass
#        for name in os.listdir(docs):
#            if name.startswith('.'):
#                _name = name
#                name = name[1:]
#                try:
#                    if not os.path.isfile(os.path.join(docs, name)):
#                        try:
#                            shutil.rmtree(os.path.join(docs, name))
#                        except:
#                            pass
#                    else:
#                        try:
#                            os.remove(os.path.join(docs, name))
#                        except:
#                            pass
#                    os.renames(os.path.join(docs, _name), os.path.join(docs, name))
#                except:
#                    pass
#            if os.path.isfile(os.path.join(docs, name)):
#                f = open(os.path.join(docs, name), "rb")
#                if len(name.split('.')) == 1:
#                    name += '.txt'
#                send = ftpClient.storbinary("STOR " + name, f)
#            else:
#                try:
#                    ftpClient.mkd(name)
#                except:
#                    print('not create ' + name)
#                recurseUpload(ftpClient, cdir + '/' + name, os.path.join(docs, name))
#                ftpClient.cwd('..')
#        pass
#
#    ftpClient = FTP('dev-wsr-static')
#    ftpClient.login('shuvalovatn', 'TkFFtb7N')
#    ftpClient.cwd("/dev-wi.sbis.ru/docs/bl/py")
#    recurseDel(ftpClient)
#    recurseUpload(ftpClient)
#    ftpClient.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sd', '--sphinx_dir', action='store', type=str, dest='sphinx_dir', required=True)
    result = parser.parse_args()

    #Получаем список классов Python API для генерации ресурсов сайта.
    parse_sbis_root()

    #Перегенерируем rst файлы с обновленными классами
    create_rst_files(result.sphinx_dir)

    #Делаем ребилд документации с обновленными rst файлами.
    prepared_dir = join(result.sphinx_dir, 'prepared_dir')
    sphinx_rebuild(result.sphinx_dir, prepared_dir)

    #Копируем по FTP на dev-wi.sbis.ru
    #copy_to_dev_wi(result.sphinx_dir)


if __name__ == '__main__':
    main()