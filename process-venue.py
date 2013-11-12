#!/usr/bin/python

import sys, os, shutil, time, argparse
import json

pathToData = '../DataSet'
srcPath = os.path.join(pathToData, 'venues.txt')
outPrefix = 'venues-'
outSuffix = '-new.json'

fullList = ['id', 'venuename', 'lat', 'lng', 'address', 'city', 'metroarea', 'uniquevisitors', 'totalcheckins', 'category',  'parentcategory']
wantedList = ['id', 'venuename', 'lat', 'lng', 'city', 'uniquevisitors', 'totalcheckins', 'category',  'parentcategory']

def parse_args():
  parser = argparse.ArgumentParser()
  # whether we want to split output files by cities
  parser.add_argument('--c', action='store_true')
  # whether we want to format for visualization
  parser.add_argument('--v', action='store_true')
  return parser.parse_args()

def split_file(args):
  fin = open(srcPath, 'r')
  head = fin.readline()
  attrs = head.strip().split('\t')

  if args.c:
    cities = set()
    fout_list = dict()
    for line in fin:
      v_dict = dict()
      venue = line.strip().split('\t')
      for i in range(0, len(attrs)):
        if attrs[i] in wantedList:
          v_dict[attrs[i]] = venue[i]
        elif attrs[i] == 'metroarea':
          region = venue[i].split(', ')[-1]
          if region in cities: fout = fout_list[region]
          else:
            tgtPath = os.path.join(pathToData, outPrefix + region + outSuffix)
            fout = open(tgtPath, 'w')
            if (args.v): fout.write('[')
            cities.add(region)
            fout_list[region] = fout
      fout.write(json.dumps(v_dict))
      if (args.v): fout.write(',')
      else: fout.write('\n')
    # cleaning up
    for region in fout_list:
      if (args.v): fout_list[region].write(']')
      fout_list[region].close()

  else:
    tgtPath = os.path.join(pathToData, 'venues-all.json')
    fout = open(tgtPath, 'w')
    if (args.v): fout.write('[')
    for line in fin:
      v_dict = dict()
      venue = line.split('\t')
      for i in range(0, len(attrs)):
        if attrs[i] in wantedList:
          v_dict[attrs[i]] = venue[i]
      fout.write(json.dumps(v_dict))
      if (args.v): fout.write(',')
      else: fout.write('\n')
    if (args.v): fout.write(']')
    fout.close()

  fin.close()

if __name__ == '__main__':
  args = parse_args()
  split_file(args)
