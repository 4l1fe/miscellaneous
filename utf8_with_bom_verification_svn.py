import sys
import subprocess
from codecs import BOM_UTF8



REQ_EXTS = ['.c', '.h', '.cpp', '.hpp', '.test']


def svnlook_changed(transaction, repo):
    cmd = r'"C:\Program Files (x86)\VisualSVN Server\bin\svnlook.exe" changed -t {} "{}" '.format(transaction, repo)
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return pipe.stdout.readlines()


def svnlook_cat(repo, path_in_repo, transaction):
    cmd = r'"C:\Program Files (x86)\VisualSVN Server\bin\svnlook.exe" cat -t {} "{}" "{}"'.format(transaction, repo, path_in_repo)
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=3) # Для проверки нам нужны первые 3 байта.
    return pipe.communicate()[0]


def main():
    repo = sys.argv[1]
    transaction = sys.argv[2]
    output = svnlook_changed(transaction, repo)

    file_statuses_names = []
    for line in output:
        line = line.decode('cp1251')
        file_status = line[:4]
        file_name = line[4:].rstrip('\r\n')
        file_statuses_names.append((file_status, file_name))

    error_template = '\n\n==============================================================\n'
    error_template += 'Содержатся файлы с кодировкой отличной от "utf-8 with BOM"\n'
    has_invalid_encoding = False
    for file_status, file_name in file_statuses_names:
        if file_name.startswith('trunk') and any([file_name.endswith(ext) for ext in REQ_EXTS]):
            if file_status.startswith('D'):
                continue
            if file_name.startswith('trunk/tools/Jinnee'):
                continue
            content = svnlook_cat(repo, file_name, transaction)
            if not content.startswith(BOM_UTF8):
                error_template += file_name + '\n'
                has_invalid_encoding = True
    error_template += '==============================================================\n\n'

    if has_invalid_encoding:
        sys.stderr.write(error_template)
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()