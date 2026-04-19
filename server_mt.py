from socket import *
from constCS import *
import time
import threading
import math

def calcular(msg):
    try:
        parts = msg.split()
        op = parts[0].upper()

        if op in ["ADD", "SUB", "MUL", "DIV", "POW"]:
            a = float(parts[1])
            b = float(parts[2])
            if op == "ADD":
                return str(a + b)
            elif op == "SUB":
                return str(a - b)
            elif op == "MUL":
                return str(a * b)
            elif op == "DIV":
                if b == 0:
                    return "Erro: divisão por zero"
                return str(a / b)
            elif op == "POW":
                return str(a ** b)

        elif op == "SQRT":
            a = float(parts[1])
            if a < 0:
                return "Erro: raiz de número negativo"
            return str(math.sqrt(a))

        else:
            return "Comando desconhecido"

    except Exception as e:
        return f"Erro: {str(e)}"


def handle_client(conn, addr):
    """Função executada em cada thread — processa requisições de um cliente."""
    print(f"[Thread] Conexão de {addr}")
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            inicio = time.time()
            msg = data.decode().strip()
            resposta = calcular(msg)
            fim = time.time()
            tempo = fim - inicio

            resposta_final = f"{resposta} | tempo servidor: {tempo:.6f}s"
            conn.send(resposta_final.encode())
    except Exception as e:
        print(f"[Thread] Erro com {addr}: {e}")
    finally:
        conn.close()
        print(f"[Thread] Conexão encerrada: {addr}")


def main():
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)
    print(f"Servidor multithread rodando em {HOST}:{PORT}...")

    try:
        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.daemon = True
            t.start()
            print(f"[Main] Thread iniciada para {addr} | Threads ativas: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
