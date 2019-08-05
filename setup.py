import sys
import os

system = sys.platform
if system.startswith('win'):
    os.system('".\\install(win).bat"')
elif system.startswith('linux'):
    os.system('"./install(linux).sh"')
else:
    os.system('"./install(mac).sh"')
