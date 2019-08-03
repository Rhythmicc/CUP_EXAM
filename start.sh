# shellcheck disable=SC2046
basedir=$(cd $(dirname "$0") || exit; pwd -P)
"$basedir"/frontend.py &
