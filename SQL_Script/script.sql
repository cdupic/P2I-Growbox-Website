
INSERT INTO Users (user_name,password, auth_token) VALUES ('test', PASSWORD('test'), '7713d075cae2f40323802bb73b355114');

INSERT INTO GreenHouses (serial, name, update_interval, temperature, soil_humidity, air_humidity, light, O2, user_name) VALUES ('GB-01', 'GrowBow V1', 10, 20, 50, 50, 1000, 21, 'test');
