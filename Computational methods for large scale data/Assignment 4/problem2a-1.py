import findspark
findspark.init()
import argparse
from pyspark import SparkContext

def spark_summary(args):
    sc = SparkContext(master = f'local[{args.workers}]')

    distFile = sc.textFile(args.data)

    values = distFile.map(lambda l: l.split('\t')).map(lambda t: float(t[2]))
    sum = values.reduce(lambda a,b:a+b)
    c = values.count()
    mean = sum/c
    M = values.reduce(lambda a,b: max(a,b))
    m = values.reduce(lambda a,b: min(a,b))

    diffsq = values.map(lambda a: (a - mean)**2)
    sum_diffs = diffsq.reduce(lambda a,b:a+b)
    dev = (sum_diffs/c)**(1/2)

    n = 10
    bins = create_bins(m,M,n)

    hist_index = values.map(lambda a: (len([a-b for b in bins[:-1] if a-b >= 0])-1,1) )
    bin_counts = hist_index.reduceByKey(lambda a,b: a+b ).sortByKey().collect()
   

    print(f'Sum: {sum}')
    print(f'Counts: {c}')
    print(f'Mean: {mean}')
    print(f'stddev: {dev}')
    print(f'max: {M}')
    print(f'min: {m}')
    print(f'hist: {bin_counts}')
    
def create_bins(m, M, n):
    diff = (M-m)/(n)
    return [diff*i + m for i in range(n+1)]    



if __name__ == '__main__':

    #/data/2022-DIT065-DAT470/data-assignment-3-10M.dat
    parser = argparse.ArgumentParser(
    )
    parser.add_argument('--data', '-d',
                        type = str,
                        help='Data file to be used')
    parser.add_argument('--workers', '-w',
                        type = int,
                        default = 4,
                        help='Number of workers')
    args = parser.parse_args()
    spark_summary(args)