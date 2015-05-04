#!/usr/bin/env python
#-*- coding: utf-8 -*-
import argparse
import os
import time
import math
import re
import shutil
import sys

# const define
BLOGPATH  = './blogs/'
TAGSPATH  = './tags/'
TAGTEMP   = './template/tag.md'
INDEXTEMP = './template/index.md'
LINK_BASE = 'https://github.com/yimun/Blog/tree/master/'
TAGS_PATTERN = '(?<!`)``([^`]+?)``(?!`)'
INDEX_FILE = "./README.md"




def getTags(file):
    ''' 
    fetch tags in file 
    '''
    pattern = re.compile(TAGS_PATTERN)
    content = unicode(open(file,'r').read(),'utf8')
    match = pattern.findall(content)
    return match

def buildCatalogUrl(item):
    ''' 
    build catalog url use file item
    '''
    return '- [' + item['name'] + '](' + LINK_BASE + item['filepath'][2:] + ')\n'

def buildTagUrl(tagname):
    ''' 
    build tag url use tag name
    '''
    return '[``' + tagname + '``](' + LINK_BASE + 'tags/' + tagname + '.md) '


def update(blogpath):

    # get tags from data files
    tagsmap = {}
    dirlist = [{'filepath':os.path.join(blogpath,item)+"/README.md",'name':item,\
        'time':os.path.getatime(os.path.join(blogpath,item)+"/README.md")} for item in os.listdir(blogpath)]
    print 'Total %d blogs has found...' % len(dirlist)
    for dir in dirlist:
        tags = getTags(dir['filepath'])
        for tag in tags:
            if not tag in tagsmap.keys():
                tagsmap[tag] = []
            tagsmap[tag].append(dir)
    print 'updating tags file...'
    # delete tags files
    if os.path.exists(TAGSPATH):
        shutil.rmtree(TAGSPATH)
    os.mkdir(TAGSPATH)
    # build tag files
    tag_temp = unicode(open(TAGTEMP).read(),'utf8')
    for key in tagsmap.keys():
        title = key
        catalog = ''
        for item in tagsmap[key]:
            catalog += buildCatalogUrl(item)
        s =  tag_temp.replace(u'{%title%}',title)
        s = s.replace('{%catalog%}',unicode(catalog,'gbk')) # windows默认的目录名都是gbk
        f = open(TAGSPATH + title + ".md",'w')
        f.write(s)
        f.close()
    print 'tags file updated ok!'
    print 'updating index file...'
    # delete index file 
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)
    # build index files
    index_temp = unicode(open(INDEXTEMP).read(),'utf8')
    catalog = ''
    tags = ''
    newest = ''
    for dir in dirlist:
        catalog += buildCatalogUrl(dir)
    for key in tagsmap.keys():
        tags += buildTagUrl(key)
    dirlist.sort(key = lambda dir : dir['time'],reverse = True)
    for dir in dirlist[:3]:
        newest += buildCatalogUrl(dir)

    s = index_temp.replace('{%catalog%}',unicode(catalog,'gbk'))
    s = s.replace('{%newest%}',unicode(newest,'gbk'))
    s = s.replace('{%tags%}',tags)
    f = open(INDEX_FILE,'w')
    f.write(s)
    f.close()
    print 'index file updated ok!'


def initMenu():
    parser = argparse.ArgumentParser(description='Yimu Blog auto indexing tools')
    parser.add_argument('action',help="action to do[add,update]")
    parser.add_argument('arg',nargs='?',help="action args") #0 or 1 
    return vars(parser.parse_args())


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    args = initMenu()
    if args['action'] == 'add':
        print 'doadd'
    if args['action'] == 'update':
        if not args['arg']:
            update(BLOGPATH)
        else:
            update(args['arg'])


        

