#!/usr/bin/env python3

import pandas as pd
import os,sys
import argparse

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-f','--files', default=['-'],nargs='*',action='store',required=True)
    parser.add_argument('-j','--idx_to_keep',default=2,action='store',type=int)
    parser.add_argument('-wd','--working_directory',default='.',action='store')
    parser.add_argument('-n','--file_name_as_header',action='store_true')
    parser.add_argument('-nh','--no_header',action='store_true')
    
    args=parser.parse_args()
    args.idx_to_keep -= 1
    if args.files==['-']:
        all_files=[f.rstrip() for f in sys.stdin.readlines()]
    else:
        all_files=args.files

    if args.working_directory != '.':
        args.working_directory=args.working_directory.rstrip('/')
        all_files=[f'{args.working_directory}/{f}' for f in all_files]
            
    HEADER=0
    if args.no_header:
        HEADER=None

    df_from_each_file=[pd.read_csv(f, index_col=0, sep='\t', header=HEADER, usecols=[0,args.idx_to_keep]) for f in all_files]
    df = pd.concat(df_from_each_file,axis=1, sort=False)

    if args.file_name_as_header:
        df.columns=[f.split('/')[-1].split('.')[0] for f in all_files]

    df.index.name='index'
    df.to_csv(sys.stdout, sep='\t',index=True)
