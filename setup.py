import sys
import os

system = sys.platform
base_dir = sys.path[0]

if system.startswith('win'):
    base_dir += '\\'
    os.system('"%sinstall(win).bat"' % base_dir)
elif system.startswith('linux'):
    base_dir += '/'
    os.system('"%sinstall(linux).sh"' % base_dir)
else:
    base_dir += '/'
    os.system('"%sinstall(mac).sh"' % base_dir)
