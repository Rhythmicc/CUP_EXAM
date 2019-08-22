basedir=$(cd "$(dirname "$0")" || exit; pwd -P)
chmod a+x "$basedir"/frontend.py
chmod 777 "$basedir"/start.sh
file="$HOME/.bashrc"

# shellcheck disable=SC2016
echo alias exam=\""$basedir"/start.sh\" >> "$file"
# shellcheck disable=SC1090
source "$file"
