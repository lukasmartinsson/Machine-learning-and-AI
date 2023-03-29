import pybloom_live
import numpy as np

file_path = '/data/2022-DIT065-DAT470/Ensembl-cds-15.txt'
#file_path = './test.txt'
with open(file_path) as f:
    lines = f.read().splitlines() 
    
p = 0.001
f_1 = pybloom_live.BloomFilter(capacity=len(lines), error_rate=p) #indicating a count of 1
f_2 = pybloom_live.BloomFilter(capacity=len(lines), error_rate=p) #indicating a count of 2
f_3 = pybloom_live.BloomFilter(capacity=len(lines), error_rate=p) #indicating a count of 3
f_4 = pybloom_live.BloomFilter(capacity=len(lines), error_rate=p) #indicating a count of 4
#d = {} #dictionary storing all counts
c = 0

size = len(lines)
for i,seq in enumerate(lines):
  
    if (i % int(size/10)) == 0:
      print(i)

    if seq not in f_1:
      f_1.add(seq)
    elif seq not in f_2:
      f_2.add(seq)
    elif seq not in f_3:
      f_3.add(seq)
    elif seq not in f_4:
      f_4.add(seq)
      c += 1

print('Frequency of items appearing 4 or more times', c/size)
