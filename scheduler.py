""" This script coordinates the racket threads that are
    performing the depth-first search on a graph in parallel.
    After each racket thread has completed its assigned search,
    this script collects the list of visited vertices and
    propagates this information to future threads.
"""
from itertools import combinations
from math import floor, log2
import queue
from queue import Queue
from scipy.special import binom
import subprocess
from threading import Thread
from utils import hashdict, process_magma_output


# Explore the power set of {1..n}
n = 12
# How many tasks to run concurrently.
n_workers = 2
# The starting depth should be a number between 1 and n.
starting_depth = n - 2
# The graph search is going to be distributed among n_tasks tasks,
# not necessarily all parallel.
n_tasks = binom(n, starting_depth)

# We will start processing from the subsets of length s0_len
s0_len = n - starting_depth


def dfs_worker(q, marked):
    """ Launches a magma process and parses its results. """
    while True:
        try:
            # Read the starting vertex from the queue.
            s0 = q.get()
        except queue.Empty:
            return
        else:
            s0str = "{" + ",".join(str(i) for i in s0) + "}"
            cmd = ["magma", "-b", "s0:=" + s0str, f"n:={n}", "dfs.m"]
            res = subprocess.run(cmd, capture_output=True)
            seen = process_magma_output(res.stdout)
            # Update the list of vertices seen so far.
            # Important: the next three lines should not be replaced by:
            #    marked |= seen, as this would not be atomic.
            newsets = seen - marked
            for k in newsets:
                marked.add(k) # All is fine: add is atomic.
            q.task_done()


if __name__ == "__main__":
    # Keep track of the vertices visited so far.
    marked = set()
    q = Queue(maxsize=n_workers)
    args = (q, marked)
    threads = [Thread(target=dfs_worker, args=args, daemon=True) for _ in range(n_workers)]
    [t.start() for t in threads]
    # We parse the database from the polytopes with more
    # points to the polytopes with fewer points.
    for s0 in combinations(set(range(1, n + 1)), s0_len):
        q.put(s0)

    q.join()

    print(len(marked))
    print("All done.")

