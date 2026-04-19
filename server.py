from socket import *
from constCS import *
import time

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
            import math
            a = float(parts[1])
            if a < 0:
                return "Erro: raiz de número negativo"
            return str(math.sqrt(a))

        else:
            return "Comando errado"

    except Exception as e:
        return f"Erro: {str(e)}"


s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print("Servidor de cálculo rodando...")

(conn, addr) = s.accept()
print("Cliente conectado:", addr)

while True:
    data = conn.recv(4096)
    if not data:
        break

    inicio = time.time()

    msg = data.decode()
    print("Recebido:", msg)

    resposta = calcular(msg)

    fim = time.time()
    tempo = fim - inicio

    resposta_final = f"{resposta} | tempo servidor: {tempo:.6f}s"

    conn.send(resposta_final.encode())

conn.close()
