FROM python:3.5-alpine
MAINTAINER Shawn McElroy "shawn@skift.io"

RUN apk add --no-cache \
    build-base \
    curl \
    gcc \
    git \
    libffi-dev \
    python3-dev \
    openssl \
    openssl-dev \
    vim \
    zsh && \
    mkdir -p /root/.vim-backups/backup/ && \
    mkdir -p /root/.vim-backups/swp/ && \
    mkdir -p /root/.vim/bundle

ADD ./.zshrc /root/.zshrc
ADD ./.zshenv /root/.zshenv
ADD ./.vimrc /root/.vimrc

RUN git clone https://gitlab.com/VundleVim/Vundle.vim.git /root/.vim/bundle/Vundle.vim && \
    git clone https://gitlab.com/zsh-users/antigen.git /root/.antigen

ENV SHELL=/bin/zsh
ENV HOME=/root
