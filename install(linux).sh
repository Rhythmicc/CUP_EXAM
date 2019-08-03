# shellcheck disable=SC2046
basedir=$(cd $(dirname "$0") || exit; pwd -P)
chmod a+x "$basedir"/frontend.py
chmod 777 "$basedir"/start.sh
file1="$HOME/.bashrc"
# shellcheck disable=SC2088
file2="$HOME/.profile"
if [ ! -f "$file1" ]; then
  touch "$HOME/.bashrc"
fi

if [ ! -f "$file2" ]; then
  touch "$HOME/.profile"
fi

sed '$a\alias exam="$basedir/start.sh"' ~/.bashrc
sed '$a\alias exam="$basedir/start.sh"' ~/.profile
# shellcheck disable=SC1090
source ~/.bashrc
# shellcheck disable=SC1090
source ~/.profile
