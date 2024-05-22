CREATE TABLE Plants
(
    id            INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name          VARCHAR(16),
    temperature   FLOAT, # in °C
    soil_humidity INT,   # in %
    air_humidity  INT,   # in %
    light         INT,   # in lux
    O2            FLOAT  # in %
);

CREATE TABLE Users
(
    pseudo VARCHAR(16) PRIMARY KEY,
    password VARCHAR(32),
    date_registration DATETIME DEFAULT NOW()
);

CREATE TABLE GreenHouses
(
    serial_number   VARCHAR(32) PRIMARY KEY,
    name            VARCHAR(16),
    update_interval INT UNSIGNED,   # in seconds
    plant_init_date DATETIME DEFAULT NOW(),
    temperature     FLOAT, # in °C
    soil_humidity   INT,   # in %
    air_humidity    INT,   # in %
    light           INT,   # in lux
    O2              FLOAT, # in %
    pseudo          VARCHAR(16),
    FOREIGN KEY (pseudo) REFERENCES Users (pseudo)
);

CREATE TABLE GreenHousePlants
(
    id              INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    plant_id        INT UNSIGNED,
    serial_number   VARCHAR(32),
    date_debut DATETIME DEFAULT NOW(),
    date_fin DATETIME DEFAULT NULL,
    FOREIGN KEY (plant_id) REFERENCES Plants (id),
    FOREIGN KEY (serial_number) REFERENCES GreenHouses (serial_number)
);


CREATE TABLE Sensors
(
    id              TINYINT UNSIGNED,
    serial_number   VARCHAR(32),
    type            ENUM ('temperature', 'soil_humidity', 'air_humidity', 'light', 'O2', 'water_level'),
    unit            VARCHAR(16),
    PRIMARY KEY (id, serial_number),
    FOREIGN KEY (serial_number) REFERENCES GreenHouses (serial_number)
);


CREATE TABLE Measures
(
    sensor_id TINYINT UNSIGNED,
    date      DATETIME DEFAULT NOW(),
    value     FLOAT,
    FOREIGN KEY (sensor_id) REFERENCES Sensors (id),
    PRIMARY KEY (sensor_id, date)
);


CREATE TABLE Actuators
(
    id              TINYINT UNSIGNED,
    serial_number   VARCHAR(32),
    type            ENUM ('temperature', 'soil_humidity', 'air_humidity', 'light', 'O2', 'water_level'),
    FOREIGN KEY (serial_number) REFERENCES GreenHouses (serial_number),
    PRIMARY KEY (id, serial_number)
);


CREATE TABLE Actions
(
    actuator_id TINYINT UNSIGNED,
    date        DATETIME DEFAULT NOW(),
    value       FLOAT,
    FOREIGN KEY (actuator_id) REFERENCES Actuators (id),
    PRIMARY KEY (actuator_id, date)
);