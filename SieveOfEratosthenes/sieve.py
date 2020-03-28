import time
from sys import argv

import numpy as np


def sieve(N, return_primes=False):
    k = 2
    sieve = np.full(N, True, dtype=bool)
    root_N = int(N**0.5)
    for (i,), (is_prime) in np.ndenumerate(sieve[k:root_N+1]):
        k = i + 2
        if is_prime:
            sieve[k*2::k] = False

    sieve[0:2] = False

    if return_primes:
        return np.arange(N)[sieve]
    else:
        return sieve.sum()
    



def main():
    assert len(argv) > 1, "ERROR: Give me N"
    
    time0 = time.time()
    sieve(int(argv[1]))
    print(time.time() - time0)
    

if __name__ == "__main__":
    main()
