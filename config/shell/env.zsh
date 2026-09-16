# 由 ~/.zshrc 引用。重複載入時不重複加入 PATH。
export VOLTA_HOME="$HOME/.volta"
export VOLTA_FEATURE_PNPM=1
typeset -U path PATH
path=("$VOLTA_HOME/bin" "$HOME/.local/bin" /opt/homebrew/bin /usr/local/bin $path)
export PATH
