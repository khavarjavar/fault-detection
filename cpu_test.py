import time, multiprocessing as mp
def work(_):
    s = 0
    for i in range(6_000_000): s += i * i
    return s
if __name__ == "__main__":
    for n in (1, 4, 8, 16, 32):
        t = time.time()
        with mp.Pool(n) as p: p.map(work, range(n))
        print(n, "procs:", round(time.time() - t, 2), "s")
