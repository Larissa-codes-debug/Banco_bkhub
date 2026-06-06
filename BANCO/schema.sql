CREATE TABLE airports (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE hotels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    stars INTEGER CHECK (stars BETWEEN 1 AND 5),
    address VARCHAR(255)
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    flight_number VARCHAR(20) UNIQUE NOT NULL,

    origin_airport_id INTEGER NOT NULL,
    destination_airport_id INTEGER NOT NULL,

    departure_time TIMESTAMP NOT NULL,
    arrival_time TIMESTAMP NOT NULL,

    total_seats INTEGER NOT NULL CHECK (total_seats > 0),
    available_seats INTEGER NOT NULL CHECK (available_seats >= 0),

    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),

    CONSTRAINT fk_origin_airport
        FOREIGN KEY (origin_airport_id)
        REFERENCES airports(id),

    CONSTRAINT fk_destination_airport
        FOREIGN KEY (destination_airport_id)
        REFERENCES airports(id),

    CONSTRAINT chk_different_airports
        CHECK (origin_airport_id <> destination_airport_id)
);

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,

    hotel_id INTEGER NOT NULL,

    room_number VARCHAR(10) NOT NULL,

    type VARCHAR(20) NOT NULL
        CHECK (type IN ('single', 'double', 'suite')),

    capacity INTEGER NOT NULL CHECK (capacity > 0),

    price_per_night DECIMAL(10,2) NOT NULL
        CHECK (price_per_night >= 0),

    CONSTRAINT fk_room_hotel
        FOREIGN KEY (hotel_id)
        REFERENCES hotels(id)
        ON DELETE CASCADE
);

CREATE TABLE flight_reservations (
    id SERIAL PRIMARY KEY,

    customer_id INTEGER NOT NULL,
    flight_id INTEGER NOT NULL,

    seat_number VARCHAR(10),

    status VARCHAR(20) NOT NULL
        CHECK (status IN ('pending', 'confirmed', 'cancelled')),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_flight_res_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_flight_res_flight
        FOREIGN KEY (flight_id)
        REFERENCES flights(id)
        ON DELETE CASCADE
);

CREATE TABLE hotel_reservations (
    id SERIAL PRIMARY KEY,

    customer_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,

    check_in DATE NOT NULL,
    check_out DATE NOT NULL,

    status VARCHAR(20) NOT NULL
        CHECK (status IN ('pending', 'confirmed', 'cancelled')),

    total_price DECIMAL(10,2) NOT NULL
        CHECK (total_price >= 0),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_hotel_res_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_hotel_res_room
        FOREIGN KEY (room_id)
        REFERENCES rooms(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_dates
        CHECK (check_out > check_in)
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,

    reservation_type VARCHAR(20) NOT NULL
        CHECK (reservation_type IN ('flight', 'hotel')),

    reservation_id INTEGER NOT NULL,

    amount DECIMAL(10,2) NOT NULL
        CHECK (amount >= 0),

    status VARCHAR(20) NOT NULL
        CHECK (status IN ('pending', 'paid', 'failed', 'refunded')),

    payment_method VARCHAR(50) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
