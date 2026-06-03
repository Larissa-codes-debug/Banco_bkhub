from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

# Criação da aplicação FastAPI
# Define título, descrição e versão da API

app = FastAPI(
    title="BookingHub API",
    description="API para gerenciamento de hotéis, voos, reservas e pagamentos",
    version="1.0"
)

# Modelos de cliente, hoteis, quartos aeroportos e voos utilizado nos métodos POST e PUT

class Cliente(BaseModel):
    nome: str
    email: str
    cpf: str
    telefone: str
    
class Hotel(BaseModel):
    nome: str
    cidade: str
    pais: str
    estrelas: int
    endereco: str


class Quarto(BaseModel):
    id_hotel: int
    numero_quarto: str
    tipo: str
    capacidade: int
    preco_por_noite: float


class Aeroporto(BaseModel):
    codigo: str
    nome: str
    cidade: str
    pais: str


class Voo(BaseModel):
    numero_voo: str
    id_aeroporto_origem: int
    id_aeroporto_destino: int
    horario_partida: str
    horario_chegada: str
    total_assentos: int
    assentos_disponiveis: int
    preco: float


class ReservaHotel(BaseModel):
    id_cliente: int
    id_quarto: int
    check_in: str
    check_out: str
    status: str
    preco_total: float


class ReservaVoo(BaseModel):
    id_cliente: int
    id_voo: int
    numero_assento: str
    status: str


class Pagamento(BaseModel):
    tipo_reserva: str
    id_reserva: int
    valor: float
    status: str
    metodo_pagamento: str


#Conexão com PostgreSQL
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


# CLIENTES
# Retorna todos os clientes cadastrados

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

# Busca um cliente específico pelo ID

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


# HOTEIS

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


# QUARTOS

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


# AEROPORTOS

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

# VOOS

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


# RESERVAS HOTEL

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


# RESERVAS VOO

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


# PAGAMENTOS

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

# CRIAR CLIENTE
# Insere um novo cliente no banco

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


# ATUALIZAR CLIENTE
# Atualiza os dados de um cliente existente

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


# EXCLUIR CLIENTE
# Remove um cliente do banco de dados

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

@app.post("/hoteis")
def criar_hotel(hotel: Hotel):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO hoteis
        (nome, cidade, pais, estrelas, endereco)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        hotel.nome,
        hotel.cidade,
        hotel.pais,
        hotel.estrelas,
        hotel.endereco
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Hotel criado com sucesso"}

@app.put("/hoteis/{id_hotel}")
def atualizar_hotel(id_hotel: int, hotel: Hotel):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE hoteis
        SET nome=%s,
            cidade=%s,
            pais=%s,
            estrelas=%s,
            endereco=%s
        WHERE id=%s
    """, (
        hotel.nome,
        hotel.cidade,
        hotel.pais,
        hotel.estrelas,
        hotel.endereco,
        id_hotel
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Hotel atualizado"}

@app.delete("/hoteis/{id_hotel}")
def deletar_hotel(id_hotel: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM hoteis WHERE id=%s",
        (id_hotel,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Hotel removido"}

@app.post("/quartos")
def criar_quarto(quarto: Quarto):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quartos
        (
            id_hotel,
            numero_quarto,
            tipo,
            capacidade,
            preco_por_noite
        )
        VALUES (%s,%s,%s,%s,%s)
    """, (
        quarto.id_hotel,
        quarto.numero_quarto,
        quarto.tipo,
        quarto.capacidade,
        quarto.preco_por_noite
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Quarto criado"}

@app.put("/quartos/{id_quarto}")
def atualizar_quarto(id_quarto: int, quarto: Quarto):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE quartos
        SET
            id_hotel=%s,
            numero_quarto=%s,
            tipo=%s,
            capacidade=%s,
            preco_por_noite=%s
        WHERE id=%s
    """, (
        quarto.id_hotel,
        quarto.numero_quarto,
        quarto.tipo,
        quarto.capacidade,
        quarto.preco_por_noite,
        id_quarto
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Quarto atualizado"}

@app.delete("/quartos/{id_quarto}")
def deletar_quarto(id_quarto: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM quartos WHERE id=%s",
        (id_quarto,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Quarto removido"}

@app.post("/aeroportos")
def criar_aeroporto(aeroporto: Aeroporto):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO aeroportos
        (
            codigo,
            nome,
            cidade,
            pais
        )
        VALUES (%s,%s,%s,%s)
    """, (
        aeroporto.codigo,
        aeroporto.nome,
        aeroporto.cidade,
        aeroporto.pais
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Aeroporto criado"}

@app.put("/aeroportos/{id_aeroporto}")
def atualizar_aeroporto(id_aeroporto: int, aeroporto: Aeroporto):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE aeroportos
        SET codigo=%s,
            nome=%s,
            cidade=%s,
            pais=%s
        WHERE id=%s
    """, (
        aeroporto.codigo,
        aeroporto.nome,
        aeroporto.cidade,
        aeroporto.pais,
        id_aeroporto
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Aeroporto atualizado"}

@app.delete("/aeroportos/{id_aeroporto}")
def deletar_aeroporto(id_aeroporto: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM aeroportos WHERE id=%s",
        (id_aeroporto,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Aeroporto removido"}

@app.post("/voos")
def criar_voo(voo: Voo):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO voos (
            numero_voo,
            id_aeroporto_origem,
            id_aeroporto_destino,
            horario_partida,
            horario_chegada,
            total_assentos,
            assentos_disponiveis,
            preco
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        voo.numero_voo,
        voo.id_aeroporto_origem,
        voo.id_aeroporto_destino,
        voo.horario_partida,
        voo.horario_chegada,
        voo.total_assentos,
        voo.assentos_disponiveis,
        voo.preco
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Voo criado com sucesso"}

@app.put("/voos/{id_voo}")
def atualizar_voo(id_voo: int, voo: Voo):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE voos
        SET
            numero_voo=%s,
            id_aeroporto_origem=%s,
            id_aeroporto_destino=%s,
            horario_partida=%s,
            horario_chegada=%s,
            total_assentos=%s,
            assentos_disponiveis=%s,
            preco=%s
        WHERE id=%s
    """, (
        voo.numero_voo,
        voo.id_aeroporto_origem,
        voo.id_aeroporto_destino,
        voo.horario_partida,
        voo.horario_chegada,
        voo.total_assentos,
        voo.assentos_disponiveis,
        voo.preco,
        id_voo
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Voo atualizado"}

@app.delete("/voos/{id_voo}")
def deletar_voo(id_voo: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM voos WHERE id=%s",
        (id_voo,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Voo removido"}

@app.post("/reservas_hotel")
def criar_reserva_hotel(reserva: ReservaHotel):

    conn = conectar()
    conn.set_session(
    isolation_level="SERIALIZABLE"
    )
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*)
        FROM reservas_hotel
        WHERE id_quarto = %s
        AND status = 'confirmed'
        AND (
            check_in < %s
            AND check_out > %s
        )
        """, (
        reserva.id_quarto,
        reserva.check_out,
        reserva.check_in
    ))

    ocupado = cursor.fetchone()[0]

    if ocupado > 0:
        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=400,
            detail="Quarto já reservado para essa data"
        )

    cursor.execute("""
        INSERT INTO reservas_hotel (
            id_cliente,
            id_quarto,
            check_in,
            check_out,
            status,
            preco_total
        )
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        reserva.id_cliente,
        reserva.id_quarto,
        reserva.check_in,
        reserva.check_out,
        reserva.status,
        reserva.preco_total
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Reserva de hotel criada"}

@app.put("/reservas_hotel/{id_reserva}")
def atualizar_reserva_hotel(
    id_reserva: int,
    reserva: ReservaHotel
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reservas_hotel
        SET
            id_cliente=%s,
            id_quarto=%s,
            check_in=%s,
            check_out=%s,
            status=%s,
            preco_total=%s
        WHERE id=%s
    """, (
        reserva.id_cliente,
        reserva.id_quarto,
        reserva.check_in,
        reserva.check_out,
        reserva.status,
        reserva.preco_total,
        id_reserva
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Reserva atualizada"}

@app.delete("/reservas_hotel/{id_reserva}")
def deletar_reserva_hotel(id_reserva: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM reservas_hotel WHERE id=%s",
        (id_reserva,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Reserva removida"}

@app.post("/reservas_voo")
def criar_reserva_voo(reserva: ReservaVoo):

    conn = conectar()
    conn.set_session(
    isolation_level="SERIALIZABLE"
    )
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT COUNT(*)
    FROM reservas_voo
    WHERE id_voo = %s
      AND numero_assento = %s
""", (
    reserva.id_voo,
    reserva.numero_assento
))
    
    ocupado = cursor.fetchone()[0]

    if ocupado > 0:
        raise HTTPException(
        status_code=400,
        detail="Assento já foi reservado"
    )

    cursor.execute("""
        INSERT INTO reservas_voo (
            id_cliente,
            id_voo,
            numero_assento,
            status
        )
        VALUES (%s,%s,%s,%s)
    """, (
        reserva.id_cliente,
        reserva.id_voo,
        reserva.numero_assento,
        reserva.status
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Reserva de voo criada"}

@app.put("/reservas_voo/{id_reserva}")
def atualizar_reserva_voo(
    id_reserva: int,
    reserva: ReservaVoo
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reservas_voo
        SET
            id_cliente=%s,
            id_voo=%s,
            numero_assento=%s,
            status=%s
        WHERE id=%s
    """, (
        reserva.id_cliente,
        reserva.id_voo,
        reserva.numero_assento,
        reserva.status,
        id_reserva
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Reserva de voo atualizada"}

@app.delete("/reservas_voo/{id_reserva}")
def deletar_reserva_voo(id_reserva: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM reservas_voo WHERE id=%s",
        (id_reserva,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Reserva removida"}

@app.post("/pagamentos")
def criar_pagamento(pagamento: Pagamento):
    

    conn = conectar()
    conn.set_session
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pagamentos (
            tipo_reserva,
            id_reserva,
            valor,
            status,
            metodo_pagamento
        )
        VALUES (%s,%s,%s,%s,%s)
    """, (
        pagamento.tipo_reserva,
        pagamento.id_reserva,
        pagamento.valor,
        pagamento.status,
        pagamento.metodo_pagamento
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Pagamento criado"}

@app.put("/pagamentos/{id_pagamento}")
def atualizar_pagamento(
    id_pagamento: int,
    pagamento: Pagamento
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pagamentos
        SET
            tipo_reserva=%s,
            id_reserva=%s,
            valor=%s,
            status=%s,
            metodo_pagamento=%s
        WHERE id=%s
    """, (
        pagamento.tipo_reserva,
        pagamento.id_reserva,
        pagamento.valor,
        pagamento.status,
        pagamento.metodo_pagamento,
        id_pagamento
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Pagamento atualizado"}

@app.delete("/pagamentos/{id_pagamento}")
def deletar_pagamento(id_pagamento: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM pagamentos WHERE id=%s",
        (id_pagamento,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Pagamento removido"}