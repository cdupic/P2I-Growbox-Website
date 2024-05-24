ALTER TABLE Users MODIFY password binary(41);

INSERT INTO Users (user_name,password, auth_token) VALUES ('test', PASSWORD('test'), '7713d075cae2f40323802bb73b355114');

