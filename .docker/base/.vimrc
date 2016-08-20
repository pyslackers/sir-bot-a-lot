" Use Vim settings, rather than Vi settings (much better!).
" This must be first, because it changes other options as a side effect.
set nocompatible
filetype off
syntax enable
let g:solarized_termtrans = 1

"colorscheme mustang
set hidden
set splitbelow
set splitright

set encoding=utf-8



""""""""""
""" KEY REMAPS
""""""""""

" change leader
let mapleader=","
" remap : to ; -- making things easier on myself
nnoremap ; :

" make hjkl navigation more natural with line wraps
nnoremap j gj
nnoremap k gk

" Use Q for formatting the current paragraph (or selection)
vmap Q gq
vmap Q gq
nmap Q gqap

" Easy window navigation
map <C-h> <C-w>h
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-l> <C-w>l

" Clear the search highlighting when pressing ,/
nmap <silent> ,/ :nohlsearch<CR>

" forget to use sudo to edit a file?
cmap w!! w !sudo tee % >/dev/null

" GO AWAY <F1> help key
inoremap <F1> <ESC>
nnoremap <F1> <ESC>
vnoremap <F1> <ESC>

" save when losing focus
au FocusLost * :wa

" html and code folding
set foldmethod=indent
set foldlevel=99
"nnoremap <leader>ft Vatzf " Visual all in tag fold
nnoremap <space> za

" organize css props
nnoremap <leader>S ?{<CR>jV/^\s*\}?$<CR>k:sort<CR>:noh<CR>

" reformat paragraphs
nnoremap <leader>q gqip

" reselect text that was just pasted to perform operations like indentation on
" it
nnoremap <leader>v V`]

" open vimrc on the fly
nnoremap <leader>ev <C-w><C-v><C-l>:e $MYVIMRC<cr>

" make it easier to get back into normal mode
inoremap jj <ESC>

" make it easier to tab through the buffers
nnoremap <leader>b :bn<CR>

" using ack
nnoremap <leader>a :Ack

" Yank text to clipboard
set clipboard=unnamed
noremap <leader>y "*y
noremap <leader>yy "*Y

" Preserve indentation while pasting text from the OS X clipboard
noremap <leader>p :set paste<CR>:put  *<CR>:set nopaste<CR>

"" SPLITS
" easily split the vim window
nnoremap <leader>wh <C-w>s
nnoremap <leader>wv <C-w>v
nnoremap <Leader><Left> <C-w><
nnoremap <Leader><Right> <C-w>>
nnoremap <Leader><Up> <C-w>+
nnoremap <Leader><Down> <C-w>-
"Max out the height of the current split
" ctrl + w _
"Max out the width of the current split
" ctrl + w |
"Normalize all split sizes, which is very handy when resizing terminal
" ctrl + w =

"Swap top/bottom or left/right split
" Ctrl+W R
"Break out current window into a new tabview
" Ctrl+W T
"Close every window in the current tabview but the current one
" Ctrl+W o

" Change between buffers
nnoremap gn :bn<CR>
nnoremap gp :bp<CR>
nnoremap gd :bd<CR>

" changing tabs
noremap th :tabnext<CR>
noremap tl :tabprev<CR>
nnoremap tn :tabnew<CR>

"" END SPLITS
""""""""""
""" END KEY REMAPS
""""""""""


""""""""""
""" EDITING
""""""""""
"highlight OverLength ctermbg=Black ctermfg=DarkRed guibg=#592929
"match OverLength /\%81v.\+/
" some basic settings. some were derived from the links below
" http://nvie.com/posts/how-i-boosted-my-vim/
set autoindent
set copyindent       " copy the previous indentation on autoindenting
set cursorline
set expandtab
set fileformat=unix
set hlsearch         " highlight searchsearch terms
set ignorecase       " ignore case when searching
set modelines=0      " not using modelines. disable it.
set nobackup         " dont use backup files
set noswapfile       " dont use the swap files
set pastetoggle=<F2> " use <F2> to toggle paste mode
set rnu              " set relative line numbers on start
set nu
set scrolloff=15     " keep the search results in view when searching. like 'zz'
set shiftround       " use multiple of shiftwidth when indenting with '<' and '>'
set shiftwidth=4     " number of spaces to use for autoindenting
set showcmd
set showmatch        " set show matching parenthesis
set smartcase        " ignore case if search pattern is all lowercase,
                     "     case-sensitive otherwise
set smarttab         " insert tabs on the start of a line according to
                     "     shiftwidth, not tabstop
set softtabstop=4
set t_Co=256
let &t_AB="\e[48;5;%dm"
let &t_AF="\e[38;5;%dm"
set tabstop=4        " a tab is four spaces
set textwidth=79
set ttyfast
set undofile
set undolevels=1000  " use many muchos levels of undo
set visualbell
set wildignore=*.swp,*.bak,*.pyc,*.class

" JS Specific tab settings
au BufNewFile,BufRead *.js, *,json, *,ts
    \ set tabstop=2
    \ set softtabstop=2
    \ set shiftwidth=2

" use real regex
" http://stevelosh.com/blog/2010/09/coming-home-to-vim/
nnoremap / /\v
vnoremap / /\v

" use <tab> to switch between matching braces instead of %
nnoremap <tab> %
vnoremap <tab> %

" auto reload vimrc when saved
au BufWritePost .vimrc so ~/.vimrc

augroup vimrc_autocmds
    autocmd!
    " highlight characters past column 120
    autocmd FileType python highlight Excess ctermbg=DarkGrey guibg=Black
    autocmd FileType python match Excess /\%79v.*/
    autocmd FileType python set nowrap
    augroup END

""""""""""
""" END EDITING
""""""""""

if has("vms")
  set nobackup		" do not keep a backup file, use versions instead
else
  set backup		" keep a backup file
endif

set backupdir=~/.vim-backups/backup//
set directory=~/.vim-backups/swp//

" CTRL-U in insert mode deletes a lot.  Use CTRL-G u to first break undo,
" so that you can undo CTRL-U after inserting a line break.
inoremap <C-U> <C-G>u<C-U>

" In many terminal emulators the mouse works just fine, thus enable it.
if has('mouse')
  set mouse=a
endif

" Switch syntax highlighting on, when the terminal has colors
" Also switch on highlighting the last used search pattern.
if &t_Co > 2 || has("gui_running")
  syntax on
  set hlsearch
endif

" Only do this part when compiled with support for autocommands.
if has("autocmd")
  " trim whitespace on save
  autocmd BufWritePre * :%s/\s\+$//e

  " Put these in an autocmd group, so that we can delete them easily.
  augroup vimrcEx
  au!

  " For all text files set 'textwidth' to 78 characters.
  autocmd FileType text setlocal textwidth=78

  " When editing a file, always jump to the last known cursor position.
  " Don't do it when the position is invalid or when inside an event handler
  " (happens when dropping a file on gvim).
  " Also don't do it when the mark is in the first line, that is the default
  " position when opening a file.
  autocmd BufReadPost *
    \ if line("'\"") > 1 && line("'\"") <= line("$") |
    \   exe "normal! g`\"" |
    \ endif

  augroup END

endif " has("autocmd")

" Convenient command to see the difference between the current buffer and the
" file it was loaded from, thus the changes you made.
" Only define it when not defined already.
if !exists(":DiffOrig")
  command DiffOrig vert new | set bt=nofile | r # | 0d_ | diffthis
          \ | wincmd p | diffthis
endif

""""""""""
""" END MISC
""""""""""

"""""""""
""" GVIM CONFIG
"""""""""
if has("gui_running")
  if has("gui_gtk2")
    set guifont=Source\ Code\ Pro
  elseif has("gui_photon")
    set guifont=Courier\ New:s11
  elseif has("gui_kde")
    set guifont=Courier\ New/11/-1/5/50/0/0/0/1/0
  elseif has("x11")
    set guifont=-*-courier-medium-r-normal-*-*-180-*-*-m-*-*
  else
    set guifont=Courier_New:h11:cDEFAULT
  endif
endif
""""""""""
""" END GVIM CONFIG
""""""""""

""""""""""
""" VUNDLE
""""""""""
" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" alternatively, pass a path where Vundle should install plugins
call vundle#begin('~/.vim/plugins')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'

""""""""""
""" END VUNDLE
""""""""""


""""""""""
""" PLUGIN CONFIG
""""""""""
Plugin 'jmcantrell/vim-virtualenv'

Plugin 'tmhedberg/SimpylFold'
let g:SimpylFold_docstring_preview=1

Plugin 'ntpeters/vim-better-whitespace'

Plugin 'nvie/vim-flake8'
if has("autocmd")
    autocmd BufWritePost *.py call Flake8()
endif
let python_highlight_all=1
let g:flake8_show_in_file=1
let g:flake8_show_in_gutter=1

Plugin 'ctrlpvim/ctrlp.vim'

Plugin 'tpope/vim-fugitive'

"Plugin 'godlygeek/tabular'
"Plugin 'plasticboy/vim-markdown'
"let g:vim_markdown_frontmatter = 1
"let g:vim_markdown_json_frontmatter = 1

Bundle 'Rykka/riv.vim'

""""""""""
""" END PLUGIN CONFIG
"""""""""

let g:CSSLint_FileTypeList = ['css', 'less']

" Custom enhancements
syntax on
filetype on
filetype plugin on
filetype plugin indent on

" this must be defined after the plugins
call vundle#end()
filetype plugin indent on
