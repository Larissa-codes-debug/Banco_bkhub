Desconsidere os arquivos soltos, para ter a versão completa utilize as pastas.

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
POST /reservas/hotel
POST /pagamentos
DELETE /reservas/{id}
POST /test/falha-transacao
