CREATE DATABASE IF NOT EXISTS gr_kills;

USE gr_kills;

CREATE TABLE IF NOT EXISTS weapon (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS kill_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    killer_hash VARCHAR(255) NOT NULL,
    killed_hash VARCHAR(255) NOT NULL,
    game_id INT NOT NULL,
    weapon_id INT NOT NULL,
    kill_date DATETIME NOT NULL,
    weapon_killed_id INT NULL,
    FOREIGN KEY (weapon_id) REFERENCES weapon(id)
);

CREATE TABLE IF NOT EXISTS maps (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type INT
);
