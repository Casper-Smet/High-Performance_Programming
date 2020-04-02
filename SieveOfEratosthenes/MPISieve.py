from mpi4py import MPI
import time
import numpy as np

from sys import argv

def findMultiples(k, lst):
    indices = []
    # ADD MPI HERE INSTEAD
    for i in lst[k:]:
        if i % k == 0:
            indices.append(i)
    return indices

if __name__ == "__main__":
    time0 = time.time()
    N = int(argv[1])

    lst = list(range(2, N))
    root_N = int(N**0.5)


    comm = MPI.COMM_WORLD
    comm_rank = comm.Get_rank()
    comm_size = comm.Get_size()
    
    k_range = np.array_split(np.arange(2, root_N+1), comm_size)
    data = comm.scatter(k_range, root=0)

    # print(len(lst), comm_rank)

    indices = []

    for k in data:
        # print(k)
        indices += findMultiples(k, lst)
    indices = np.array(indices)

    MIndices = comm.gather(indices)
    
    if comm_rank == 0:
        head = MIndices[0]
        np.append(head, MIndices[1:])
        unique_indices = np.unique(head)
        array = np.array(lst)
        primes = np.delete(array, unique_indices)
        print(time.time() - time0)
        print(primes)

