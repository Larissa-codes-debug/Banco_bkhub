from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal
from datetime import date, datetime


app = FastAPI(
    title="BookingHub API",
    description="API conectada ao banco BookingHub com tabelas em inglês",
    version="1.0"
)


# =========================
# CONEXÃO COM O BANCO
# =========================

def conectar():
    return psycopg2.connect(
        host="localhost",
        port="5433",
        database="banco_bkhub",
        user="postgres",
        password="1810",
        client_encoding="UTF8"
    )


def converter_dados(valor):
    if isinstance(valor, list):
        return [converter_dados(item) for item in valor]

    if isinstance(valor, dict):
        return {chave: converter_dados(valor[chave]) for chave in valor}

    if isinstance(valor, Decimal):
        return float(valor)

    if isinstance(valor, (date, datetime)):
        return valor.isoformat()

    return valor


# =========================
# MODELOS
# =========================

class Customer(BaseModel):
    name: str
    email: str
    cpf: str
    phone: str | None = None


class Airport(BaseModel):
    code: str
    name: str
    city: str
    country: str


class Hotel(BaseModel):
    name: str
    city: str
    country: str
    stars: int
    address: str | None = None


class Room(BaseModel):
    hotel_id: int
    room_number: str
    type: str
    capacity: int
    price_per_night: float


class Flight(BaseModel):
    flight_number: str
    origin_airport_id: int
    destination_airport_id: int
    departure_time: str
    arrival_time: str
    total_seats: int
    available_seats: int
    price: float


class FlightReservation(BaseModel):
    customer_id: int
    flight_id: int
    seat_number: str
    status: str = "confirmed"


class HotelReservation(BaseModel):
    customer_id: int
    room_id: int
    check_in: str
    check_out: str
    status: str = "confirmed"
    total_price: float


class Payment(BaseModel):
    reservation_type: str
    reservation_id: int
    amount: float
    status: str
    payment_method: str


# =========================
# ROTAS DE TESTE
# =========================

@app.get("/")
def home():
    return {"message": "BookingHub API funcionando"}


@app.get("/test-database")
def test_database():
    try:
        conn = conectar()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT COUNT(*) AS total_airports FROM airports;")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return {
            "status": "connected",
            "message": "Banco conectado com sucesso",
            "result": result
        }

    except Exception as erro:
        raise HTTPException(status_code=500, detail=str(erro))


# =========================
# CUSTOMERS
# =========================

@app.get("/customers")
def list_customers():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id, name, email, cpf, phone, created_at
        FROM customers
        ORDER BY id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return converter_dados(data)


@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id, name, email, cpf, phone, created_at
        FROM customers
        WHERE id = %s
    """, (customer_id,))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    if not data:
        raise HTTPException(status_code=404, detail="Customer not found")

    return converter_dados(data)


@app.post("/customers")
def create_customer(customer: Customer):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("""
            INSERT INTO customers (name, email, cpf, phone)
            VALUES (%s, %s, %s, %s)
            RETURNING id, name, email, cpf, phone, created_at
        """, (
            customer.name,
            customer.email,
            customer.cpf,
            customer.phone
        ))

        new_customer = cursor.fetchone()
        conn.commit()

        return converter_dados({
            "message": "Customer created successfully",
            "customer": new_customer
        })

    except Exception as erro:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(erro))

    finally:
        cursor.close()
        conn.close()


@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("""
            UPDATE customers
            SET name = %s,
                email = %s,
                cpf = %s,
                phone = %s
            WHERE id = %s
            RETURNING id, name, email, cpf, phone, created_at
        """, (
            customer.name,
            customer.email,
            customer.cpf,
            customer.phone,
            customer_id
        ))

        updated_customer = cursor.fetchone()
        conn.commit()

        if not updated_customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        return converter_dados({
            "message": "Customer updated successfully",
            "customer": updated_customer
        })

    except HTTPException:
        raise

    except Exception as erro:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(erro))

    finally:
        cursor.close()
        conn.close()


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM customers
            WHERE id = %s
        """, (customer_id,))

        conn.commit()

        return {"message": "Customer deleted successfully"}

    except Exception as erro:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(erro))

    finally:
        cursor.close()
        conn.close()


# =========================
# AIRPORTS
# =========================

@app.get("/airports")
def list_airports():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id, code, name, city, country
        FROM airports
        ORDER BY id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return converter_dados(data)


@app.get("/airports/{airport_id}")
def get_airport(airport_id: int):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id, code, name, city, country
        FROM airports
        WHERE id = %s
    """, (airport_id,))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    if not data:
        raise HTTPException(status_code=404, detail="Airport not found")

    return converter_dados(data)


@app.post("/airports")
def create_airport(airport: Airport):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("""
            INSERT INTO airports (code, name, city, country)
            VALUES (%s, %s, %s, %s)
            RETURNING id, code, name, city, country
        """, (
            airport.code,
            airport.name,
            airport.city,
            airport.country
        ))

        new_airport = cursor.fetchone()
        conn.commit()

        return converter_dados({
            "message": "Airport created successfully",
            "airport": new_airport
        })

    except Exception as erro:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(erro))

    finally:
        cursor.close()
        conn.close()


# =========================
# HOTELS
# =========================

@app.get("/hotels")
def list_hotels():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id, name, city, country, stars, address
        FROM hotels
        ORDER BY id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return converter_dados(data)

@app.post("/test/falha-transacao")
def falha_transacao():

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("BEGIN")

        cur.execute("""
            INSERT INTO reservas_voo
            (id_cliente, id_voo, numero_assento, status)
            VALUES (1, 1, '99Z', 'confirmed')
        """)

        # erro proposital
        raise Exception("Erro proposital")

        conn.commit()

    except Exception as e:

        conn.rollback()

        return {
            "mensagem": "Rollback executado com sucesso",
            "erro": str(e)
        }

    finally:
        cur.close()
        conn.close()


@app.get("/hotels/{hotel_id}")
def get_hotel(hotel_id: int):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id, name, city, country, stars, address
        FROM hotels
        WHERE id = %s
    """, (hotel_id,))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    if not data:
        raise HTTPException(status_code=404, detail="Hotel not found")

    return converter_dados(data)


@app.post("/hotels")
def create_hotel(hotel: Hotel):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("""
            INSERT INTO hotels (name, city, country, stars, address)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, name, city, country, stars, address
        """, (
            hotel.name,
            hotel.city,
            hotel.country,
            hotel.stars,
            hotel.address
        ))

        new_hotel = cursor.fetchone()
        conn.commit()

        return converter_dados({
            "message": "Hotel created successfully",
            "hotel": new_hotel
        })

    except Exception as erro:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(erro))

    finally:
        cursor.close()
        conn.close()


# =========================
# ROOMS
# =========================

@app.get("/rooms")
def list_rooms():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            r.id,
            r.hotel_id,
            h.name AS hotel_name,
            r.room_number,
            r.type,
            r.capacity,
            r.price_per_night
        FROM rooms r
        JOIN hotels h ON h.id = r.hotel_id
        ORDER BY r.id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return converter_dados(data)


@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            r.id,
            r.hotel_id,
            h.name AS hotel_name,
            r.room_number,
            r.type,
            r.capacity,
            r.price_per_night
        FROM rooms r
        JOIN hotels h ON h.id = r.hotel_id
        WHERE r.id = %s
    """, (room_id,))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    if not data:
        raise HTTPException(status_code=404, detail="Room not found")

    return converter_dados(data)


@app.post("/rooms")
def create_room(room: Room):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("""
            INSERT INTO rooms
            (hotel_id, room_number, type, capacity, price_per_night)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, hotel_id, room_number, type, capacity, price_per_night
        """, (
            room.hotel_id,
            room.room_number,
            room.type,
            room.capacity,
            room.price_per_night
        ))

        new_room = cursor.fetchone()
        conn.commit()

        return converter_dados({
            "message": "Room created successfully",
            "room": new_room
        })

    except Exception as erro:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(erro))

    finally:
        cursor.close()
        conn.close()


# =========================
# FLIGHTS
# =========================

@app.get("/flights")
def list_flights():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            f.id,
            f.flight_number,
            f.origin_airport_id,
            origin.code AS origin_code,
            origin.city AS origin_city,
            f.destination_airport_id,
            destination.code AS destination_code,
            destination.city AS destination_city,
            f.departure_time,
            f.arrival_time,
            f.total_seats,
            f.available_seats,
            f.price
        FROM flights f
        JOIN airports origin ON origin.id = f.origin_airport_id
        JOIN airports destination ON destination.id = f.destination_airport_id
        ORDER BY f.id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return converter_dados(data)


@app.get("/flights/available")
def list_available_flights():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            f.id,
            f.flight_number,
            origin.code AS origin_code,
            origin.city AS origin_city,
            destination.code AS destination_code,
            destination.city AS destination_city,
            f.departure_time,
            f.arrival_time,
            f.available_seats,
            f.price
        FROM flights f
        JOIN airports origin ON origin.id = f.origin_airport_id
        JOIN airports destination ON destination.id = f.destination_airport_id
        WHERE f.available_seats > 0
        ORDER BY f.departure_time
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return converter_dados(data)


@app.get("/flights/{flight_id}")
def get_flight(flight_id: int):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            f.id,
            f.flight_number,
            f.origin_airport_id,
            origin.code AS origin_code,
            origin.city AS origin_city,
            f.destination_airport_id,
            destination.code AS destination_code,
            destination.city AS destination_city,
            f.departure_time,
            f.arrival_time,
            f.total_seats,
            f.available_seats,
            f.price
        FROM flights f
        JOIN airports origin ON origin.id = f.origin_airport_id
        JOIN airports destination ON destination.id = f.destination_airport_id
        WHERE f.id = %s
    """, (flight_id,))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    if not data:
        raise HTTPException(status_code=404, detail="Flight not found")

    return converter_dados(data)


@app.post("/flights")
def create_flight(flight: Flight):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("""
            INSERT INTO flights
            (
                flight_number,
                origin_airport_id,
                destination_airport_id,
                departure_time,
                arrival_time,
                total_seats,
                available_seats,
                price
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            flight.flight_number,
            flight.origin_airport_id,
            flight.destination_airport_id,
            flight.departure_time,
            flight.arrival_time,
            flight.total_seats,
            flight.available_seats,
            flight.price
        ))

        new_flight = cursor.fetchone()
        conn.commit()

        return converter_dados({
            "message": "Flight created successfully",
            "flight": new_flight
        })

    except Exception as erro:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(erro))

    finally:
        cursor.close()
        conn.close()


# =========================
# AVAILABLE HOTELS
# =========================

@app.get("/hotels/available")
def list_available_hotels(
    city: str | None = None,
    check_in: str | None = None,
    check_out: str | None = None
):
    if not check_in or not check_out:
        raise HTTPException(
            status_code=400,
            detail="Informe check_in e check_out. Exemplo: 2026-06-10 e 2026-06-15"
        )

    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    sql = """
        SELECT DISTINCT
            h.id AS hotel_id,
            h.name,
            h.city,
            h.country,
            h.stars,
            h.address,
            r.id AS room_id,
            r.room_number,
            r.type,
            r.capacity,
            r.price_per_night
        FROM hotels h
        JOIN rooms r ON r.hotel_id = h.id
        WHERE r.id NOT IN (
            SELECT hr.room_id
            FROM hotel_reservations hr
            WHERE hr.status != 'cancelled'
            AND hr.check_in < %s
            AND hr.check_out > %s
        )
    """

    parameters = [check_out, check_in]

    if city:
        sql += " AND h.city ILIKE %s"
        parameters.append(f"%{city}%")

    sql += " ORDER BY h.name, r.room_number"

    cursor.execute(sql, parameters)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return converter_dados(data)


# =========================
# FLIGHT RESERVATIONS
# =========================

@app.post("/flight-reservations")
def create_flight_reservation(reservation: FlightReservation):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("BEGIN")

        cursor.execute("""
            SELECT id, available_seats
            FROM flights
            WHERE id = %s
            FOR UPDATE
        """, (reservation.flight_id,))

        flight = cursor.fetchone()

        if not flight:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Flight not found")

        if flight["available_seats"] <= 0:
            conn.rollback()
            raise HTTPException(status_code=409, detail="No seats available")

        cursor.execute("""
            SELECT id
            FROM flight_reservations
            WHERE flight_id = %s
            AND seat_number = %s
            AND status != 'cancelled'
        """, (
            reservation.flight_id,
            reservation.seat_number
        ))

        occupied_seat = cursor.fetchone()

        if occupied_seat:
            conn.rollback()
            raise HTTPException(status_code=409, detail="Seat already reserved")

        cursor.execute("""
            INSERT INTO flight_reservations
            (customer_id, flight_id, seat_number, status)
            VALUES (%s, %s, %s, %s)
            RETURNING *
        """, (
            reservation.customer_id,
            reservation.flight_id,
            reservation.seat_number,
            reservation.status
        ))

        new_reservation = cursor.fetchone()

        cursor.execute("""
            UPDATE flights
            SET available_seats = available_seats - 1
            WHERE id = %s
        """, (reservation.flight_id,))

        conn.commit()

        return converter_dados({
            "message": "Flight reservation created successfully",
            "reservation": new_reservation
        })

    except HTTPException:
        raise

    except Exception as erro:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(erro))

    finally:
        cursor.close()
        conn.close()


@app.get("/flight-reservations")
def list_flight_reservations():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            fr.id,
            fr.customer_id,
            c.name AS customer_name,
            fr.flight_id,
            f.flight_number,
            fr.seat_number,
            fr.status
        FROM flight_reservations fr
        JOIN customers c ON c.id = fr.customer_id
        JOIN flights f ON f.id = fr.flight_id
        ORDER BY fr.id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return converter_dados(data)


# =========================
# HOTEL RESERVATIONS
# =========================

@app.post("/hotel-reservations")
def create_hotel_reservation(reservation: HotelReservation):
    conn = conectar()
    conn.set_session(isolation_level="SERIALIZABLE")
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("BEGIN")

        cursor.execute("""
            SELECT id
            FROM rooms
            WHERE id = %s
            FOR UPDATE
        """, (reservation.room_id,))

        room = cursor.fetchone()

        if not room:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Room not found")

        cursor.execute("""
            SELECT id
            FROM hotel_reservations
            WHERE room_id = %s
            AND status != 'cancelled'
            AND check_in < %s
            AND check_out > %s
        """, (
            reservation.room_id,
            reservation.check_out,
            reservation.check_in
        ))

        conflict = cursor.fetchone()

        if conflict:
            conn.rollback()
            raise HTTPException(
                status_code=409,
                detail="Room already reserved in this period"
            )

        cursor.execute("""
            INSERT INTO hotel_reservations
            (customer_id, room_id, check_in, check_out, status, total_price)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            reservation.customer_id,
            reservation.room_id,
            reservation.check_in,
            reservation.check_out,
            reservation.status,
            reservation.total_price
        ))

        new_reservation = cursor.fetchone()

        conn.commit()

        return converter_dados({
            "message": "Hotel reservation created successfully",
            "reservation": new_reservation
        })

    except HTTPException:
        raise

    except Exception as erro:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(erro))

    finally:
        cursor.close()
        conn.close()


@app.get("/hotel-reservations")
def list_hotel_reservations():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            hr.id,
            hr.customer_id,
            c.name AS customer_name,
            hr.room_id,
            r.room_number,
            h.name AS hotel_name,
            hr.check_in,
            hr.check_out,
            hr.status,
            hr.total_price
        FROM hotel_reservations hr
        JOIN customers c ON c.id = hr.customer_id
        JOIN rooms r ON r.id = hr.room_id
        JOIN hotels h ON h.id = r.hotel_id
        ORDER BY hr.id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return converter_dados(data)


# =========================
# CUSTOMER RESERVATION HISTORY
# =========================

@app.get("/customers/{customer_id}/reservations")
def customer_reservation_history(customer_id: int):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            'flight' AS type,
            fr.id AS reservation_id,
            f.flight_number AS description,
            f.departure_time AS reservation_date,
            fr.status,
            p.amount AS payment_amount,
            p.status AS payment_status
        FROM flight_reservations fr
        JOIN flights f ON f.id = fr.flight_id
        LEFT JOIN payments p
            ON p.reservation_id = fr.id
            AND p.reservation_type = 'flight'
        WHERE fr.customer_id = %s

        UNION ALL

        SELECT
            'hotel' AS type,
            hr.id AS reservation_id,
            h.name AS description,
            hr.check_in AS reservation_date,
            hr.status,
            p.amount AS payment_amount,
            p.status AS payment_status
        FROM hotel_reservations hr
        JOIN rooms r ON r.id = hr.room_id
        JOIN hotels h ON h.id = r.hotel_id
        LEFT JOIN payments p
            ON p.reservation_id = hr.id
            AND p.reservation_type = 'hotel'
        WHERE hr.customer_id = %s

        ORDER BY reservation_date DESC
    """, (
        customer_id,
        customer_id
    ))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return converter_dados(data)


# =========================
# PAYMENTS
# =========================

@app.get("/payments")
def list_payments():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id, reservation_type, reservation_id, amount, status, payment_method, created_at
        FROM payments
        ORDER BY id
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return converter_dados(data)


@app.post("/payments")
def create_payment(payment: Payment):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("BEGIN")

        cursor.execute("""
            INSERT INTO payments
            (reservation_type, reservation_id, amount, status, payment_method)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
        """, (
            payment.reservation_type,
            payment.reservation_id,
            payment.amount,
            payment.status,
            payment.payment_method
        ))

        new_payment = cursor.fetchone()

        if payment.status in ["paid", "pago"]:
            if payment.reservation_type == "flight":
                cursor.execute("""
                    UPDATE flight_reservations
                    SET status = 'confirmed'
                    WHERE id = %s
                """, (payment.reservation_id,))

            elif payment.reservation_type == "hotel":
                cursor.execute("""
                    UPDATE hotel_reservations
                    SET status = 'confirmed'
                    WHERE id = %s
                """, (payment.reservation_id,))

        conn.commit()

        return converter_dados({
            "message": "Payment registered successfully",
            "payment": new_payment
        })

    except Exception as erro:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(erro))

    finally:
        cursor.close()
        conn.close()


# =========================
# CANCEL RESERVATION
# =========================

@app.delete("/reservations/{reservation_id}")
def cancel_reservation(reservation_id: int, reservation_type: str):
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("BEGIN")

        if reservation_type == "flight":
            cursor.execute("""
                SELECT flight_id, status
                FROM flight_reservations
                WHERE id = %s
                FOR UPDATE
            """, (reservation_id,))

            reservation = cursor.fetchone()

            if not reservation:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Flight reservation not found")

            if reservation["status"] != "cancelled":
                cursor.execute("""
                    UPDATE flight_reservations
                    SET status = 'cancelled'
                    WHERE id = %s
                """, (reservation_id,))

                cursor.execute("""
                    UPDATE flights
                    SET available_seats = available_seats + 1
                    WHERE id = %s
                """, (reservation["flight_id"],))

        elif reservation_type == "hotel":
            cursor.execute("""
                SELECT id, status
                FROM hotel_reservations
                WHERE id = %s
                FOR UPDATE
            """, (reservation_id,))

            reservation = cursor.fetchone()

            if not reservation:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Hotel reservation not found")

            cursor.execute("""
                UPDATE hotel_reservations
                SET status = 'cancelled'
                WHERE id = %s
            """, (reservation_id,))

        else:
            conn.rollback()
            raise HTTPException(
                status_code=400,
                detail="Invalid reservation_type. Use flight or hotel"
            )

        conn.commit()

        return {
            "message": "Reservation cancelled successfully",
            "reservation_type": reservation_type,
            "reservation_id": reservation_id
        }

    except HTTPException:
        raise

    except Exception as erro:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(erro))

    finally:
        cursor.close()
        conn.close()


# =========================
# OCCUPANCY REPORT
# =========================

@app.get("/reports/occupancy")
def occupancy_report():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            f.id,
            f.flight_number,
            f.total_seats,
            COUNT(fr.id) AS total_reservations,
            ROUND(
                COUNT(fr.id)::numeric / f.total_seats * 100,
                2
            ) AS occupancy_percentage
        FROM flights f
        LEFT JOIN flight_reservations fr
            ON fr.flight_id = f.id
            AND fr.status = 'confirmed'
        GROUP BY f.id, f.flight_number, f.total_seats
        ORDER BY occupancy_percentage DESC
    """)

    flight_occupancy = cursor.fetchall()

    cursor.execute("""
        SELECT
            h.name AS hotel,
            r.id AS room_id,
            r.room_number,
            r.type,
            COUNT(hr.id) AS total_reservations
        FROM rooms r
        JOIN hotels h ON h.id = r.hotel_id
        LEFT JOIN hotel_reservations hr
            ON hr.room_id = r.id
            AND hr.status = 'confirmed'
        GROUP BY h.name, r.id, r.room_number, r.type
        ORDER BY total_reservations DESC
    """)

    hotel_occupancy = cursor.fetchall()

    cursor.close()
    conn.close()

    return converter_dados({
        "flight_occupancy": flight_occupancy,
        "hotel_occupancy": hotel_occupancy
    })


# =========================
# TRANSACTION FAILURE TEST
# =========================

@app.post("/test/transaction-failure")
def test_transaction_failure():
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("BEGIN")

        cursor.execute("""
            INSERT INTO flight_reservations
            (customer_id, flight_id, seat_number, status)
            VALUES (1, 1, 'TEST-FAILURE', 'pending')
        """)

        raise Exception("Simulated failure before COMMIT")

    except Exception as erro:
        conn.rollback()
        return {
            "message": "Rollback executed successfully. The reservation was not saved.",
            "simulated_error": str(erro)
        }

    finally:
        cursor.close()
        conn.close()
