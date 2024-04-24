LOAD DATA INFILE 'weapons_export_2024-04-22_081519.csv'
INTO TABLE weapon
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, name);

LOAD DATA INFILE '250k_with_gameid.csv'
INTO TABLE kill_logs
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(killer_hash, killed_hash, game_id, weapon_id, @kill_date)
SET kill_date = STR_TO_DATE(@kill_date, '%Y-%m-%d %H:%i:%s');

LOAD DATA INFILE 'maps.csv'
INTO TABLE maps
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, name, type);

LOAD DATA INFILE 'game_data.csv'
INTO TABLE game_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, map, is_private, date);
