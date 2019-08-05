# shellcheck disable=SC2046
basedir=$(cd $(dirname "$0") || exit; pwd -P)
chmod a+x "$basedir"/frontend.py
chmod 777 "$basedir"/start.sh
file="$HOME/.bashrc"
# shellcheck disable=SC2088
if [ ! -f "$file" ]; then
  file="$HOME/.profile"
fi

sed '$a alias exam="$basedir/start.sh"' "$file"
# shellcheck disable=SC1090
source "$file"
