"""Сценарий выполняет автоматизацию ответа на вопросы,
когда происходит инициализация окружения для sphinx по команде sphinx-quickstart"""
import subprocess
import argparse
import os


def main(sphinx_dir, platform_version):
    command = 'sphinx-quickstart {sphinx_dir}'.format(sphinx_dir=sphinx_dir)
    child_proc = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    answers = 'n{linesep}'
    answers += '_{linesep}'
    answers += 'СБиС{linesep}'
    answers += 'Краснов{linesep}'
    answers += '{platform_version}{linesep}'
    answers += '{platform_version}{linesep}'
    answers += '.rst{linesep}'
    answers += 'index{linesep}'
    answers += 'n{linesep}'
    answers += 'n{linesep}'
    answers += 'n{linesep}'
    answers += 'n{linesep}'
    answers += 'n{linesep}'
    answers += 'n{linesep}'
    answers += 'n{linesep}'
    answers += 'n{linesep}'
    answers += 'n{linesep}'
    answers += 'n{linesep}'
    answers += 'y{linesep}'
    answers += 'y{linesep}'
    answers = answers.format(linesep=os.linesep, platform_version=platform_version)

    try:
        outs, errs = child_proc.communicate(answers.encode('cp1251'), timeout=10)
        print(outs.decode())
    except subprocess.TimeoutExpired:
        child_proc.kill()
        print('error - TimeoutExpired')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-sd', '--sphinx_dir', action='store', type=str, dest='sphinx_dir', required=True)
    parser.add_argument('-pv', '--platform_version', action='store', type=str, dest='platform_version', required=True)
    result = parser.parse_args()

    main(result.sphinx_dir, result.platform_version)