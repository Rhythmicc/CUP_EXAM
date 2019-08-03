# shellcheck disable=SC2046
basedir=$(cd $(dirname "$0") || exit; pwd -P)
chmod a+x "$basedir"/frontend.py
chmod 777 "$basedir"/start.sh
sed -i '' "\$a \\
alias exam=\"$basedir/start.sh\"
" ~/.bashrc
# shellcheck disable=SC1090
source ~/.bashrc
