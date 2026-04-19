from socket import *
from constCS import *
import time
import random

NUM_REQUESTS = 200

OPERATIONS = [
    lambda: f"ADD {random.randint(1,1000)} {random.randint(1,1000)}",
    lambda: f"SUB {random.randint(1,1000)} {random.randint(1,1000)}",
    lambda: f"MUL {random.randint(1,100)}  {random.randint(1,100)}",
    lambda: f"DIV {random.randint(1,1000)} {random.randint(1,999)}",
    lambda: f"POW {random.randint(1,10)}   {random.randint(1,5)}",
    lambda: f"SQRT {random.randint(1,10000)}",
]


def run_single_client():
    print(f"\nCliente SINGLE-THREAD | {NUM_REQUESTS} requisições sequenciais")
    results = []

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))

    t_start = time.time()

    for i in range(NUM_REQUESTS):
        msg = random.choice(OPERATIONS)()
        t0 = time.time()
        s.send(msg.encode())
        resp = s.recv(4096).decode()
        t1 = time.time()
        results.append(t1 - t0)
        if i % 50 == 0:
            print(f"  req {i:4d}: {msg.strip():20s} -> {resp[:40]}")

    s.close()
    t_end = time.time()
    total = t_end - t_start

    print(f"\nResultados ({len(results)} respostas recebidas):")
    print(f"  Tempo total:          {total:.4f}s")
    print(f"  Média por requisição: {sum(results)/len(results)*1000:.2f}ms")
    print(f"  Mínimo:               {min(results)*1000:.2f}ms")
    print(f"  Máximo:               {max(results)*1000:.2f}ms")
    print(f"  Throughput:           {len(results)/total:.1f} req/s")

    return total


if __name__ == "__main__":
    run_single_client()
