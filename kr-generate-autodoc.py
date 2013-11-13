# -*- coding: utf-8 -*-
import sys, os, shutil, argparse
import textwrap
import api_sphinx_examples
from os.path import join
from ftplib import FTP
from operator import eq as equal

sys.path.append(os.getcwd())
import sbis_root


classes_list, methods_list = list(), list()


def prepareSourceDirs(sphinx_root):
    os.chdir(sphinx_root)
    if not os.path.exists('.\docs'):
        os.makedirs('.\docs')
    if not os.path.exists('.\doc-static') or not os.path.exists('.\doc-static\conf.py') or not os.path.exists('.\doc-static\index.rst'):
        exit('fatal error: no config or index files')
    else:
        try:
            shutil.rmtree('.\doc-source-genc', ignore_errors=False, onerror=None)
        except:
            pass
        finally:
            try:
                shutil.copytree('.\doc-static', '.\doc-source-genc')
            except:
                if not os.path.exists('.\doc-source-genc'):
                    exit('fatal error: doc-source-genc is not found')
                else:
                    pass

def getSbisMembers(sphinx_root):
    sbis_dir = sbis_root.__dict__

    def appendItem(lst, it):
        lst.append(it)

    switch = {
                "<class 'Boost.Python.class'>": lambda: appendItem(classes_list, key),
                "<class 'type'>": lambda: appendItem(classes_list, key),
                "<class 'Boost.Python.function'>":lambda: appendItem(methods_list, key)
             }
    for key in sbis_dir:
        if (str(type(sbis_dir[key])) != "<class 'type'>"and switch.get(str(type(sbis_dir[key])))) \
            or (str(type(sbis_dir[key])) == "<class 'type'>" and ord(key[0]) < 128 and key[0].istitle()):
            switch.get(str(type(sbis_dir[key])))()
    for _lst in [classes_list, methods_list]:
        _lst.sort()

def regenSources(sphinx_root):
    os.chdir(sphinx_root)
    req_classes = ['Record', 'RecordSet', 'IField', 'BLObject', 'IStatement', 'IDatabase', 'SqlQuery']
    list_cl_str = ""

    try:
        os.makedirs('.\doc-source-genc\sections\classes')
        os.makedirs('.\doc-source-genc\sections\methods')
    except:
        if not os.path.exists('.\doc-source-genc\sections'):
            exit('fatal error: sections folder is not found')
    for cl in classes_list:
        file = open('.\doc-source-genc\sections\classes\\'+cl+'.rst', mode='w', encoding='utf-8')
        equals = "======"
        for _char in cl:
            equals += "="

        # Если текущий класс(cl) входит в req_classes, то к автогенерируемой документации класса и его методов
        # подставляем кусок кода(code_snippet), описанный в модуле api_sphinx_examples.
        has_classes = [equal(cl,r_cl) for r_cl in req_classes]
        if not any(has_classes):
            file.write(".. Класс.\n\nКласс "+cl+"\n"+equals+"\n.. automodule:: sbis_root\n.. autoclass:: "+cl+"\n\t:members:\n\t:private-members:\n\t:special-members:")
        else:
            file.write(".. Класс.\n\nКласс "+cl+"\n"+equals+"\n.. automodule:: sbis_root\n.. autoclass:: "+cl+"\n\n\t")
            cl_obj = getattr(sbis_root, cl)
            cl_obj_items = cl_obj.__dict__.items()
            cl_methods = [item for item in cl_obj_items if not item[0].startswith('__')]

            for cl_method_name, cl_method_obj in cl_methods:
                file.write(".. automethod:: "+cl_method_name)
                file.write("\n\n\t\t")
                exmp_cl_obj = getattr(api_sphinx_examples, cl, None)
                exmp_meth_obj = getattr(exmp_cl_obj, cl_method_name, None)
                code_snippet = getattr(exmp_meth_obj, '__doc__', None)
                if code_snippet:
                    code_snippet = code_snippet.splitlines()
                    code_snippet = '\n'.join([code_line.strip() for code_line in code_snippet])
                    file.write(".. code-block:: python\n\n")
                    file.write(textwrap.indent(code_snippet, '\t'*3))
                    file.write("\n\n\t")
                else:
                    file.write("\n\n\t")

        list_cl_str += "\t"+"classes/"+cl+"\n"

    cls_rst = open('.\doc-source-genc\sections\\classes.rst', mode='w', encoding='utf-8')
    clss_str = ".. СБиС Классы.\n\n"
    clss_str += "Классы модуля sbis-python\n=========================\n\n"
    clss_str += ".. toctree::\n\t:maxdepth: 2\n\n" + list_cl_str + "\n"
    cls_rst.write(clss_str)
    cls_rst.close()

    mth_rst = open('.\doc-source-genc\sections\\methods.rst', mode='w', encoding='utf-8')
    mth_str = ".. СБиС Методы.\n\n"
    mth_str += "Методы модуля sbis-python\n============\n\n"
    mth_str += ".. toctree::\n\t:maxdepth: 2\n\n\tmethods/Rec\n\n"
    mth_rst.write(mth_str)
    mth_rst.close()

    mth_mod = open('.\doc-source-genc\sections\\methods\\Rec.rst', mode='w', encoding='utf-8')
    equals = "======"
    mth_mod.write("Методы модуля sbis-python\n=========================\n.. automodule:: sbis_root\n\t:members:\n\t:private-members:\n\t:special-members:")
    mth_mod.close()

def rebuildStatic(platform_name, sphinx_root):
    os.chdir(sphinx_root)
    os.chdir('.\\' + platform_name + '\www\service')
    os.system('dir > txt')
    # os.system('sphinx-build -b html -w sphinx_errors.txt -E -a -c C:\SPHINX_PY_AUTODOC\doc-source-genc C:\SPHINX_PY_AUTODOC\doc-source-genc C:\SPHINX_PY_AUTODOC\docs')
    os.system('sphinx-build -b html -w sphinx_errors.txt -E -a -c '+join(sphinx_root, 'doc-source-genc ')+join(sphinx_root,'doc-source-genc ')+join(sphinx_root,'docs'))
    shutil.copy(os.path.abspath('..\..\..\doc-source-genc\index.php'), os.path.abspath('..\..\..\docs'))

def copyToDevWI(sphinx_root):
    def recurseDel(ftpClient, cdir = "/dev-wi.sbis.ru/docs/bl/py", rootdir = "/dev-wi.sbis.ru/docs/bl/py"):
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

    def recurseUpload(ftpClient, cdir = "/dev-wi.sbis.ru/docs/bl/py", docs = os.path.normpath(sphinx_root + '\docs'), rootdir = "/dev-wi.sbis.ru/docs/bl/py"):
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
                send = ftpClient.storbinary("STOR "+ name, f)
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
    #парсим аргументы из командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('-pn', '--platform_name', action='store', type=str, dest='platform_name', required=True)
    parser.add_argument('-sr', '--sphinx_root', action='store', type=str, dest='sphinx_root', required=True)
    res_args = parser.parse_args()
    platform_name = res_args.platform_name
    sphinx_root = res_args.sphinx_root

    #Проверяем, что папка с начальными ресурсами существует. Готовим директорию для хранения исходных ресурсов автодокументации.
    prepareSourceDirs(sphinx_root)

    #Получаем список классов Python API для генерации ресурсов сайта.
    getSbisMembers(sphinx_root)
    # if isSuccessUpdate:
    #Перегенерируем rst файлы с обновленными классами
    regenSources(sphinx_root)
    #Делаем ребилд документации с обновленными ресурсами
    rebuildStatic(platform_name, sphinx_root)

    #Копируем по FTP на dev-wi.sbis.ru
    copyToDevWI(sphinx_root)

if __name__ == '__main__':
    main()