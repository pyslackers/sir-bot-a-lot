#!/usr/local/env zsh

# Set up the prompt
setopt histignorealldups sharehistory

# vi style incremental search
bindkey '^R' history-incremental-search-backward
bindkey '^S' history-incremental-search-forward
bindkey '^P' history-search-backward
bindkey '^N' history-search-forward

# Keep 1000 lines of history within the shell and save it to ~/.zsh_history:
HISTSIZE=1000
SAVEHIST=1000
HISTFILE=~/.zsh_history

# for vim stuff
set editing-mode vi
export MYVIMRC=${MYVIMRC:-"$HOME/.vimrc"}
export EDITOR=${EDITOR:-'vim'}

# Uncomment the following line to display red dots whilst waiting for completion.
COMPLETION_WAITING_DOTS="true"

# You may need to manually set your language environment
export LANG=${LANG:-'en_US.UTF-8'}

#
# ANTIGEN
#
ANTIGEN=${ANTIGEN:-${HOME}/.antigen/}
if [ -d "${ANTIGEN}" ] && [ -f "${ANTIGEN}/antigen.zsh" ]; then
    source $HOME/.antigen/antigen.zsh

    # Load the oh-my-zsh's library.
    antigen use oh-my-zsh

    antigen bundle git
    # Load the theme.
    antigen theme bureau
    antigen bundle pip
    antigen bundle python
    antigen bundle virtualenv
    antigen bundle tmuxinator
    antigen bundle command-not-found

    # Syntax highlighting bundle.
    antigen bundle zsh-users/zsh-syntax-highlighting

    # Tell antigen that you're done.
    antigen apply

fi

# local config for this system
if [ -f "${HOME}/.zshrc_after" ]; then
    source "${HOME}/.zshrc_after"
fi
