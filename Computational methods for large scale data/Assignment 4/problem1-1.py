from mrjob.job import MRJob, MRStep
import numpy as np
from sklearn.datasets import make_blobs
import logging

class MRKmeans(MRJob):

    #[[0.0,0.0], [2.1, 2.4], [1.4, 1.7]]
    def mapper_init(self):
        logging.info("...Initializing centroids...")
        with open('/home/2022/jansfelt/2022-DAT470-DIT065-CTLSD/data/A4/centroids.dat') as f:
            centroids = [x.split(',') for x in f.read().splitlines()]
            centroids = [[float(x) for x in c] for c in centroids] # Convert to numerics
        self.centroids = centroids


    def mapper(self, _, value):
        data = [float(x) for x in value.split(',')]
        yield _, (data, self.centroids)

    def combiner(self, _, values):
        c = {}
        for data, centroids in values:
            x = data[0]
            y = data[1]
            minDist = 100_000_000
            for i, cent in enumerate(centroids):
                dist =(x-cent[0])**2 + (y-cent[1])**2
                if dist < minDist:
                    minDist = dist
                    c_index = i

            c[(x,y)] = c_index
            logging.info(f"Assigning centroid {c_index} to data point {(x,y)}")
        yield _, c

    def reducer(self, key, values):
        c_tot = {}
        for c in values:
            for key in c:
                c_tot[key] = c.get(key)
        yield "out", c_tot

    def combiner_recompute(self, _, values):
        c_tot = next(values)
        centroids = [(0.0,0.0)]*3
        cluster_sizes = [0]*3
        #centroids = np.zeros((3,2))
        for key in c_tot:
            logging.info(f"Centroids {centroids}")
            datapoint = eval(key)
            cent_index = c_tot.get(key)
            cent = centroids[cent_index]
            logging.info(f"Datapoint {datapoint} centroid {cent}")
            x = cent[0]
            y = cent[1]
            x += datapoint[0]
            y += datapoint[1]
            centroids[cent_index] = (x,y)
            cluster_sizes[cent_index] += 1
            
            #centroids[c_tot.get(key)] += eval(key)
            #logging.info(f"Datapoint {eval(key)} with value {c_tot.get(key)}")
        logging.info(f"Sending centroids {centroids}")
        yield _, (centroids, cluster_sizes)
    
    def reducer_update_centroids(self, _, values):
        centroids = np.zeros((3,2))
        total_cluster_sizes = np.zeros(3)
        for cent, sizes in values:
            for i in range(3):
                centroids[i] += cent[i]
                total_cluster_sizes[i] += sizes[i]
            
        logging.info(f"Centroid {centroids} with sizes {total_cluster_sizes.reshape(-1,1)}")
        centroids = centroids / total_cluster_sizes.reshape(-1,1)

        logging.info(f"New Centroids {centroids}")
        self.write_centroids(centroids)
        
    def write_centroids(self, centroids):
         with open('/home/2022/jansfelt/2022-DAT470-DIT065-CTLSD/data/A4/centroids.dat', "w") as f:
             for c in centroids:
                f.write(str(c[0])+","+str(c[1])+"\n")

    def steps(self):
        return [MRStep(mapper_init=self.mapper_init,
                mapper=self.mapper,
                combiner=self.combiner,
                reducer=self.reducer),
                MRStep(combiner = self.combiner_recompute,
                reducer = self.reducer_update_centroids)]

if __name__ == '__main__':
    logging.basicConfig(filename='logs.log',format='# %(message)s',level=logging.INFO, filemode='w')
    MRKmeans.run()
