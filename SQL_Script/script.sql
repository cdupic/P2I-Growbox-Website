ALTER TABLE Users MODIFY token VARCHAR(32);
INSERT INTO Users (user_name,password, token) VALUES ('test', 'test', '7713d075cae2f40323802bb73b355114');