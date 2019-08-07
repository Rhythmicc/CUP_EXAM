import sys
import os


def remove_command():
    os.system('cat ~/.bashrc > tmp')
    with open('tmp', 'r') as f:
        content = f.readlines()
    with open('tmp', 'w') as f:
        for line in content:
            if not line.strip():
                continue
            if line.split()[-1].startswith('exam='):
                continue
            f.write(line + '\n')
    os.system('cat tmp > ~/.bashrc')
    os.system('rm tmp')


system = sys.platform
base_dir = sys.path[0]
flag = False
if len(sys.argv) > 1:
    flag = sys.argv[1] == '--clean'

if system.startswith('win'):
    base_dir += '\\'
    os.system('"%sinstall(win).bat"' % base_dir)
    if flag:
        os.system('del "%sinstall.sh"' % base_dir)
        os.system('del "%sinstall(win).bat"' % base_dir)
        os.system('del "%sstart.sh"' % base_dir)
    exit(0)
else:
    remove_command()
    base_dir += '/'
    os.system('"%sinstall.sh"' % base_dir)
if flag:
    os.system('rm "%sinstall(win).bat"' % base_dir)
    os.system('rm "%sinstall.sh"' % base_dir)
    os.system('rm "%sexam.bat"' % base_dir)
