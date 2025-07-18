" https://chatgpt.com/share/68238028-b084-8008-a306-848b87788229
" To use: 
" :source /full/path/to/fix.vim
" :FixDoc 
" can search for dash types (hard to visually distinguish) as follows:
" /\%u2014   " em-dash
" /\%u2013   " en-dash
" /\%u002D   " hyphen-minus
" see the chat GPT chat above for ideas on syntax highlighting

function! Doc2Markdown()
  " Convert dash between numbers to en-dash
  " %s/\(\d\+\)\s*-\s*\(\d\+\)/\1–\2/g

  " Convert double dash or single dash between words to em-dash
  " %s/\(\w\)\s*--\s*\(\w\)/\1 — \2/g
  " %s/\(\w\)\s*-\s*\(\w\)/\1 — \2/g

  " Normalize smart double quotes and smart apostrophes
  %s/[“”]/"/g
  %s/[‘’]/'/g " these show up in filenames so leave them alone

  " Replace two or more spaces after period with one space
  " %s/\.  \+/. /g

  " Normalize ellipses
  " %s/\. *\. *\. */…/g

  " Remove form feed (page break) characters
  " %s/\%x0c//g

  " Convert code for italics into markdown italics
  " %s/<I>/\*/g
  " %s/<D>/\*/g
endfunction

command! FixDoc call Doc2Markdown()

