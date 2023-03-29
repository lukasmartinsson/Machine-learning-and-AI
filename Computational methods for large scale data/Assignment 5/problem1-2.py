import findspark
findspark.init()
import argparse
from pyspark import SparkContext
import re

def len_prefix(word1,word2):
    count = 0
    for c1, c2 in zip(word1,word2):
        if c1 == c2:
            count += 1
        else:
            break
    return count

def compute(args):
    sc = SparkContext(master = f'local[{args.workers}]')

    distFile = sc.textFile(args.data)

    words = distFile.flatMap(lambda a: a.split(' ')) \
                    .map(lambda w: re.sub("[^a-z]","",w.lower())) \
                    .map(lambda w: (w,1))
    unique = words.reduceByKey(lambda a,b: a+b)

    '''
    Maybe add bins where the key is first 2 letters and value is all words beginning with those letters:
    ('aa', ['aand','aaron',...]),...
    Then we can call for i, words in enumerate(unique_list) on all different keys and calculate them seperately.
    
    prefix_key = distFile.flatMap(lambda a: a.split(' ')) \
                    .map(lambda w: re.sub("[^a-z]","",w.lower())) \
                    .map(lambda w: (w,1))
    '''

    #if unique word average length should be used:
    #sum = unique.map(lambda w : len(w[0])).reduce(lambda a,b : a+b)
    unique_count = unique.count()
    sum = unique.map(lambda w: len(w[0])*w[1]).reduce(lambda a,b: a+b)
    count = words.count()
    unique_words = unique.sortBy(lambda a: a[0])

    print(f'Average word length: {sum/count}')
    print(f'Total number of unique words: {unique_count}')
    
    unique_list = unique_words.collect()
    prefix_len = 0
    for i, words in enumerate(unique_list):
        if i == len(unique_list) -1:
            break
        curr_w = words[0]
        next_w = unique_list[i+1][0]
        prefix_len += len_prefix(curr_w,next_w)
    avg_prefix = prefix_len / len(unique_list)
    print(f'Average prefix length: {avg_prefix}')
    print(f'Unique words {unique_words.collect()}')


if __name__ == '__main__':
    #/data/2022-DIT065-DAT470/gutenberg/060/06049.txt
    parser = argparse.ArgumentParser(
    )
    parser.add_argument('--data', '-d',
                        default = "/data/2022-DIT065-DAT470/gutenberg/060/06049.txt",
                        help='Data file to be used')
    parser.add_argument('--workers', '-w',
                        default = 16,
                        help='Number of workers')
    args = parser.parse_args()
    compute(args)