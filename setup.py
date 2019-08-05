import sys
import os

system = sys.platform
base_dir = sys.path[0]
flag = False
if len(sys.argv) > 1:
    flag = sys.argv[1] == '--clean'

if system.startswith('win'):
    base_dir += '\\'
    os.system('"%sinstall(win).bat"' % base_dir)
    if flag:
        os.system('del "%sinstall(linux).sh"' % base_dir)
        os.system('del "%sinstall(mac).sh"' % base_dir)
        os.system('del "%sinstall(win).bat"' % base_dir)
        os.system('del "%sstart.sh"' % base_dir)
    exit(0)
elif system.startswith('linux'):
    base_dir += '/'
    os.system('"%sinstall(linux).sh"' % base_dir)
else:
    base_dir += '/'
    os.system('"%sinstall(mac).sh"' % base_dir)
if flag:
    os.system('rm "%sinstall(win).bat"' % base_dir)
    os.system('rm "%sinstall(mac).sh"' % base_dir)
    os.system('rm "%sinstall(linux).sh"' % base_dir)
    os.system('rm "%sexam.bat"' % base_dir)
