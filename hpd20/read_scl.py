#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


def read_scale(file_name):
    fh = file(file_name, "r")
    text = fh.read()
    lines = text.splitlines()
    state = 0
    items = [1.0]
    items_org = ['1/1']
    for line in lines:
        if len(line):
            line = line.strip()
            if line[0] == '!':
                continue
            if state == 0:
                comment = line
                state = 1
            elif state == 1:
                count = int(line)
                state = 2
            elif state == 2:
                items_org.append(line)
                ratio = line.split('/')
                if len(ratio) == 2:
                    value = float(ratio[0])/float(ratio[1])
                else:
                    value = float(line)
                items.append(value)
    print ("    ['"+file_name+"',");
    print ("        '"+comment+"',");
    print ("        "+str(count) + ",");
    print ("        "+str(items_org));
    print ("        "+str(items));
    print ("    ],")
    return [file_name, comment, count+1, items_org, items]

if __name__ == "__main__":

    for index, item in enumerate(sys.argv[1:]):
        __ = read_scale(sys.argv[index+1])
