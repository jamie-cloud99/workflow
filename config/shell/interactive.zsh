# 僅供互動式 zsh；既有 Oh My Zsh 可先載入，本檔不會再次啟動它。
[[ -o interactive ]] || return 0

() {
  local config_dir=$1 prefix candidate
  local -a prefixes
  prefixes=("${HOMEBREW_PREFIX:-}" /opt/homebrew /usr/local)

  # 新機也能使用補完與歷史；保留既有 shell 的歷史設定。
  if (( ! $+functions[compdef] )); then
    autoload -Uz compinit
    compinit
  fi
  [[ -n $HISTFILE ]] || HISTFILE=${ZDOTDIR:-$HOME}/.zsh_history
  (( HISTSIZE > 0 )) || HISTSIZE=10000
  (( SAVEHIST > 0 )) || SAVEHIST=10000

  # 設定先於主題載入，避免新機啟動設定精靈。
  source "$config_dir/p10k.zsh"
  if (( ! $+functions[p10k] )); then
    for prefix in "${prefixes[@]}"; do
      [[ -n $prefix ]] || continue
      candidate=$prefix/share/powerlevel10k/powerlevel10k.zsh-theme
      if [[ -r $candidate ]]; then
        source "$candidate"
        break
      fi
    done
  fi

  if (( $+commands[fzf] && ! $+functions[fzf-history-widget] )); then
    source <(fzf --zsh)
  fi
  if (( $+commands[zoxide] && ! $+functions[__zoxide_z] )); then
    eval "$(zoxide init zsh)"
  fi
  if (( ! $+functions[_zsh_autosuggest_start] )); then
    for prefix in "${prefixes[@]}"; do
      [[ -n $prefix ]] || continue
      candidate=$prefix/share/zsh-autosuggestions/zsh-autosuggestions.zsh
      if [[ -r $candidate ]]; then
        source "$candidate"
        break
      fi
    done
  fi
} "${${(%):-%x}:A:h}"

return 0
