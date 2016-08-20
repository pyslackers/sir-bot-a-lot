export LANG="en_US.UTF-8"
export LC_COLLATE="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
export LC_MESSAGES="en_US.UTF-8"
export LC_MONETARY="en_US.UTF-8"
export LC_NUMERIC="en_US.UTF-8"
export LC_TIME="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"

addPath() {
    export PATH="${1}:${PATH}"
}

# default paths
export PATH="/usr/bin:/bin:/usr/sbin:/sbin"

# make sure /usr/local is before system
if [ -d /usr/local/bin ]; then
    addPath "/usr/local/sbin"
    addPath "/usr/local/bin"
fi

# add home bin
if [ -d $HOME/bin ]; then
    addPath "$HOME/bin"
fi
