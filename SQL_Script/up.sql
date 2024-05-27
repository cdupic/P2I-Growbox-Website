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
    user_name VARCHAR(16) PRIMARY KEY,
    password VARBINARY(64),
    date_registration DATETIME DEFAULT NOW(),
    auth_token varchar(32)
);

CREATE TABLE GreenHouses
(
    serial   VARCHAR(32) PRIMARY KEY,
    name            VARCHAR(16),
    update_interval INT UNSIGNED,   # in seconds
    plant_init_date DATETIME DEFAULT NOW(),
    temperature     FLOAT, # in °C
    soil_humidity   INT,   # in %
    air_humidity    INT,   # in %
    light           INT,   # in lux
    O2              FLOAT, # in %
    user_name       VARCHAR(16),
    FOREIGN KEY (user_name) REFERENCES Users (user_name)
);

CREATE TABLE GreenHousePlants
(
    id              INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    plant_id        INT UNSIGNED,
    greenhouse_serial   VARCHAR(32),
    date_start DATETIME DEFAULT NOW(),
    date_end DATETIME DEFAULT NULL,
    FOREIGN KEY (plant_id) REFERENCES Plants (id),
    FOREIGN KEY (greenhouse_serial) REFERENCES GreenHouses (serial)
);


CREATE TABLE Sensors
(
    id              TINYINT UNSIGNED,
    greenhouse_serial   VARCHAR(32),
    type            ENUM ('temperature', 'soil_humidity', 'air_humidity', 'light', 'O2', 'water_level'),
    PRIMARY KEY (id, greenhouse_serial),
    FOREIGN KEY (greenhouse_serial) REFERENCES GreenHouses (serial)
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
    greenhouse_serial   VARCHAR(32),
    type            ENUM ('temperature', 'soil_humidity', 'air_humidity', 'light', 'O2', 'water_level'),
    FOREIGN KEY (greenhouse_serial) REFERENCES GreenHouses (serial),
    PRIMARY KEY (id, greenhouse_serial)
);


CREATE TABLE Actions
(
    actuator_id TINYINT UNSIGNED,
    date        DATETIME DEFAULT NOW(),
    value       FLOAT,
    FOREIGN KEY (actuator_id) REFERENCES Actuators (id),
    PRIMARY KEY (actuator_id, date)
);
