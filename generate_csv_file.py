import argparse
import subprocess
from time import sleep


def generate(sbis_exe, prg_file):
    command = r'''{sbis_exe} "/fx:ЗагрузитьФункции(""{prg_file}""); КолвоЗаданий();" '''.format(sbis_exe=sbis_exe,
                                                                                                prg_file=prg_file)
    subprocess.Popen(command)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sbis_exe', dest='sbis_exe')
    parser.add_argument('-cf', '--csv_file', dest='csv_file')
    parser.add_argument('-prg', '--prg_file', dest='prg_file')
    parser.add_argument('-stm', '--sbis_exe_timeout', dest='sbis_exe_timeout', type=int)
    result = parser.parse_args()
    #result = parser.parse_args(['-s', 'C:\\Users\\dv.krasnov\\СБиС2\\sbis.exe', '-p', 'D:\\\download\\\Список из сбис\\\Кол_воЗаданий.prg', '-stm', '240'])  # тройные слыши нужно обязательно
    print(result.sbis_exe, result.prg_file)

    while True:
        generate(result.sbis_exe, result.prg_file)
        sleep(result.sbis_exe_timeout)