import requests
import threading
import time

URL = "http://127.0.0.1:8000/hotel-reservations"

sucessos = 0
falhas = 0

lock = threading.Lock()


def reservar(cliente):
    global sucessos, falhas

    payload = {
        "customer_id": cliente,
        "room_id": 1,
        "check_in": "2026-06-10",
        "check_out": "2026-06-15",
        "status": "confirmed",
        "total_price": 1000
    }

    try:
        response = requests.post(URL, json=payload)

        with lock:
            if response.status_code == 200:
                sucessos += 1
                print(f"[SUCESSO] Cliente {cliente}")
                print(response.text)
            else:
                falhas += 1
                print(f"[CONFLITO] Cliente {cliente}")
                print(response.text)

    except Exception as e:
        with lock:
            falhas += 1
            print(f"[ERRO] Cliente {cliente}: {e}")


threads = []

inicio = time.time()

for i in range(1, 20):
    t = threading.Thread(target=reservar, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

fim = time.time()

print("\n======================")
print("RESULTADO DO TESTE DE CONFLITO DE HOTEL")
print("======================")
print(f"Reservas feitas: {sucessos}")
print(f"Conflitos bloqueados: {falhas}")
print(f"Tempo total: {fim - inicio:.2f}s")
print("======================")
