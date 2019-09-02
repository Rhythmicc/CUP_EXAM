import sys
import os


def remove_command():
    with open('~/.bashrc', 'r') as f:
        content = f.readlines()
    with open('~/.bashrc', 'w') as f:
        for line in content:
            if not line.strip():
                continue
            if line.split()[-1].startswith('exam='):
                continue
            f.write(line + '\n')


system = sys.platform
base_dir = sys.path[0]
if system.startswith('win'):
    dir_char = '\\'
else:
    dir_char = '/'
base_dir += dir_char
flag = False

if len(sys.argv) > 1:
    flag = sys.argv[1] == '--clean' or sys.argv[1] == '--direct'

if system.startswith('win'):
    if sys.argv[1] != '--direct':
        os.system('setx /m PATH %%PATH%%;%s;' % base_dir)
    else:
        base_dir += dir_char
        os.remove(base_dir + 'exam.sh')
else:
    remove_command()
    if sys.argv[1] != '--direct':
        os.system('echo alias exam="%sexam.sh"' % base_dir)
    else:
        os.remove(base_dir + 'exam.bat')
if flag:
    os.remove('%sinstall(win).bat' % base_dir)
    os.remove('%sinstall.sh' % base_dir)
    os.removedirs('%simg/' % base_dir)
    os.remove('%sREADME.md' % base_dir)
    os.remove('%s.last_title.txt' % base_dir)
    os.remove('%scontent.xls' % base_dir)
    os.removedirs('%s.idea/' % base_dir)
