import time
from sys import argv

import numpy as np
from mpi4py import MPI


def first_common_index(start_N, k):
    if not start_N % k:
        index = 0
    else:
        index = (start_N // k + 1) * k - start_N
    return index


def update_partial_sieve(start_N, k, sieve):
    if k >= start_N:
        k = k - start_N
        if sieve[k]:
            sieve[k*2::k] = False
    else:
        start = first_common_index(start_N, k)
        sieve[start::k] = False
    

def main():
    N = int(argv[1])
    root_N = int(N**0.5)

    comm = MPI.COMM_WORLD
    comm_rank = comm.Get_rank()
    comm_size = comm.Get_size()
    if comm_rank == 0:
        time0 = time.time()
        # Find shapes for each rank's partial_sieve
        shapes = [array.shape[0]
                  for array in np.array_split(np.empty(N, dtype=bool), comm_size)]
        # Find starting N for each rank
        sizes = []
        for i in range(len(shapes)):
            sizes.append((shapes[i], sum(shapes[:i])))
    else:
        sizes = None

    (shape, first_N) = comm.scatter(sizes, root=0)
    partial_sieve = np.full(shape, True, dtype=bool)

    k = 2
    for k in range(k, root_N+1):
        update_partial_sieve(first_N, k, partial_sieve)

    split_sieve = comm.gather(partial_sieve, root=0)
    if comm_rank == 0:
        sieve = np.concatenate(split_sieve)
        sieve[:2] = False
        print(comm_size, N, time.time() - time0, sep=",")
        # print(sieve.sum())


if __name__ == "__main__":
    main()
