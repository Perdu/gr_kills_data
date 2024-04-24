# Recreate db:
```
drop table kill_logs; drop table weapon;
```
```
sudo mariadb -u root < create_db.sql && sudo mariadb -u root gr_kills < load_data.sql
```

# Kills by weapon:
```sql
select name, count(*) as kills from kill_logs join weapon on weapon_id = weapon.id group by weapon_id order by kills desc;
```

```
+-------------------+-------+
| name              | kills |
+-------------------+-------+
| katana            | 46405 |
| rifle             | 32215 |
| sniper            | 25343 |
| dualUzi           | 18426 |
| knife             | 17944 |
| smg               | 16726 |
| minigun           | 13645 |
| shotgun           | 11805 |
| gauntlet          | 11504 |
| dualpistol        |  9549 |
| rocket            |  8263 |
| revolver          |  7886 |
| flamethrower      |  6618 |
| arrow             |  6195 |
| projectileGrenade |  5499 |
| fusionRifle       |  4491 |
| shuriken          |  2979 |
| crossbowBolt      |  2074 |
| riotShield        |   962 |
| fireBurn          |   912 |
| projectileSmoke   |   518 |
| grappleHook       |    21 |
| bow               |    20 |
+-------------------+-------+
```


# Kills of weapon:
```sql
select name, count(*) as deaths from kill_logs join weapon on weapon_killed_id = weapon.id group by weapon_killed_id order by deaths desc;
```

```
+-------------------+--------+
| name              | deaths |
+-------------------+--------+
| rifle             |  17999 |
| katana            |  17840 |
| dualUzi           |  14795 |
| sniper            |  14030 |
| smg               |  10983 |
| minigun           |   8566 |
| shotgun           |   7478 |
| knife             |   7191 |
| rocket            |   6724 |
| dualpistol        |   6663 |
| revolver          |   6610 |
| flamethrower      |   6527 |
| gauntlet          |   5724 |
| arrow             |   4540 |
| projectileGrenade |   3653 |
| fusionRifle       |   2595 |
| crossbowBolt      |   2075 |
| fireBurn          |   1121 |
| shuriken          |   1112 |
| projectileSmoke   |    725 |
| riotShield        |    597 |
+-------------------+--------+
```


# Nb games:
```sql
select count(distinct game_id) from kill_logs;
```
1806

# Fill kill_logs_full (too long):
```sql
INSERT INTO kill_logs_full (id, killer_hash, killed_hash, game_id, weapon_id, kill_date, weapon_killed_id) select id, killer_hash, killed_hash as a, game_id, weapon_id, kill_date b, (SELECT weapon_id from kill_logs where killer_hash = a and kill_date = (SELECT MAX(kill_date) from kill_logs where killer_hash = a and kill_date < b) limit 1) from kill_logs;
```

# Nb row of killed players who don't have a kill:
```sql
select count(*) from kill_logs where killed_hash not in (select unique killer_hash from kill_logs);
```
66205/250000 = 26.5% (!)

By map type:
```sql
CREATE TEMPORARY TABLE temp_rows AS select count(*) as nb_kill_rows_without_kill from kill_logs join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 1 and killed_hash not in (select unique killer_hash from kill_logs); CREATE TEMPORARY TABLE temp_total_rows AS select count(*) as nb_kill_rows from kill_logs join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 1; SELECT temp_rows.nb_kill_rows_without_kill, temp_total_rows.nb_kill_rows, temp_rows.nb_kill_rows_without_kill/temp_total_rows.nb_kill_rows as ratio FROM temp_rows, temp_total_rows; DROP TEMPORARY TABLE temp_rows; DROP TEMPORARY TABLE temp_total_rows;

CREATE TEMPORARY TABLE temp_rows AS select count(*) as nb_kill_rows_without_kill from kill_logs join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 2 and killed_hash not in (select unique killer_hash from kill_logs); CREATE TEMPORARY TABLE temp_total_rows AS select count(*) as nb_kill_rows from kill_logs join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 2; SELECT temp_rows.nb_kill_rows_without_kill, temp_total_rows.nb_kill_rows, temp_rows.nb_kill_rows_without_kill/temp_total_rows.nb_kill_rows as ratio FROM temp_rows, temp_total_rows; DROP TEMPORARY TABLE temp_rows; DROP TEMPORARY TABLE temp_total_rows;

CREATE TEMPORARY TABLE temp_rows AS select count(*) as nb_kill_rows_without_kill from kill_logs join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 3 and killed_hash not in (select unique killer_hash from kill_logs); CREATE TEMPORARY TABLE temp_total_rows AS select count(*) as nb_kill_rows from kill_logs join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 3; SELECT temp_rows.nb_kill_rows_without_kill, temp_total_rows.nb_kill_rows, temp_rows.nb_kill_rows_without_kill/temp_total_rows.nb_kill_rows as ratio FROM temp_rows, temp_total_rows; DROP TEMPORARY TABLE temp_rows; DROP TEMPORARY TABLE temp_total_rows;
```

Arena:
```
+---------------------------+--------------+--------+
| nb_kill_rows_without_kill | nb_kill_rows | ratio  |
+---------------------------+--------------+--------+
|                      3971 |       137719 | 0.0288 |
+---------------------------+--------------+--------+
```

Hub:
```
+---------------------------+--------------+--------+
| nb_kill_rows_without_kill | nb_kill_rows | ratio  |
+---------------------------+--------------+--------+
|                     53443 |        87290 | 0.6122 |
+---------------------------+--------------+--------+
```

BR:
```
+---------------------------+--------------+--------+
| nb_kill_rows_without_kill | nb_kill_rows | ratio  |
+---------------------------+--------------+--------+
|                      8789 |        24986 | 0.3518 |
+---------------------------+--------------+--------+
```

# Nb of killed players who don't have a kill:
```sql
select count(distinct killed_hash) from kill_logs where killed_hash not in (select unique killer_hash from kill_logs);
```
/
```
select count(distinct killed_hash) from kill_logs;
```
7751/12110 = 64% (!!)

By map type:
```sql
CREATE TEMPORARY TABLE temp_players AS select count(distinct killed_hash) as nb_killed_players_without_kill from kill_logs join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 1 and killed_hash not in (select unique killer_hash from kill_logs);
CREATE TEMPORARY TABLE temp_total_players AS select count(distinct killed_hash) as nb_killed_players from kill_logs join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 1;
SELECT temp_players.nb_killed_players_without_kill, temp_total_players.nb_killed_players, temp_players.nb_killed_players_without_kill/temp_total_players.nb_killed_players as ratio FROM temp_players, temp_total_players;
DROP TEMPORARY TABLE temp_players;
DROP TEMPORARY TABLE temp_total_players;
```
```sql
CREATE TEMPORARY TABLE temp_players AS select count(distinct killed_hash) as nb_killed_players_without_kill from kill_logs join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 2 and killed_hash not in (select unique killer_hash from kill_logs); CREATE TEMPORARY TABLE temp_total_players AS select count(distinct killed_hash) as nb_killed_players from kill_logs join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 2; SELECT temp_players.nb_killed_players_without_kill, temp_total_players.nb_killed_players, temp_players.nb_killed_players_without_kill/temp_total_players.nb_killed_players as ratio FROM temp_players, temp_total_players; DROP TEMPORARY TABLE temp_players; DROP TEMPORARY TABLE temp_total_players;

CREATE TEMPORARY TABLE temp_players AS select count(distinct killed_hash) as nb_killed_players_without_kill from kill_logs join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 3 and killed_hash not in (select unique killer_hash from kill_logs); CREATE TEMPORARY TABLE temp_total_players AS select count(distinct killed_hash) as nb_killed_players from kill_logs join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 3; SELECT temp_players.nb_killed_players_without_kill, temp_total_players.nb_killed_players, temp_players.nb_killed_players_without_kill/temp_total_players.nb_killed_players as ratio FROM temp_players, temp_total_players; DROP TEMPORARY TABLE temp_players; DROP TEMPORARY TABLE temp_total_players;
```

Arena:
```
+--------------------------------+-------------------+--------+
| nb_killed_players_without_kill | nb_killed_players | ratio  |
+--------------------------------+-------------------+--------+
|                            517 |              2771 | 0.1866 |
+--------------------------------+-------------------+--------+
```
Hub:
```
+--------------------------------+-------------------+--------+
| nb_killed_players_without_kill | nb_killed_players | ratio  |
+--------------------------------+-------------------+--------+
|                           6442 |              8962 | 0.7188 |
+--------------------------------+-------------------+--------+
```
BR:
```
+--------------------------------+-------------------+--------+
| nb_killed_players_without_kill | nb_killed_players | ratio  |
+--------------------------------+-------------------+--------+
|                           1198 |              2801 | 0.4277 |
+--------------------------------+-------------------+--------+
```



# kdr (overestimated as we don't know know killed weapon for a lot of rows):
```sql
CREATE TEMPORARY TABLE temp_kills_by_weapon AS select name, count(*) as a from kill_logs join weapon on weapon_id = weapon.id group by weapon_id order by a desc;
CREATE TEMPORARY TABLE temp_kills_of_weapon AS select name, count(*) as a from kill_logs join weapon on weapon_killed_id = weapon.id group by weapon_killed_id order by a desc;
SELECT k1.name, k1.a, k2.a, k1.a / k2.a AS kill_ratio FROM temp_kills_by_weapon k1 JOIN temp_kills_of_weapon k2 ON k1.name = k2.name ORDER BY kill_ratio DESC;
DROP TEMPORARY TABLE temp_kills_by_weapon;
DROP TEMPORARY TABLE temp_kills_of_weapon;
```

```
+-------------------+-------+-------+------------+
| name              | a     | a     | kill_ratio |
+-------------------+-------+-------+------------+
| shuriken          |  2979 |  1112 |     2.6790 |
| katana            | 46405 | 17840 |     2.6012 |
| knife             | 17944 |  7191 |     2.4953 |
| gauntlet          | 11504 |  5724 |     2.0098 |
| sniper            | 25343 | 14030 |     1.8063 |
| rifle             | 32215 | 17999 |     1.7898 |
| fusionRifle       |  4491 |  2595 |     1.7306 |
| riotShield        |   962 |   597 |     1.6114 |
| minigun           | 13645 |  8566 |     1.5929 |
| shotgun           | 11805 |  7478 |     1.5786 |
| smg               | 16726 | 10983 |     1.5229 |
| projectileGrenade |  5499 |  3653 |     1.5053 |
| dualpistol        |  9549 |  6663 |     1.4331 |
| arrow             |  6195 |  4540 |     1.3645 |
| dualUzi           | 18426 | 14795 |     1.2454 |
| rocket            |  8263 |  6724 |     1.2289 |
| revolver          |  7886 |  6610 |     1.1930 |
| flamethrower      |  6618 |  6527 |     1.0139 |
| crossbowBolt      |  2074 |  2075 |     0.9995 |
| fireBurn          |   912 |  1121 |     0.8136 |
| projectileSmoke   |   518 |   725 |     0.7145 |
+-------------------+-------+-------+------------+
```

# kdr, without rows of players that didn't get a kill
```sql
CREATE TEMPORARY TABLE temp_kills_by_weapon AS select name, count(*) as a from kill_logs join weapon on weapon_id = weapon.id where weapon_killed_id is not null group by weapon_id order by a desc; CREATE TEMPORARY TABLE temp_kills_of_weapon AS select name, count(*) as a from kill_logs join weapon on weapon_killed_id = weapon.id group by weapon_killed_id order by a desc; SELECT k1.name, k1.a, k2.a, k1.a / k2.a AS kill_ratio FROM temp_kills_by_weapon k1 JOIN temp_kills_of_weapon k2 ON k1.name = k2.name ORDER BY kill_ratio DESC; DROP TEMPORARY TABLE temp_kills_by_weapon; DROP TEMPORARY TABLE temp_kills_of_weapon;
```

```
+-------------------+-------+-------+------------+
| name              | a     | a     | kill_ratio |
+-------------------+-------+-------+------------+
| sniper            | 16264 | 14030 |     1.1592 |
| minigun           |  9609 |  8566 |     1.1218 |
| rifle             | 20172 | 17999 |     1.1207 |
| projectileGrenade |  4066 |  3653 |     1.1131 |
| shotgun           |  8232 |  7478 |     1.1008 |
| katana            | 18622 | 17840 |     1.0438 |
| knife             |  7391 |  7191 |     1.0278 |
| dualpistol        |  6799 |  6663 |     1.0204 |
| smg               | 10962 | 10983 |     0.9981 |
| gauntlet          |  5665 |  5724 |     0.9897 |
| arrow             |  4398 |  4540 |     0.9687 |
| rocket            |  6362 |  6724 |     0.9462 |
| shuriken          |  1049 |  1112 |     0.9433 |
| revolver          |  6207 |  6610 |     0.9390 |
| fusionRifle       |  2392 |  2595 |     0.9218 |
| dualUzi           | 12371 | 14795 |     0.8362 |
| crossbowBolt      |  1375 |  2075 |     0.6627 |
| flamethrower      |  4199 |  6527 |     0.6433 |
| riotShield        |   373 |   597 |     0.6248 |
| projectileSmoke   |   407 |   725 |     0.5614 |
| fireBurn          |   604 |  1121 |     0.5388 |
+-------------------+-------+-------+------------+
```

# kills by weapon, by game type
```sql
select weapon.name, count(*) as a from kill_logs join weapon on weapon_id = weapon.id join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 1 group by weapon_id order by a desc;
select weapon.name, count(*) as a from kill_logs join weapon on weapon_id = weapon.id join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 2 group by weapon_id order by a desc;
select weapon.name, count(*) as a from kill_logs join weapon on weapon_id = weapon.id join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 3 group by weapon_id order by a desc;
```
Arena:
```
+-------------------+-------+
| name              | a     |
+-------------------+-------+
| rifle             | 18496 |
| sniper            | 15141 |
| katana            | 14028 |
| dualUzi           | 12799 |
| smg               | 10435 |
| minigun           |  8799 |
| shotgun           |  7643 |
| dualpistol        |  6809 |
| rocket            |  6773 |
| revolver          |  6509 |
| knife             |  6455 |
| gauntlet          |  5246 |
| arrow             |  4597 |
| projectileGrenade |  4421 |
| flamethrower      |  4349 |
| fusionRifle       |  1890 |
| crossbowBolt      |  1329 |
| shuriken          |   688 |
| fireBurn          |   613 |
| projectileSmoke   |   435 |
| riotShield        |   264 |
+-------------------+-------+
```
Hub:

```
+-------------------+-------+
| name              | a     |
+-------------------+-------+
| katana            | 31680 |
| knife             |  9460 |
| rifle             |  8922 |
| sniper            |  8219 |
| gauntlet          |  5163 |
| dualUzi           |  3986 |
| smg               |  3705 |
| shuriken          |  2257 |
| shotgun           |  2134 |
| minigun           |  1812 |
| fusionRifle       |  1696 |
| flamethrower      |  1612 |
| dualpistol        |  1448 |
| arrow             |  1093 |
| rocket            |  1043 |
| revolver          |   833 |
| projectileGrenade |   765 |
| riotShield        |   634 |
| crossbowBolt      |   476 |
| fireBurn          |   234 |
| projectileSmoke   |    77 |
| grappleHook       |    21 |
| bow               |    20 |
+-------------------+-------+
```

BR:
```
+-------------------+------+
| name              | a    |
+-------------------+------+
| rifle             | 4793 |
| minigun           | 3034 |
| smg               | 2586 |
| knife             | 2029 |
| shotgun           | 2028 |
| sniper            | 1983 |
| dualUzi           | 1641 |
| dualpistol        | 1292 |
| gauntlet          | 1094 |
| fusionRifle       |  905 |
| katana            |  697 |
| flamethrower      |  657 |
| revolver          |  544 |
| arrow             |  505 |
| rocket            |  447 |
| projectileGrenade |  313 |
| crossbowBolt      |  269 |
| fireBurn          |   65 |
| riotShield        |   64 |
| shuriken          |   34 |
| projectileSmoke   |    6 |
+-------------------+------+
```

# kdr by game type, without rows of players that didn't get a kill
```sql
CREATE TEMPORARY TABLE temp_kills_by_weapon AS select weapon.name, count(*) as a from kill_logs join weapon on weapon_id = weapon.id join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 1 AND weapon_killed_id is not null group by weapon_id order by a desc; CREATE TEMPORARY TABLE temp_kills_of_weapon AS select weapon.name, count(*) as a from kill_logs join weapon on weapon_killed_id = weapon.id join game_data on kill_logs.game_id = game_data.id join maps on game_data.map = maps.id where maps.type = 1 group by weapon_killed_id order by a desc; SELECT k1.name, k1.a, k2.a, k1.a / k2.a AS kill_ratio FROM temp_kills_by_weapon k1 JOIN temp_kills_of_weapon k2 ON k1.name = k2.name ORDER BY kill_ratio DESC; DROP TEMPORARY TABLE temp_kills_by_weapon; DROP TEMPORARY TABLE temp_kills_of_weapon;
```

Arena:
```
+-------------------+-------+-------+------------+
| name              | a     | a     | kill_ratio |
+-------------------+-------+-------+------------+
| sniper            | 13467 | 11431 |     1.1781 |
| shotgun           |  6828 |  5916 |     1.1542 |
| minigun           |  7833 |  6905 |     1.1344 |
| projectileGrenade |  3805 |  3406 |     1.1171 |
| rifle             | 16376 | 14797 |     1.1067 |
| revolver          |  5756 |  5598 |     1.0282 |
| smg               |  9184 |  8957 |     1.0253 |
| dualpistol        |  5989 |  5892 |     1.0165 |
| fusionRifle       |  1677 |  1663 |     1.0084 |
| gauntlet          |  4377 |  4382 |     0.9989 |
| arrow             |  4017 |  4083 |     0.9838 |
| rocket            |  5990 |  6131 |     0.9770 |
| knife             |  5271 |  5484 |     0.9612 |
| katana            | 12241 | 12738 |     0.9610 |
| dualUzi           | 10977 | 12786 |     0.8585 |
| shuriken          |   601 |   714 |     0.8417 |
| crossbowBolt      |  1196 |  1763 |     0.6784 |
| flamethrower      |  3703 |  5751 |     0.6439 |
| fireBurn          |   540 |   920 |     0.5870 |
| riotShield        |   238 |   417 |     0.5707 |
| projectileSmoke   |   374 |   706 |     0.5297 |
+-------------------+-------+-------+------------+
```

Other game types don't make sense due to low amount of data and large amount of players without kills
