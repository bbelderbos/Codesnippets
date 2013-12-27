set nocompatible
set history=10000
set cursorline
set autoindent
" make searches case-sensitive only if they contain upper-case characters
set ignorecase smartcase
" search highlighting
set hls is
set incsearch
" no tabs, I like 2 spaces for indenting
set tabstop=2
set expandtab
set shiftwidth=2
set shiftround
" tell vim to remember certain things when we exit
set viminfo='10,\"100,:20,%,n~/.viminfo
filetype plugin on 
syntax on
let mapleader = ","
" no arrow keys allowed, I have to use hjkl keys !!
noremap <Up> <Nop> 
noremap <Down> <Nop> 
noremap <Left> <Nop> 
noremap <Right> <Nop>
noremap \ ,
" clears the search buffer
nnoremap <silent> <C-l> :nohl<CR><C-l>
" extend * search on visual selection - see practical vim ch13 (last tip)
xnoremap * :<C-u>call <SID>VSetSearch()<CR>/<C-R>=@/<CR><CR> 
xnoremap # :<C-u>call <SID>VSetSearch()<CR>?<C-R>=@/<CR><CR>

function! s:VSetSearch()
  let temp = @s
  norm! gv"sy
  let @/ = '\V' . substitute(escape(@s, '/\'), '\n', '\\n', 'g') 
  let @s = temp
endfunction

function! ResCur()
  if line("'\"") <= line("$")
    normal! g`"
    return 1
  endif
endfunction

augroup resCur
  autocmd!
  autocmd BufWinEnter * call ResCur()
augroup END

" shows number of search hits
nmap ,c :%s///gn<CR>
" saves + executes scripts
nmap ,p :w<CR>:!python %<CR>
nmap ,b :w<CR>:!bash %<CR>
nmap ,h :w<CR>:!php %<CR>
nmap ,r :w<CR>:!ruby %<CR>
" opens the file under cursor in new vertical split window
nmap gf :vertical wincmd f<CR>
" opens vimrc in vert. split window
nmap ,v :vsp ~/.vimrc<CR>

" the following shortcuts require the conque plugin
" open programs in new vertical split window:
nmap cp :ConqueTermVSplit python<CR>
" open phpsh (fb devs) in split terminal
nmap ch :ConqueTermVSplit phpsh<CR>
" search github code in Vim vertical split window
nmap ,g :ConqueTermVSplit python /Users/bbelderbos/CODE/codesnippets/python/github_search.py<CR>
" search stack overflow Q&A in Vim vertical split window
nmap ,s :ConqueTermVSplit python /Users/bbelderbos/CODE/codesnippets/python/stackoverflow_cli_search.py<CR>

" ignore spam
set wildignore=*.swp,*.bak,*.pyc,*.class,*.jar,*.gif,*.png,*.jpg
" open all folds
set foldlevel=99

" install plugins and runtime files in their own private directories.
call pathogen#infect()

" save with ctrl+s
:nmap <c-s> :w<CR>
:imap <c-s> <Esc>:w<CR>a
:imap <c-s> <Esc><c-s>

" reload .vimrc in current session
:nmap vc :so $MYVIMRC<CR>
