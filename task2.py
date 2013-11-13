from os import walk, mkdir
from os.path import splitext, join, exists, basename
from xml.etree.ElementTree import ElementTree
from traceback import print_exc
from additional_functions import (hyp_sp_to_underscore,
                                  write_object_params,
                                  write_sources_triggers,
                                  write_static_methods)


def main(ROOT_DIR, ROOT_DIR_SBIS3):
    if not exists(ROOT_DIR_SBIS3): mkdir(ROOT_DIR_SBIS3)  # Создаем пакет sbis3.

    # Корневой __init__ файл для импорта всех модулей.
    main_init_file = open(join(ROOT_DIR_SBIS3, '__init__.py'), 'w', encoding='utf-8')

    # Обход всей директории "МОдули".
    for dirpath, subdirnames, filenames in walk(ROOT_DIR):

        if dirpath == ROOT_DIR_SBIS3: continue  # Пропускаем папку со сгенерированными питоновскими объектами.

        module_name = 'mod_' + hyp_sp_to_underscore(basename(dirpath))
        WRITING_DIR = join(ROOT_DIR_SBIS3, module_name)  # Формируем адрес папки для записи генер-х объектов.
        for filename in filenames:
            f_name, f_exten = splitext(filename)

            # Начинаем парсить только для файлов с расишрением f_exten == orx.
            if 'orx' in f_exten:
                if not exists(WRITING_DIR): mkdir(WRITING_DIR)  # Создаем пакет для сгенер-х объектов
                                                                # только если в модуле имеется .orx-файл.

                main_init_file.write('from .{} import *\n'.format(module_name))

                # __init__ файл для каждого модуля.
                sub_init_file = open(join(WRITING_DIR, '__init__.py'), 'w', encoding='utf-8')

                try:
                    root = ElementTree(file=dirpath+'\\'+filename)
                    for OBJ in root.findall('object'):
                        obj_name = OBJ.get('name')
                        tmp_name = join(WRITING_DIR, obj_name) + '.py'  # Имя .py-файла для каждого объекта верхнего уровня.
                        obj_file = open(tmp_name, 'w+', encoding='utf-8')

                        sub_init_file.write('from .{} import *\n'.format(obj_name))

                        obj_comment = "'''{}'''".format(OBJ.findtext('comment')) if OBJ.findall('comment') else ''

                        obj_file.write('class {}:\n'.format(obj_name))
                        obj_file.write('\tinsert_on_create = {}\n'.format(OBJ.get('insert_or_create')))
                        obj_file.write('\tread_only = {}\n'.format(OBJ.get('read_only')))
                        if obj_comment:
                            obj_file.write('\tcomment = {}\n'.format(obj_comment))
                        write_sources_triggers(OBJ, obj_file)
                        write_object_params(OBJ, obj_file)
                        position =  obj_file.tell()
                        write_static_methods(OBJ, obj_file, position=position)

                        # Обход вложенных объектов, только на один уровень вниз.
                        if OBJ.find('object'):
                            for subOBJ in OBJ.findall('object'):
                                sub_comment = "'''{}'''".format(subOBJ.findtext('comment')) if subOBJ.findall('comment') else ''
                                obj_file.write('\tclass {}: \n'.format(subOBJ.get('name')))
                                obj_file.write('\t\tinsert_on_create = {}\n'.format(subOBJ.get('insert_or_create')))
                                obj_file.write('\t\tread_only = {}\n'.format(subOBJ.get('read_only')))
                                if sub_comment:
                                    obj_file.write('\t\tcomment = {}\n'.format(sub_comment))
                                write_sources_triggers(subOBJ, obj_file, tab_count=2)
                                write_object_params(subOBJ, obj_file, tab_count=2)
                                position = obj_file.tell()
                                write_static_methods(subOBJ, obj_file, tab_count=2, position=position)

                            obj_file.close()
                except:
                    print_exc()  # Сокращение для print_exception(*sys.exc_info(), limit, file).

                sub_init_file.close()
    main_init_file.close()

if __name__ == '__main__':
    ROOT_DIR = r'D:\test\sbis\sbis\Модули'
    ROOT_DIR_SBIS3 = join(ROOT_DIR, 'sbis3')

    main(ROOT_DIR, ROOT_DIR_SBIS3)