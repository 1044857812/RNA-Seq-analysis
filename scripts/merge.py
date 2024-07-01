#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python >= 2.7


#####Import Module#####
import logging
import sys
import os
import math
import time
import argparse
import glob
import re


#####Description####
usage = '''
@Date    : 2019-04-14 20:20:21
@Author  : yhfu (yhfu2012@gmail.com)
@Link    : http://fengxuan.tk
@Version : $Id$
Description:

Example:
    python {} [-i input] [-o output]
Step:

'''.format(__file__[__file__.rfind(os.sep) + 1:])


#####HelpFormat#####
class HelpFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass



def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=HelpFormatter, description=usage)
    parser.add_argument('-i', '--input', type = str)
    parser.add_argument(
        '-f', '--fpkm', help='FPKM output file',default="./merged_FPKM.txt", type=str)
    parser.add_argument(
        '-t', '--tpm', help='TPM output file',default="./merged_TPM.txt", type=str)
    parser.add_argument('-v', '--verbose', help='verbosely print information. -vv for printing debug information',
                        action="count", default=0)
    args = parser.parse_args()

    # logging level
    if args.verbose >= 2:
        level = logging.DEBUG
    elif args.verbose == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(level=level, format='%(asctime)s [line:%(lineno)d][%(levelname)s:] %(message)s',
                        datefmt='%Y-%m-%d  %H:%M:%S'
                        )
    return args


def main():
    args = parse_args()
    files = glob.glob(args.input+"/*")
    title=["geneid"]
    all_fpkm={}
    all_tpm={}
    i=0
    with open(args.fpkm,"w") as f2,open(args.tpm,"w") as f3:
        for file in files:
            run = os.path.basename(file)
            ff = glob.glob(file + "/*fpkm_tracking")
            if ff:
                title.append(run)
                with open(ff[0], "r") as f1:
                    lc=0
                    for line in f1:
                        lc=lc+1
                        line=line.strip()
                        if line.startswith("Gene ID"):
                            continue
                        parts=line.split("\t")
                        if not parts[0] in all_fpkm:
                            all_fpkm[parts[0]]=[0 for x in range(0,len(files))]
                        all_fpkm[parts[0]][i] = float(all_fpkm[parts[0]][i]) + float(parts[7])
                        if not parts[0] in all_tpm:
                            all_tpm[parts[0]]=["0" for x in range(0,len(files))]
                        if parts[8]=="-nan":
                            parts[8]="0"
                        all_tpm[parts[0]][i] = float(all_tpm[parts[0]][i]) + float(parts[8])
                i=i+1          
        f2.write("\t".join(title)+ "\n")           
        for g in all_fpkm:
            if len(title) == len(all_fpkm[g])+1:
                f2.write(g+"\t"+"\t".join([str(h) for h in all_fpkm[g]]) + "\n")
        
            else:
                print(len(title))
                print(len(all_fpkm[g]))

        f3.write("\t".join(title)+ "\n")
        for g in all_tpm:
            if len(title)==len(all_tpm[g])+1:                
                f3.write(g+"\t"+"\t".join([str(t) for t in all_tpm[g]])+ "\n")
            else:
                print(len(title))
                print(len(all_fpkm[g]))



if __name__ == '__main__':
    try:
        start_time = time.time()
        print('Start at :' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))

        main()

        end_time = time.time()
        print('Start at :' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))
        print('Spend time :' + str(end_time - start_time))
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) See you!\n")
        sys.exit(0)
