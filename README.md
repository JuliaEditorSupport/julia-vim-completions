# Deoplete-Julia 
This package supplimentes julia-vim by providing syntax competions, through Deoplete.

## WIP
This package is functional, but not, right now easily installed.


## Requirements:

 - [NeoVim](https://github.com/neovim/neovim)
 - [Deoplete](https://github.com/Shougo/deoplete.nvim)
 
 
## Installation
 - WIP: Use faverate Vim package manager, eg Vundle.
 
Set your `.vimrc` config up to use this new source -- add something like (you should already have the first line)

```
let g:deoplete#enable_at_startup = 1
let g:deoplete#sources = {}
let g:deoplete#sources._ = ['julia','buffer','member','dictionary','omni','file']
```

The first time a you `using` a module, will take a little longer as it caches the names from that module (in particular the first time you edit a file at all will take longer, as it builds the cache of names for `Base`).
This cache should rebuild when the module is editted.

You shouldn't notice the cache being generated -- it won't hang, but julia completions will not work til it is done.

## Demo

Check out the video of it working. (Click the image below)
[![asciicast](https://asciinema.org/a/688g8iyhj1idrtz8ooptr6iso.png)](https://asciinema.org/a/688g8iyhj1idrtz8ooptr6iso)
(Yes, I know that code is not actually correct. Recording demos is hard.)
