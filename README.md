# Gun Raiders' kills data

[Gun Raiders](https://gunraiders.com/) is a VR FPS game. This repository contains scripts to analyze a 24-hour dump of game kills logs and the results.

## Tools

DB used is MariaDB. Script is python.

## Repository content

- [create_db.sql](create_db.sql) creates the MariaDB database
- [load_data.sql](load_data.sql) loads data from the CSV files
- [add_weapon_killed_id.py](add_weapon_killed_id.py) computes the weapon_killed_id, an estimation of which weapon the player was likely using when killed (based on previous or next kill)
- [querys.md](querys.md) lists SQL queries and related results
