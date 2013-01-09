set nocompatible
set history=10000
set cursorline
set autoindent
" make searches case-sensitive only if they contain upper-case characters
set ignorecase smartcase
" search highlighting
set hls is
set incsearch
" no tabs, but 2 spaces as indenting
set tabstop=2
set expandtab
set shiftwidth=2
set shiftround
" Tell vim to remember certain things when we exit
set viminfo='10,\"100,:20,%,n~/.viminfo
filetype plugin on 
syntax on
let mapleader = ","
" no arrow keys allowed
noremap <Up> <Nop> 
noremap <Down> <Nop> 
noremap <Left> <Nop> 
noremap <Right> <Nop>
noremap \ ,
nnoremap <silent> <C-l> :nohl<CR><C-l>
" extend * search on visual selection
" from practical vim ch13 (last tip)
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

" handy shortcuts
nmap ,c :%s///gn<CR>
nmap ,p :w<CR>:!python %<CR>
nmap ,h :w<CR>:!php %<CR>
nmap ,r :w<CR>:!ruby %<CR>
nmap gf :vertical wincmd f<CR>
nmap ,v :vsp ~/.vimrc<CR>

" requires conque plugin
nmap cp :ConqueTermVSplit python<CR>
nmap ,g :ConqueTermVSplit python /Users/bbelderbos/CODE/codesnippets/python/github_search.py<CR>
nmap ,s :ConqueTermVSplit python /Users/bbelderbos/CODE/codesnippets/python/stackoverflow_cli_search.py<CR>
