CREATE TABLE Plants
(
    id            INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name          VARCHAR(32),
    temperature   SMALLINT, # in °C
    soil_humidity SMALLINT,   # in %
    air_humidity  SMALLINT,   # in %
    light         SMALLINT,   # in lux
    O2            SMALLINT,  # in %
    date_bloom  INT UNSIGNED DEFAULT 0
);

CREATE TABLE Users
(
    user_name VARCHAR(16) PRIMARY KEY,
    password VARBINARY(64),
    date_registration DATETIME DEFAULT UTC_TIMESTAMP(),
    auth_token varchar(32)
);

CREATE TABLE GreenHouses
(
    serial   VARCHAR(32) PRIMARY KEY,
    update_interval INT UNSIGNED,   # in minutes
    plant_init_date DATETIME DEFAULT UTC_TIMESTAMP(),
    temperature     SMALLINT, # in °C (/10)
    soil_humidity   SMALLINT,   # in % (/10)
    air_humidity    SMALLINT,   # in % (/10)
    light           SMALLINT,   # in lux
    O2              SMALLINT, # in % (/10)
    need_downlink  BOOLEAN DEFAULT FALSE,
    is_custom_config BOOLEAN DEFAULT FALSE
);

CREATE TABLE UserGreenHouses
(
    user_name VARCHAR(16),
    greenhouse_serial VARCHAR(32),
    name VARCHAR(32),
    role ENUM ('owner', 'guest', 'collaborator'),
    PRIMARY KEY (user_name, greenhouse_serial),
    FOREIGN KEY (user_name) REFERENCES Users (user_name),
    FOREIGN KEY (greenhouse_serial) REFERENCES GreenHouses (serial)
);


CREATE TABLE GreenHousePlants
(
    id              INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    plant_id        INT UNSIGNED,
    greenhouse_serial   VARCHAR(32),
    count INT UNSIGNED,
    date_start DATETIME DEFAULT UTC_TIMESTAMP(),
    date_end DATETIME DEFAULT NULL,
    FOREIGN KEY (plant_id) REFERENCES Plants (id),
    FOREIGN KEY (greenhouse_serial) REFERENCES GreenHouses (serial)
);

CREATE TABLE Notifications (
                               id INT PRIMARY KEY AUTO_INCREMENT,
                               message VARCHAR(255),
                               date DATETIME DEFAULT CURRENT_TIMESTAMP(),
                               greenhouse_serial VARCHAR(32),
                               notification_type ENUM ('temperature', 'air_humidity', 'soil_humidity', 'light', 'O2', 'water_level', 'new_member', 'new_role', 'drop_plant', 'new_plant', 'custom_config'),
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
    date      DATETIME DEFAULT UTC_TIMESTAMP(),
    value     SMALLINT,
    FOREIGN KEY (sensor_id) REFERENCES Sensors (id),
    PRIMARY KEY (sensor_id, date)
);

CREATE TABLE ProcessedMeasures
(
    sensor_id TINYINT UNSIGNED,
    date      DATETIME,
    value     SMALLINT,
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
    date        DATETIME DEFAULT UTC_TIMESTAMP(),
    value       SMALLINT,
    FOREIGN KEY (actuator_id) REFERENCES Actuators (id),
    PRIMARY KEY (actuator_id, date)
);
