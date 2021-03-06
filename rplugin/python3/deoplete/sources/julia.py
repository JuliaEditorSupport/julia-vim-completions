# ============================================================================
# AUTHOR: Lyndon White <lyndon.white at research.uwa.edu.au
# License: MIT license
# ============================================================================

import re
from collections import namedtuple
from os.path import exists, getmtime, getsize
# TODO: replace all use of os.path with pathlib
from pathlib import Path
from .base import Base
import subprocess
import codecs


JULIA_PATH = "julia"
JLTAG_PATH = Path(__file__).resolve().parent.parent.joinpath("jltag.jl")

TagsCacheItem = namedtuple('TagsCacheItem', 'mtime candidates')

def readtagfile(f):
    for line in f:
        if not(line.strip()) or line[0]=='!'  : continue

        entries = line.split("\t")
        try:
            word, file, address = entries[0:3]
            fields = dict([ff.split(":",1) for ff in entries[3:-1]])
            fields = dict([(kk.strip(),vv.strip()) for kk,vv in fields.items()])

            yield {'word':word,
                   'dup':1,
                   'kind':fields.get('kind',""),
                   'menu':fields.get('module',"")+"."+fields.get('string',""),
                   'info':(fields.get('module',"")+"."+fields.get('string',"") + "\n"+
                           codecs.decode(fields.get("doc",""), "unicode-escape"))
                   }
        except ValueError as ee:
            raise(ValueError("On line: " + line +"\n",ee))

def get_refered_tagfiles(vim):
    current_filename = vim.call('expand','%:p')
    jltag_proc = subprocess.Popen([JULIA_PATH, str(JLTAG_PATH), "refer", current_filename],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

    for line in jltag_proc.stderr.readlines():
        output = line.decode('utf-8').strip().replace("'", "''")
        vim.command("echom 'deomplete-julia: Tagger: %s'" % output)

    tagfiles=[line.decode('utf-8').strip() for line in jltag_proc.stdout.readlines()]
    return tagfiles



class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'julia'
        self.mark = '[J]'
        self.filetypes = ['julia']
        self.__cache = {}
        self.vim.command("echom 'deomplete-julia: initialised'")

    def on_event(self, context):
        if 'tag' in context['sources']:
            self.vim.command("echom \"deomplete-julia: Warning: deocomple-source 'tag' and  'julia' probably should not mix.\"")
        self.__make_cache()

    def gather_candidates(self, context):
        if len(self.__cache)==0:
            self.__make_cache()

        candidates = dict()
        for filename in self.__cache.keys():
            for cand in  self.__cache[filename].candidates:
                candidates[cand['word']] = candidates.get(cand['word'],[])
                candidates[cand['word']].append(cand)

        p = re.compile('(?:{})$'.format(context['keyword_patterns']))
        return [cand for word in candidates.keys() if p.match(word) for cand in candidates[word]]


    def __make_cache(self):
        for filename in self.__get_tagfiles():
            mtime = getmtime(filename)
            if filename not in self.__cache or self.__cache[filename].mtime != mtime:
                with open(filename, 'r', errors='replace') as f:
                    tags = list(readtagfile(f))
                    self.vim.command("echom \"deoplete-julia: %s, with %s tags\"" % (filename,len(tags)))
                    self.__cache[filename] = TagsCacheItem(mtime,tags)

        self.vim.command("echom \"deomplete-julia: Cache Made\"")


    def __get_tagfiles(self):
        refered_tagfiles = get_refered_tagfiles(self.vim)

        include_files = self.vim.call(
            'neoinclude#include#get_tag_files') if self.vim.call(
                'exists', '*neoinclude#include#get_tag_files') else []
        return [x for x in self.vim.call(
                'map', self.vim.call('tagfiles') + include_files + refered_tagfiles,
                'fnamemodify(v:val, ":p")')
                if exists(x)]


