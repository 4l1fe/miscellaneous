from itertools import chain
from textwrap import indent
from pprint import pprint

TAB = '\t'

# Функция замещает дефис и пробел в именах на подчеркивание.
def hyp_sp_to_underscore(name):
    return name.replace('-', '_').replace(' ', '_')


# Функции для заполнения классов методами и полями
def write_sources_triggers(OBJ, file, tab_count=1):
    tab = TAB * tab_count
    sources = []
    extension_sources = []
    for source in OBJ.findall('source'):
        trigger_attribs = []
        for trigger in source.findall('trigger_list/trigger'):
            trigger_attribs.append({'name': trigger.get('name'),
                                    'priority': trigger.get('priority'),
                                    'type': trigger.get('type')})
        sources.append((source.get('name'), trigger_attribs))

    for ext_source in OBJ.findall('extension_source'):
        extension_sources.append(ext_source.get('name'))

    file.write(tab + 'sources_triggers = {}\n'.format(sources))
    file.write(tab + 'extension_sources = {}\n'.format(extension_sources))


def write_object_params(OBJ, file, tab_count=1):
    tab = TAB * tab_count
    obj_params = []
    for param in OBJ.findall('object_params/object_param'):
        param_attribs = param.attrib
        if param.findall('comment'):
            obj_par_comment = param.findtext('comment')
            param_attribs.update(comment=obj_par_comment)
        obj_params.append(param_attribs)
    file.write(tab + 'object_params = {}\n'.format(obj_params))


def write_static_methods(OBJ, file, tab_count=1, position=None,):
    tab = TAB * tab_count
    method_kinds = ('generate_method', 'select', 'standart_select', 'declarative', 'proxy', 'http')
    methods_structure = {}  # Вся вложенная структура методов, за исключением их параметров и тел.
    method_names = []  # Список имен методов для проверки на совпадение.
    i = 2

    # В каждом повторении будем наполнять словарь methods_structure для целого объекта(класса) OBJ.
    # Этот словарь запишем позже в определение класса.
    # Он будет содержать подробное описание для каждого метода объекта(класса).
    for method in OBJ.findall('*'):
        if method.tag not in method_kinds: continue  # Пропускаем один цикл, если дочерний тэг не является методом.

        # Форматируем имя метода.
        method_name = method.get('name').split('.', 1)[1] if ('.' in method.get('name')) else method.get('name')
        if method_name in method_names:  # Если имя метода повторяется, дописываем суффикс "Метод_2".
            method_name += '_{}'.format(i)
            i += 1
        method_names.append(method_name)

        loop_tab = tab
        methods_structure[method_name] = {}
        isdeclarative = (method.tag == 'declarative')

        # Объявление вложенных тэгов и их атрибутов.
        method_attribs = method.attrib
        method_params = ''
        returns = []
        method_handlers = []
        cached = method.find('cached').attrib if method.findall('cached') else {}
        meth_comment = "'''{}'''".format(method.findtext('comment')) if method.findall('comment') else ''
        area_of_sight = method.find('area_of_sight').attrib if method.findall('area_of_sight') else {}
        sources = []
        fields = []
        sortings = []
        filtering_params = []
        calculatings = []
        composites = []

        for couple in [['method_attribs', method_attribs], ['cached', cached], ['meth_comment', meth_comment], ['area_of_sight', area_of_sight]]:
            if couple[1]:
                methods_structure[method_name].update([couple])

        # Создаем строку с позиционными/именованными аргументами для записи в определение метода.
        if not isdeclarative:  # Для этого метода тэг <parametr> служит для фильтрации.
            for parameter in chain(method.findall('parameter'), method.findall('std_parameter')):
                if parameter.get('default'):
                    gotten = parameter.get('default')
                    default = "'{}'".format(gotten) if gotten == 'null' else gotten
                    method_params += ', ' + parameter.get('name') + '=' + default
                else:
                    method_params += ', ' + parameter.get('name')
        # Форматируем строку с параметрами в необходимый для записи вид,
        # убираем первую запятую в строке с параметрами.
        method_params = method_params.replace(', ', '', 1)

        # Заполняем список возвращаемых значений метода.
        for retr in method.findall('return'):
            dict_ = retr.attrib
            dict_['format'] = {}
            elements = []
            for tag in retr.findall('format/*'):
                if tag.tag == 'element':
                    st = tag.find('string')
                    val = tag.find('value')
                    element = {st.tag: st.text, val.tag: val.text}
                    elements.append(element)
                else:
                    dict_['format'].update({tag.tag: tag.text})
                if elements:
                    dict_['format'].update({'elements': elements})
            returns.append(dict_)
        if returns: methods_structure[method_name].update({'returns': returns})

        # Заполняем список обработчиков метода.
        for handler in method.findall('method_hadler'):
            method_handlers.append(handler.text)
        if method_handlers: methods_structure[method_name].update({'method_handlers': method_handlers})

        if isdeclarative:
            # Заполняем список источников <source>.
            for source in method.findall('source'):
                attribs = source.attrib
                attribs.update(name=source.get('name'))
                sources.append(attribs)
            if sources: methods_structure[method_name].update({'sources': sources,})

            # Заполняем список полей для метода declarative.
            for field in method.findall('field'):
                fields.append(field.text)
            if fields: methods_structure[method_name].update({'fields': fields})

            # Заполняем список параметров сортировки для метода declarative.
            for sorting in method.findall('sorting'):
                sortings.append(sorting.attrib)
            if sortings: methods_structure[method_name].update({'sortings': sortings})

            # Заполняем список параметров фильтрации для метода declarative.
            for fil_param in method.findall('parameter'):
                attribs = fil_param.attrib
                if fil_param.findall('comment'):  # Простой find('comment') тупит, не находит элемент.
                    fil_param_comment = fil_param.findtext('comment')
                    attribs.update(comment=fil_param_comment)
                filtering_params.append(attribs)
            if filtering_params: methods_structure[method_name].update({'filtering_params': filtering_params})

            # Заполняем список рассчитываемых полей метода declarative.
            for calculating in method.findall('calculating'):
                attribs = calculating.attrib
                if calculating.findall('definition'):
                    attribs['definition'] = {}
                    attribs['definition'].update(language=calculating.findtext('definition/language'))
                    attribs['definition'].update(body=calculating.findtext('definition/body'))
                if calculating.get('type') == 'ENUM':
                    attribs['enum_items'] = []
                    for value in calculating.findall('enums_item/value'):
                        attribs['enum_items'].append({'value': value.text})
                if calculating.get('type') == 'FLAGS':
                    attribs['flag_items'] = []
                    for value in calculating.findall('flags_item/value'):
                        attribs['flag_items'].append({'value': value.text})
                calculatings.append(attribs)
            if calculatings: methods_structure[method_name].update({'calculatings': calculatings})

            # Заполняем список условий фильтрации, только первый уровень.
            for composite in method.findall('composite'):
                com_attribs = composite.attrib
                if composite.findall('simple'):
                    simples = []
                    for simple in composite.findall('simple'):
                        sim_attribs = simple.attrib
                        sim_attribs['left']= simple.find('left').attrib
                        sim_attribs['right'] = simple.find('right').attrib
                        simples.append(sim_attribs)
                    com_attribs['simples'] = simples
                if composite.findall('sql_expression'):
                    sql_exprs = []
                    for sql_expr in composite.findall('sql_expression'):
                        language = sql_expr.findtext('definition/language')
                        body = sql_expr.findtext('definition/body')
                        sql_exprs.append({'language': language, 'body': body})
                    com_attribs['sql_expressions'] = sql_exprs
                composites.append(com_attribs)
            if composites: methods_structure[method_name].update({'composites':composites})

        # Записываем метод с необходимыми отступами.
        file.write(loop_tab + '@staticmethod\n')
        file.write(loop_tab + 'def {}({}):\n'.format(method_name, method_params))
        loop_tab += TAB
        if method.get('type') == 'PYTHON':
            file.write(indent("{}".format(method.findtext('definition/body')) + '\n\n', loop_tab))
        else:
            file.write(loop_tab + 'pass\n\n')

    # Сохраняем записанную часть файла,
    # затем записываем словарь methods_structure на необходимую строку,
    # после чего записываем сохраненную часть обратно, но уже после словаря methods_structure.
    file.seek(position)
    file_chunk = file.read()
    file.seek(position)
    file.write(tab + 'methods_structure = {}\n\n'.format(methods_structure))
    file.write(file_chunk)


#    print(OBJ.attrib.get('name'), '='*50)
#    pprint(methods_structure)

#        file.write(tab + 'attribs = {}\n'.format(method.attrib))
#        file.write(tab + 'cached = {}\n'.format(cached))
#        file.write(tab + 'comment = {}\n'.format(meth_comment))
#        file.write(tab + 'area_of_sight = {}\n'.format(area_of_sight))
#        file.write(tab + 'returns = {}\n'.format(returns))
#        if isdeclarative:
#            file.write(tab + 'fields = {}\n'.format(fields))
#            file.write(tab + 'sources = {}\n'.format(sources))
#            file.write(tab + 'sortings = {}\n'.format(sortings))
#            file.write(tab + 'filtering_parameters = {}\n'.format(filtering_params))
#            file.write(tab + 'calculatings = {}\n\n'.format(calculatings))
#        file.write(tab + '#########FROM TAG <BODY>#########\n')
#        file.write(indent("'''{} '''".format(method.findtext('definition/body', "dummy_body")) + '\n\n', tab))