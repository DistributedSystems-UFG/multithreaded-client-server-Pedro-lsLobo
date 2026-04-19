from socket import *
from constCS import *
import time
import threading
import random

NUM_REQUESTS = 200
NUM_THREADS  = 20
RESULTS = []
LOCK = threading.Lock()

OPERATIONS = [
    lambda: f"ADD {random.randint(1,1000)} {random.randint(1,1000)}",
    lambda: f"SUB {random.randint(1,1000)} {random.randint(1,1000)}",
    lambda: f"MUL {random.randint(1,100)}  {random.randint(1,100)}",
    lambda: f"DIV {random.randint(1,1000)} {random.randint(1,999)}",
    lambda: f"POW {random.randint(1,10)}   {random.randint(1,5)}",
    lambda: f"SQRT {random.randint(1,10000)}",
]


def send_request(req_id):
    """Cada chamada abre sua própria conexão e envia uma requisição."""
    msg = random.choice(OPERATIONS)()
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((HOST, PORT))
        t0 = time.time()
        s.send(msg.encode())
        resp = s.recv(4096).decode()
        t1 = time.time()
        s.close()
        elapsed = t1 - t0
        with LOCK:
            RESULTS.append(elapsed)
        if req_id % 50 == 0:
            print(f"  req {req_id:4d}: {msg.strip():20s} -> {resp[:40]}")
    except Exception as e:
        print(f"  req {req_id}: ERRO - {e}")


def run_multithread_client():
    print(f"\n=== Cliente MULTITHREAD | {NUM_REQUESTS} requisições | {NUM_THREADS} threads paralelas ===")
    threads = []
    t_start = time.time()

    sem = threading.Semaphore(NUM_THREADS)

    def worker(req_id):
        with sem:
            send_request(req_id)

    for i in range(NUM_REQUESTS):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    t_end = time.time()
    total = t_end - t_start

    if RESULTS:
        print(f"\nResultados ({len(RESULTS)} respostas recebidas):")
        print(f"  Tempo total (wall clock): {total:.4f}s")
        print(f"  Média por requisição:     {sum(RESULTS)/len(RESULTS)*1000:.2f}ms")
        print(f"  Mínimo:                   {min(RESULTS)*1000:.2f}ms")
        print(f"  Máximo:                   {max(RESULTS)*1000:.2f}ms")
        print(f"  Throughput:               {len(RESULTS)/total:.1f} req/s")

    return total


if __name__ == "__main__":
    run_multithread_client()
