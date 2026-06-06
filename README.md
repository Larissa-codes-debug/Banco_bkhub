## Integrantes
- Larissa Lopes
- Ingrid Silveira

## Como executar
1. Restaurar o banco de dados.
2. Instalar dependências.
3. Executar:
   uvicorn main:app --reload

## Repositório
https://github.com/Larissa-codes-debug/Banco_bkhub

Startup,indicações do projeto e orientações. 

"A startup BookingHub está desenvolvendo uma plataforma online de reservas de hotéis
e passagens aéreas. Durante períodos de alta temporada, a plataforma recebe dezenas de
milhares de requisições simultâneas, exigindo que o banco de dados seja capaz de sustentar
alto volume com consistência e disponibilidade.
Neste trabalho, vocês atuarão como a equipe de engenharia de dados da BookingHub. A
missão é construir o backend da plataforma — composto por uma API REST em Python
e um banco de dados PostgreSQL — com atenção especial a três pilares fundamentais:
• Processamento eficiente de consultas: uso de índices, análise de planos de execução
e otimização de queries;
• Controle de transações e concorrência: garantindo consistência e evitando problemas como overbooking;
• Estratégias de recuperação de falhas: WAL, backups e restauração pontual.
O trabalho é avaliado tanto pela implementação técnica quanto pela análise e reflexão
documentadas no relatório."


 Python
- FastAPI
- PostgreSQL
- psycopg2
- Faker
- GitHub

## Estrutura do projeto

bash
dashboard/
│
├── API/              # Código da API FastAPI
├── BANCO/            # Scripts SQL, schema e seed
├── FRONTEND/         # Telas do sistema
├── TESTES/           # Testes de concorrência e isolamento
├── .gitignore        #Arquivos não alocados a máquina já tem que estar configurada.
└── README.md          #Instruções de uso.

http://127.0.0.1:8000/docs

GET /voos/disponiveis
GET /hoteis/disponiveis
GET /clientes/{id}/reservas
GET /relatorios/ocupacao
POST /reservas/voo



| Consulta | Tempo Antes                         | Tempo Depois |
| -------- | ----------------------------------- | ------------ |
| C1       | 0,077 ms                            | 0,058 ms     |
| C2       | 1,4 ms (estimado do plano anterior) | 1,171 ms     |
| C3       | 0,098 ms                            | 0,145 ms     |
| C4       | 0,138 ms                            | 0,574 ms     |





| Índice                                | Tipo   | Justificativa                    |
| ------------------------------------- | ------ | -------------------------------- |
| idx_flights_departure_time            | B-Tree | Busca por intervalo de datas     |
| idx_rooms_hotel                       | B-Tree | Busca por igualdade (`hotel_id`) |
| idx_flight_reservations_customer      | B-Tree | Filtro por cliente               |
| idx_payments_reservation              | B-Tree | Junções por tipo e id da reserva |
| idx_flight_reservations_flight_status | B-Tree | Filtro por voo e status          |
| idx_airports_city                     | B-Tree | Busca por cidade                 |
