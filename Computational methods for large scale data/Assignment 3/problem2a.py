from mrjob.job import MRJob, MRStep
import time
import numpy as np
import operator


class MRSummary(MRJob):
 
    def mapper(self, _, line):                
        id, group, value = line.split('\t')
        yield ("id", float(value))

    def combiner_stats(self,key,values):
        n = 10
        m = 3.1
        M = 7.2
        bins = self.create_bins(m,M,n) #creating bins
        f = [0]*(n-1)
    
        min_val = float(next(values))
        max_val = min_val
        s = 0
        s2 = 0
        for i, val in enumerate(values):
            val = float(val)

            #Calculating bin frequencies
            diffs = [b - val for b in bins if b-val>0]
            b_index = n - len(diffs) - 1
            f[b_index] += 1

            s += val
            s2 += val**2
            min_val = min(val, min_val)
            max_val = max(val, max_val)
        yield ("Stats", (i, min_val, max_val, s, s2, f))

    def reducer_stats(self, key, values):
        if key == "Stats":
            m = 100_000_000
            M = -m
            s_tot = 0
            s2_tot = 0
            count = 0

            n = 10
            f_tot = np.zeros(n-1)
            for i, min_val, max_val, s, s2, f in values:
                count += int(i)
                m = min(float(min_val), m)
                M = max(float(max_val), M)
                s_tot += float(s)
                s2_tot += float(s2)
                f_tot += np.array(f)

            avg = s_tot / count
            std = ((s2_tot) / count + avg**2)**(1/2)
            yield ("Stats", (m, M, avg, std, list(f_tot)))
            

    def steps(self):
        return [MRStep(mapper=self.mapper,
                combiner=self.combiner_stats,
                reducer=self.reducer_stats)
                ]

    def create_bins(self, m, M, n):
        diff = (M-m)/(n-1)
        return [diff*i + m for i in range(n)]

if __name__ == '__main__':
    MRSummary.run()
