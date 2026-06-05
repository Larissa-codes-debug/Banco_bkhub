import requests
import threading
import time

URL = "http://127.0.0.1:8000/flight-reservations"

flight_id = 1

sucessos = 0
falhas = 0

lock = threading.Lock()


def fazer_reserva(usuario):
    global sucessos, falhas

    payload = {
        "customer_id": usuario,
        "flight_id": flight_id,
        "seat_number": f"{usuario}A",
        "status": "confirmed"
    }

    try:
        response = requests.post(URL, json=payload)

        with lock:
            if response.status_code == 200:
                sucessos += 1
                print(f"[SUCESSO] Usuário {usuario}")
                print(response.text)
            else:
                falhas += 1
                print(f"[FALHA] Usuário {usuario}")
                print(response.text)

    except Exception as e:
        with lock:
            falhas += 1
            print(f"[ERRO] Usuário {usuario}: {e}")


threads = []

inicio = time.time()

for i in range(1, 30):
    t = threading.Thread(target=fazer_reserva, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

fim = time.time()

print("\n========================")
print("RESULTADO DO TESTE DE OVERBOOKING")
print("========================")
print(f"Reservas feitas com sucesso: {sucessos}")
print(f"Conflitos bloqueados: {falhas}")
print(f"Tempo total: {fim - inicio:.2f}s")
print("========================")
