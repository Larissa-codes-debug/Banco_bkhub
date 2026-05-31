from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI(
    title="BookingHub API",
    description="API para gerenciamento de hotéis, voos, reservas e pagamentos",
    version="1.0"
)

class Cliente(BaseModel):
    nome: str
    email: str
    cpf: str
    telefone: str

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="banco_bkhub",
        user="postgres",
        password="miss23"
    )


@app.get("/")
def home():
    return {"mensagem": "BookingHub API funcionando"}


# ==========================
# CLIENTES
# ==========================

@app.get("/clientes")
def listar_clientes():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email, cpf, telefone
        FROM clientes
        ORDER BY id
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@app.get("/clientes/{id_cliente}")
def buscar_cliente(id_cliente: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email, cpf, telefone
        FROM clientes
        WHERE id = %s
    """, (id_cliente,))

    dado = cursor.fetchone()

    cursor.close()
    conn.close()

    return dado


# ==========================
# HOTEIS
# ==========================

@app.get("/hoteis")
def listar_hoteis():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM hoteis
        ORDER BY id
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@app.get("/hoteis/{id_hotel}")
def buscar_hotel(id_hotel: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM hoteis
        WHERE id = %s
    """, (id_hotel,))

    dado = cursor.fetchone()

    cursor.close()
    conn.close()

    return dado


# ==========================
# QUARTOS
# ==========================

@app.get("/quartos")
def listar_quartos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM quartos
        ORDER BY id
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@app.get("/quartos/{id_quarto}")
def buscar_quarto(id_quarto: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM quartos
        WHERE id = %s
    """, (id_quarto,))

    dado = cursor.fetchone()

    cursor.close()
    conn.close()

    return dado


# ==========================
# AEROPORTOS
# ==========================

@app.get("/aeroportos")
def listar_aeroportos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM aeroportos
        ORDER BY id
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@app.get("/aeroportos/{id_aeroporto}")
def buscar_aeroporto(id_aeroporto: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM aeroportos
        WHERE id = %s
    """, (id_aeroporto,))

    dado = cursor.fetchone()

    cursor.close()
    conn.close()

    return dado


# ==========================
# VOOS
# ==========================

@app.get("/voos")
def listar_voos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM voos
        ORDER BY id
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@app.get("/voos/{id_voo}")
def buscar_voo(id_voo: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM voos
        WHERE id = %s
    """, (id_voo,))

    dado = cursor.fetchone()

    cursor.close()
    conn.close()

    return dado


# ==========================
# RESERVAS HOTEL
# ==========================

@app.get("/reservas_hotel")
def listar_reservas_hotel():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM reservas_hotel
        ORDER BY id
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@app.get("/reservas_hotel/{id_reserva}")
def buscar_reserva_hotel(id_reserva: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM reservas_hotel
        WHERE id = %s
    """, (id_reserva,))

    dado = cursor.fetchone()

    cursor.close()
    conn.close()

    return dado


# ==========================
# RESERVAS VOO
# ==========================

@app.get("/reservas_voo")
def listar_reservas_voo():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM reservas_voo
        ORDER BY id
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@app.get("/reservas_voo/{id_reserva}")
def buscar_reserva_voo(id_reserva: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM reservas_voo
        WHERE id = %s
    """, (id_reserva,))

    dado = cursor.fetchone()

    cursor.close()
    conn.close()

    return dado


# ==========================
# PAGAMENTOS
# ==========================

@app.get("/pagamentos")
def listar_pagamentos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM pagamentos
        ORDER BY id
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@app.get("/pagamentos/{id_pagamento}")
def buscar_pagamento(id_pagamento: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM pagamentos
        WHERE id = %s
    """, (id_pagamento,))

    dado = cursor.fetchone()

    cursor.close()
    conn.close()

    return dado

# ==========================
# CRIAR CLIENTE
# ==========================

@app.post("/clientes")
def criar_cliente(cliente: Cliente):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clientes
        (nome, email, cpf, telefone)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (
        cliente.nome,
        cliente.email,
        cliente.cpf,
        cliente.telefone
    ))

    novo_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "mensagem": "Cliente criado com sucesso",
        "id": novo_id
    }


# ==========================
# ATUALIZAR CLIENTE
# ==========================

@app.put("/clientes/{id_cliente}")
def atualizar_cliente(
    id_cliente: int,
    cliente: Cliente
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clientes
        SET
            nome = %s,
            email = %s,
            cpf = %s,
            telefone = %s
        WHERE id = %s
    """, (
        cliente.nome,
        cliente.email,
        cliente.cpf,
        cliente.telefone,
        id_cliente
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "mensagem": "Cliente atualizado com sucesso"
    }


# ==========================
# EXCLUIR CLIENTE
# ==========================

@app.delete("/clientes/{id_cliente}")
def deletar_cliente(id_cliente: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM clientes
        WHERE id = %s
    """, (id_cliente,))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "mensagem": "Cliente excluído com sucesso"
    }