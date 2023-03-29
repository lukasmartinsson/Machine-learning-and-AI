import numpy as np
import argparse
import time

def compute(args):
    
    #Reading the data, splitting every new line
    with open(args.data) as f:
        lines = f.read().split("\n")

    freq_count = {}
    start_index = {}
    stop_index = {}
    prev_freq = 0
    tot_freq = 0

    size = len(lines)
    keys = [None]*size
    seq_count = [0]*size

    #looping through all sequences and taking out start/stop index for each frequency 
    #as well as number of sequences with the given frequency
    for i, line in enumerate(lines):
        if line == '':
            continue
        key ,freq  = line.split(" ")
        freq = int(freq)
        tot_freq += freq

        keys[i] = key

        freq_count[freq] = freq_count.get(freq,0) + freq
        seq_count[i] = freq

        if prev_freq is not freq:
            start_index[freq] = i
            stop_index[prev_freq] = i-1
        prev_freq = freq
    stop_index[freq] = size #inserting stop_index for last frequency
        
    #Computing the probability vector for frequencies
    max_freq = int(lines[0].split(" ")[1])
    p_freq = [freq_count.get(i,0) / tot_freq for i in range(max_freq+1)]

    ##probablity vector for each sequence (used in original sampling)
    p_seq = [seq_count[i] / tot_freq for i in range(size)]

    #Sample how many times to draw from each frequency-bin
    start_time = time.time()
    freq_choices = np.bincount(sample(range(max_freq+1), args.n, p_freq))
    freq_c_time = time.time() - start_time

    #draw that many times from the bin
    seqs_samples = []
    sample_time = 0
    for i, f in enumerate(freq_choices):
        if f > 0: 
            keys_f = keys[start_index[i]:stop_index[i]+1]
            start_time = time.time()
            seqs_samples += list(sample(keys_f, f)) #draw f sequences uniformly
            temp_time = time.time() - start_time
            sample_time += temp_time

    tot_time_updated = freq_c_time+sample_time
    samples_per_second_updated = args.n / tot_time_updated
    
    #Timing the original sampling
    start_time = time.time()
    sample(keys, args.n, p_seq)
    stop_time = time.time()

    tot_time2 = stop_time-start_time
    samples_per_second2 = args.n / tot_time2

    #print(seqs_samples)
    print(f"Original time: {tot_time2}")
    print(f"Original samples per second {samples_per_second2}")
    print(f"Updated time: {tot_time_updated}")
    print(f"Updated samples per second {samples_per_second_updated}")


def sample(keys, n, p=None):
    rng = np.random.default_rng()
    if p == None:
        return rng.choice(keys, n, replace=True)
    else:
        return rng.choice(keys, n, replace=True, p=p)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    )
    parser.add_argument('--data', '-d',
                        default = "/data/2022-DIT065-DAT470/Ensembl-cds-15-counts.txt",
                        help='Data file to be used')
    parser.add_argument('--workers', '-w',
                        default = 16,
                        help='Number of workers')
    parser.add_argument('--n',
                        default = 1,
                        type = int,
                        help='Number of samples')
    args = parser.parse_args()
    compute(args)
