import psycopg2
from faker import Faker
import random
from datetime import timedelta

fake = Faker('pt_BR')

conn = psycopg2.connect(
    host="localhost",
    database="banco_bkhub",
    user="postgres",
    password="1810"
)

cursor = conn.cursor()

print("Conectado com sucesso!")


# HOTÉIS
for _ in range(20):

    nome = fake.company() + " Hotel"
    cidade = fake.city()
    pais = "Brasil"
    estrelas = random.randint(1, 5)
    endereco = fake.address()

    cursor.execute("""
        INSERT INTO hoteis (
            nome,
            cidade,
            pais,
            estrelas,
            endereco
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        nome,
        cidade,
        pais,
        estrelas,
        endereco
    ))

conn.commit()

print("Hotéis inseridos!")


# QUARTOS
cursor.execute("SELECT id FROM hoteis")
hoteis = cursor.fetchall()

tipos_quarto = ['single', 'double', 'suite']

for hotel in hoteis:

    id_hotel = hotel[0]

    for numero_quarto in range(1, 11):

        cursor.execute("""
            INSERT INTO quartos (
                id_hotel,
                numero_quarto,
                tipo,
                capacidade,
                preco_por_noite
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            id_hotel,
            str(numero_quarto),
            random.choice(tipos_quarto),
            random.randint(1, 4),
            random.randint(150, 900)
        ))

conn.commit()

print("Quartos inseridos!")


# CLIENTES
for _ in range(100):

    cursor.execute("""
        INSERT INTO clientes (
            nome,
            email,
            cpf,
            telefone
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (
        fake.name(),
        fake.unique.email(),
        fake.unique.cpf(),
        fake.phone_number()
    ))

conn.commit()

print("Clientes inseridos!")


# AEROPORTOS
aeroportos = [
    ('FOR', 'Aeroporto de Fortaleza', 'Fortaleza'),
    ('REC', 'Aeroporto do Recife', 'Recife'),
    ('GRU', 'Aeroporto de Guarulhos', 'São Paulo'),
    ('GIG', 'Aeroporto Galeão', 'Rio de Janeiro'),
    ('BSB', 'Aeroporto de Brasília', 'Brasília')
]

for aeroporto in aeroportos:

    cursor.execute("""
        INSERT INTO aeroportos (
            codigo,
            nome,
            cidade,
            pais
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (codigo) DO NOTHING
    """, (
        aeroporto[0],
        aeroporto[1],
        aeroporto[2],
        'Brasil'
    ))

conn.commit()

print("Aeroportos inseridos!")


# VOOS
cursor.execute("SELECT id FROM aeroportos")
ids_aeroportos = [a[0] for a in cursor.fetchall()]

for i in range(50):

    origem = random.choice(ids_aeroportos)
    destino = random.choice(ids_aeroportos)

    while destino == origem:
        destino = random.choice(ids_aeroportos)

    horario_partida = fake.date_time_this_year()
    horario_chegada = horario_partida + timedelta(
        hours=random.randint(1, 5)
    )

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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (numero_voo) DO NOTHING
    """, (
        f"BH{random.randint(1000,999999)}",
        origem,
        destino,
        horario_partida,
        horario_chegada,
        150,
        150,
        random.randint(300, 1500)
    ))

conn.commit()

print("Voos inseridos!")


# RESERVAS DE HOTEL
cursor.execute("SELECT id FROM clientes")
ids_clientes = [c[0] for c in cursor.fetchall()]

cursor.execute("""
    SELECT id, preco_por_noite
    FROM quartos
""")

quartos = cursor.fetchall()

for _ in range(200):

    id_cliente = random.choice(ids_clientes)

    quarto = random.choice(quartos)

    id_quarto = quarto[0]
    preco_quarto = quarto[1]

    check_in = fake.date_this_year()

    noites = random.randint(1, 10)

    check_out = check_in + timedelta(days=noites)

    preco_total = preco_quarto * noites

    cursor.execute("""
        INSERT INTO reservas_hotel (
            id_cliente,
            id_quarto,
            check_in,
            check_out,
            preco_total,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        id_cliente,
        id_quarto,
        check_in,
        check_out,
        preco_total,
        random.choice([
            'pending',
            'confirmed',
            'cancelled'
        ])
    ))

conn.commit()

print("Reservas de hotel inseridas!")


# RESERVAS DE VOO
cursor.execute("SELECT id FROM voos")
ids_voos = [v[0] for v in cursor.fetchall()]

for _ in range(300):

    id_cliente = random.choice(ids_clientes)

    id_voo = random.choice(ids_voos)

    numero_assento = (
        f"{random.randint(1,30)}"
        f"{random.choice(['A','B','C','D'])}"
    )

    cursor.execute("""
        INSERT INTO reservas_voo (
            id_cliente,
            id_voo,
            numero_assento,
            status
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (
        id_cliente,
        id_voo,
        numero_assento,
        random.choice([
            'pending',
            'confirmed',
            'cancelled'
        ])
    ))

conn.commit()

print("Reservas de voo inseridas!")


# PAGAMENTOS
cursor.execute("""
    SELECT id, preco_total
    FROM reservas_hotel
""")

reservas_hotel = cursor.fetchall()

for reserva in reservas_hotel:

    cursor.execute("""
        INSERT INTO pagamentos (
            tipo_reserva,
            id_reserva,
            valor,
            metodo_pagamento,
            status
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        'hotel',
        reserva[0],
        reserva[1],
        random.choice([
            'credit_card',
            'pix',
            'boleto'
        ]),
        random.choice([
            'pending',
            'paid',
            'failed',
            'refunded'
        ])
    ))

conn.commit()

print("Pagamentos inseridos!")


cursor.close()
conn.close()

print("Conexão encerrada!")
