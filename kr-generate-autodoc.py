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

    # хитрое Танино вычисление нужных объектов из всего словаря пакета sbis_root.
    for k, v in sbis_root_dict.items():
        string = str(type(v))
        if (string != "<class 'type'>" and switch.get(string)) \
            or (string == "<class 'type'>" and ord(k[0]) < 128 and k[0].istitle()):
            switch.get(string)()

    classes_list.sort()
    methods_list.sort()


def generate_required_files(sphinx_dir):
    """В целом конечная документация строится по rst-файлам.
    В этой функции динамически создаются rst-директивы вместе с блоками кода, которые подхватываются из
    строк документации объектов модуля api_sphinx_examples, и ,соответственно, пишутся в rst-файлы.
    По ним sphinx создаст конечную документацию в функции sphinx_build().
    Тут так же присутствует правка конфигурационного файла глобальных настроек conf.py"""

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
        equals = "======" + "="*len(cl)  # Знаков = должно быть равное количество длине имени класса.

        # Если текущий класс(cl) входит в req_classes, то к автогенерируемой документации класса и его методам
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

    template = ".. СБиС Классы.\n\n"
    template += "Классы модуля sbis-python\n"
    template += "=========================\n\n"
    template += ".. toctree::\n"
    template += "\t:maxdepth: 2\n\n"
    template += all_classes_str + "\n"
    classes_rst = open(join(sphinx_dir, sc_name+'.rst'), mode='w', encoding='utf-8')
    classes_rst.write(template)
    classes_rst.close()

    template = ".. СБиС Методы.\n\n"
    template += "Методы модуля sbis-python\n"
    template += "============\n\n"
    template += ".. toctree::\n"
    template += "\t:maxdepth: 2\n\n"
    template += "\tmethods/AllMethods\n\n"
    methods_rst = open(join(sphinx_dir, sm_name+'.rst'), mode='w', encoding='utf-8')
    methods_rst.write(template)
    methods_rst.close()

    all_methods_rst = open(join(sect_meth_dir, 'AllMethods.rst'), mode='w', encoding='utf-8')  #TODO: переименовать
    all_methods_rst.write(
        "Методы модуля sbis-python\n"
        "=========================\n"
        ".. automodule:: sbis_root\n"
        "\t:members: " + ', '.join(methods_list))
    all_methods_rst.close()

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

    # Настраиваем conf.py, чтобы подключить автоматический вывод строк документирования объектов.
    # Настройки добавляются в конец файла conf.py, тем самым переписывая уже существующие(так проще и понятнее).
    conf = open(join(sphinx_dir, 'conf.py'), 'a')
    current_dir = os.getcwd()
    template = 'sys.path.insert(0, r"{}")\n'.format(current_dir)
    template += 'extensions = ["sphinx.ext.autodoc"]'
    conf.write(template)


def sphinx_build(sphinx_dir):
    prepared_dir = join(sphinx_dir, 'prepared_dir')
    os.system('sphinx-build -b html -w sphinx_errors.txt -E -a ' + sphinx_dir  + ' ' + prepared_dir)


def copy_to_dev_wi(sphinx_dir):

    def recurseDel(ftpClient, cdir="/dev-wi.sbis.ru/docs/bl/py", rootdir="/dev-wi.sbis.ru/docs/bl/py"):
        ftpClient.cwd(cdir)
        lister = list()
        ftpClient.retrlines("NLST", lambda l: lister.append(l))
        for name in lister:
            testToDel = cdir + '/' + name
            try:
                ftpClient.delete(testToDel)
            except:
                try:
                    ftpClient.rmd(testToDel)
                except:
                    recurseDel(ftpClient, testToDel)
        try:
            ftpClient.rmd(testToDel)
        except:
            try:
                if testToDel[:testToDel.rfind('/')] != rootdir:
                    ftpClient.rmd(testToDel[:testToDel.rfind('/')])
                    print('in folder:' + testToDel)#.removedirs(testToDel)
            except:
                pass
        return

    def recurseUpload(ftpClient, cdir="/dev-wi.sbis.ru/docs/bl/py", docs=os.path.normpath(sphinx_dir + '\docs'),
                      rootdir="/dev-wi.sbis.ru/docs/bl/py"):
        try:
            ftpClient.cwd(cdir)
        except:
            pass
        for name in os.listdir(docs):
            if name.startswith('.'):
                _name = name
                name = name[1:]
                try:
                    if not os.path.isfile(os.path.join(docs, name)):
                        try:
                            shutil.rmtree(os.path.join(docs, name))
                        except:
                            pass
                    else:
                        try:
                            os.remove(os.path.join(docs, name))
                        except:
                            pass
                    os.renames(os.path.join(docs, _name), os.path.join(docs, name))
                except:
                    pass
            if os.path.isfile(os.path.join(docs, name)):
                f = open(os.path.join(docs, name), "rb")
                if len(name.split('.')) == 1:
                    name += '.txt'
                send = ftpClient.storbinary("STOR " + name, f)
            else:
                try:
                    ftpClient.mkd(name)
                except:
                    print('not create ' + name)
                recurseUpload(ftpClient, cdir + '/' + name, os.path.join(docs, name))
                ftpClient.cwd('..')
        pass

    ftpClient = FTP('dev-wsr-static')
    ftpClient.login('shuvalovatn', 'TkFFtb7N')
    ftpClient.cwd("/dev-wi.sbis.ru/docs/bl/py")
    recurseDel(ftpClient)
    recurseUpload(ftpClient)
    ftpClient.close()


def main():
    """Сценарий был частично переписан,
    после довольно специфической логики изначального автора"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-sd', '--sphinx_dir', action='store', type=str, dest='sphinx_dir', required=True)
    result = parser.parse_args()

    parse_sbis_root()

    generate_required_files(result.sphinx_dir)

    sphinx_build(result.sphinx_dir)


if __name__ == '__main__':
    main()