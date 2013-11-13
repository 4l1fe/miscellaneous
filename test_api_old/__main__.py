# coding=utf-8
if __name__ == '__main__':
    import sys
    import unittest
    import argparse
    import _xmlrunner
    from os.path import abspath, dirname, split

    sys.path.append('')

    #=============Параметры командной строки.
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--modules', dest='modules', default=[], nargs='*')
    parser.add_argument('-xo', '--xml_output', dest='xml_output', default='',
                        help='Директория, в которую будут выводиться результаты тестов в xml формате.')
    results = parser.parse_args()

    suite = unittest.TestSuite()
    package_dir = (abspath(dirname(__file__)))
    top_level = split(package_dir)[0]

    #=============Добавление тестовых .py файлов, прописанных в консоли.
    if len(results.modules) > 0:
        for mod_name in results.modules:
            mod_name = mod_name if mod_name.endswith('.py') else mod_name + '.py'
            suite.addTest(unittest.TestLoader().discover('test_api', mod_name, top_level_dir=top_level))

    else:  # Добавление всех тестовых .py файлов, не содержащих _ или __ в имени файла.
        all_ = unittest.TestLoader().discover('test_api', '[!_][!_]*', top_level_dir=top_level)
        suite.addTests(all_)

    if results.xml_output:
        _xmlrunner.XMLTestRunner(output=results.xml_output, verbosity=2).run(suite)
    else:
        unittest.TextTestRunner(verbosity=2).run(suite)