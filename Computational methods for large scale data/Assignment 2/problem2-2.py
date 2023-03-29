import multiprocessing # See https://docs.python.org/3/library/multiprocessing.html
import argparse # See https://docs.python.org/3/library/argparse.html
import random
from math import pi

def do_task(q_res, n):
    while True:
        s = sample_pi(n)
        q_res.put(s)
        
        
def sample_pi(n):
    """ Perform n steps of Monte Carlo simulation for estimating Pi/4.
        Returns the number of successes."""
    random.seed()
    s = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1
    return s
   

def compute_pi(args):
    random.seed(1)
  
    q_res = multiprocessing.Queue()
    
    n = 100
    
    processes = [multiprocessing.Process(target=do_task, args=(q_res, n)) for rank in range(args.workers)]

    for p in processes:
        p.start()
        
    acc = 100
    s_total = 0
    n_total = 0
    
    while acc >= args.accuracy:
        res = q_res.get()
        s_total += res
        n_total += 100
        pi_est = 4*s_total/n_total
        acc = abs(pi-pi_est)
    
    for p in processes:
        p.terminate()

    q_res.close()
    print(" Steps\tSuccess\tPi est.\tError")
    print("%6d\t%7d\t%1.5f\t%1.5f" % (n_total, s_total, pi_est, pi-pi_est))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute Pi using Monte Carlo simulation.')
    parser.add_argument('--workers', '-w',
                        default='4',
                        type = int,
                        help='Number of parallel processes')
    parser.add_argument('--accuracy', '-a',
                        default='0.00001',
                        type = float,
                        help='Accuracy to get until stopping process')
    args = parser.parse_args()
    compute_pi(args)
    
