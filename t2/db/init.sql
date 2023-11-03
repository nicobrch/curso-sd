CREATE TABLE Maestro (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    email VARCHAR UNIQUE,
    stock INTEGER DEFAULT 0,
    secret_key VARCHAR(255)
);

CREATE TABLE Venta (
    id SERIAL PRIMARY KEY,
    maestro_id INTEGER,
    monto INTEGER,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (maestro_id) REFERENCES Maestro(id)
);

CREATE TABLE Reposicion (
    id SERIAL PRIMARY KEY,
    maestro_id INTEGER,
    stock INTEGER,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (maestro_id) REFERENCES Maestro(id)
);

INSERT INTO maestro (nombre, email, stock, secret_key)
VALUES
    ('John Doe', 'john.doe@example.com', 10, 'secret_key_1'),
    ('Alice Smith', 'alice.smith@example.com', 10, 'secret_key_2'),
    ('Bob Johnson', 'bob.johnson@example.com', 10, 'secret_key_3');