import subprocess
import argparse


def main(sphinx_dir):
    command = 'sphinx-quickstart {}'.format(sphinx_dir)
    child_proc = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    answers = 'n{0}'
    answers += '_{0}'
    answers += 'СБиС{0}'
    answers += 'Краснов, Шувалова{0}'
    answers += '3.6.0{0}'
    answers += '3.6.0{0}'
    answers += '.rst{0}'
    answers += 'index{0}'
    answers += 'n{0}'
    answers += 'n{0}'
    answers += 'n{0}'
    answers += 'n{0}'
    answers += 'n{0}'
    answers += 'n{0}'
    answers += 'n{0}'
    answers += 'n{0}'
    answers += 'n{0}'
    answers += 'n{0}'
    answers += 'y{0}'
    answers += 'y{0}'
    answers = answers.format('\r\n')

    try:
        outs, errs = child_proc.communicate(answers.encode('cp1251'), timeout=10)
        print(outs.decode())
    except subprocess.TimeoutExpired:
        child_proc.kill()
        print('error - TimeoutExpired')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-sd', '--sphinx_dir', action='store', type=str, dest='sphinx_dir', required=True)
    result = parser.parse_args()

    main(result.sphinx_dir)