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
    
    shape = N // comm_size
    if N % comm_size == 0:
        first_N = shape * comm_rank
    else:
        greater_parts = comm_size - (N % comm_size)
        if comm_rank < greater_parts:
            shape += 1
            first_N = shape * comm_rank
        else:
            first_N = (shape + 1) * greater_parts + shape * (comm_rank - greater_parts)
    partial_sieve = np.full(shape, True, dtype=bool)

    # Dubbel werk
    k = 2
    for k in range(k, root_N+1):
        update_partial_sieve(first_N, k, partial_sieve)

    if comm_rank == 0:
        # Assuming the first rank has at least the first two items in the Sieve
        partial_sieve[:2] = False
    partial_sum = partial_sieve.sum()
    # Alleen sum teruggeven
    total_sum = comm.reduce(partial_sum, op=MPI.SUM, root=0)
    if comm_rank == 0:
        # print(total_sum)
        print(comm_size, N, time.time() - time0, sep=",")



if __name__ == "__main__":
    main()
