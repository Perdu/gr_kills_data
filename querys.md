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
select name, count(*) as a from kill_logs join weapon on weapon_killed_id = weapon.id group by weapon_killed_id order by a desc;
```

# Nb games:
```sql
select count(distinct game_id) from kill_logs;
```

# Fill kill_logs_full (too long):
```sql
INSERT INTO kill_logs_full (id, killer_hash, killed_hash, game_id, weapon_id, kill_date, weapon_killed_id) select id, killer_hash, killed_hash as a, game_id, weapon_id, kill_date b, (SELECT weapon_id from kill_logs where killer_hash = a and kill_date = (SELECT MAX(kill_date) from kill_logs where killer_hash = a and kill_date < b) limit 1) from kill_logs;
```

# Nb row of killed players who don't have a kill:
```sql
select count(*) from kill_logs where killed_hash not in (select unique killer_hash from kill_logs);
```

# Nb of killed players who don't have a kill:
```sql
select count(distinct killed_hash) from kill_logs where killed_hash not in (select unique killer_hash from kill_logs);
/
select count(distinct killed_hash) from kill_logs;
```

# kdr (ordering works but doesn't take null fields into account):
```sql
CREATE TEMPORARY TABLE temp_kills_by_weapon AS select name, count(*) as a from kill_logs join weapon on weapon_id = weapon.id group by weapon_id order by a desc;
CREATE TEMPORARY TABLE temp_kills_of_weapon AS select name, count(*) as a from kill_logs join weapon on weapon_killed_id = weapon.id group by weapon_killed_id order by a desc;
SELECT k1.name, k1.a, k2.a, k1.a / k2.a AS kill_ratio FROM temp_kills_by_weapon k1 JOIN temp_kills_of_weapon k2 ON k1.name = k2.name ORDER BY kill_ratio DESC;
DROP TEMPORARY TABLE temp_kills_by_weapon;
DROP TEMPORARY TABLE temp_kills_of_weapon;
```

# kdr, without rows of players that didn't get a kill
```sql
CREATE TEMPORARY TABLE temp_kills_by_weapon AS select name, count(*) as a from kill_logs join weapon on weapon_id = weapon.id where weapon_killed_id is not null group by weapon_id order by a desc; CREATE TEMPORARY TABLE temp_kills_of_weapon AS select name, count(*) as a from kill_logs join weapon on weapon_killed_id = weapon.id group by weapon_killed_id order by a desc; SELECT k1.name, k1.a, k2.a, k1.a / k2.a AS kill_ratio FROM temp_kills_by_weapon k1 JOIN temp_kills_of_weapon k2 ON k1.name = k2.name ORDER BY kill_ratio DESC; DROP TEMPORARY TABLE temp_kills_by_weapon; DROP TEMPORARY TABLE temp_kills_of_weapon;
```
