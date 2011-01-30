#!/usr/bin/env python

import re, time, sys

line_terminators = ('\r\n', '\n', '\r')

def follow(logfile, delay=1.0):
    trailing = True
    
    while 1:
        where = logfile.tell()
        line = logfile.readline()
        if line:
            if trailing and line in line_terminators:
                trailing = False
                continue

            if line[-1] in line_terminators:
                line = line[:-1]
                if line[-1:] == '\r\n':
                    line = line[:-1]

            trailing = False
            yield line
        else:
            trailing = True
            logfile.seek(where,0)
            time.sleep(delay)

def main(opt):
    

    logfile  = open(opt.file, 'rb')

    listfile = open(opt.list, 'rb')
    list=[]
    list_line = listfile.readline()
    while(list_line):
        list.append(list_line.strip('\r\n'))
        list_line = listfile.readline()

        line_num = 0
        try:
            for line in follow(logfile):
                line_num = line_num + 1
                for key in list:
                    if re.search(key, line):
                        print "%s: %s" %(line_num, line)
        finally:
            logfile.close()

if __name__=='__main__':
    from optparse import OptionParser

    opt = OptionParser()
    opt.add_option('-f', '--file', dest='file', type='string', action='store',
                   help='log file to watch')
    opt.add_option('-l', '--list', dest='list', type='string', action='store',
                   helo='regex to catch')
    
    (opt, args) = opt.parse_args()
    
#    if opt.file and opt.list
#        main(opt)
#    else:   
    opt.print_help()
