#!/usr/bin/env python3
import twlang
import os
import sys

def copy_fix(infile, delete_unused, append_missing, delete_empty):
    content = open(infile).readlines()
    trans = twlang.translations(infile)
    if delete_unused or append_missing:
        local = twlang.localizes()
    if append_missing:
        supported = []
    for tran, (start, expr, end) in trans.items():
        if delete_unused and tran not in local:
            content[start:end] = [None]*(end-start)
        if append_missing and tran in local:
            if expr or (not expr and delete_empty):
                supported.append(local.index(tran))
            else:
                content[start:end] = [None]*(end-start)
        if delete_empty and not expr:
            content[start:end] = [None]*(end-start)
    content = [line for line in content if line != None]
    if append_missing:
        missing = [index for index in range(len(local)) if index not in supported]
        if missing:
            if content[-1] != "\n":
                content.append("\n")
            for i, miss in enumerate(missing):
                if local[miss][1] != "":
                    content.append("["+local[miss][1]+"]\n")
                content.append(local[miss][0]+"\n== \n\n")
            content[-1] = content[-1][:-1]
    return "".join(content)

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__) + "/../..")

    if len(sys.argv) < 3:
        print("usage: python copy_fix.py <infile> <outfile> [--delete-unused] [--append-missing] [--delete-empty]")
        sys.exit()
    infile = sys.argv[1]
    outfile = sys.argv[2]
    args = sys.argv[3:]
    delete_unused = False
    append_missing = False
    delete_empty = False
    for arg in args:
        if arg == "--delete-unused":
            delete_unused = True
        elif arg == "--append-missing":
            append_missing = True
        elif arg == "--delete-empty":
            delete_empty = True
        else:
            print("No such argument '"+arg+"'.")
            sys.exit()

    content = copy_fix(infile, delete_unused, append_missing, delete_empty)

    open(outfile, "w").write("".join(content))
    print("Successfully created '" + outfile + "'.")
