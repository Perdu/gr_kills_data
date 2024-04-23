import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="gr_kills",
    password="gr_kills",
    database="gr_kills"
)

mycursor = mydb.cursor()

# Get distinct game_ids from kill_logs table
mycursor.execute("SELECT DISTINCT game_id FROM kill_logs")
games = mycursor.fetchall()

# Iterate through each game_id
for game in games:
    game_id = game[0]
    print("game_id: %s" % game_id)
    mycursor.execute(f"SELECT id, killed_hash, kill_date, weapon_killed_id FROM kill_logs WHERE game_id = {game_id}")
    game_logs = mycursor.fetchall()
    #print(len(game_logs))
    for row in game_logs:
        # print(row)
        if row[3] != None:
            # already computed
            print("continue")
            continue
        row_id = row[0]
        killed_hash = row[1]
        kill_date = row[2]
        mycursor.execute(f"SELECT weapon_id, MAX(kill_date) FROM kill_logs WHERE game_id = {game_id} AND killer_hash = '{killed_hash}' AND kill_date <= '{kill_date}'")
        weapon = mycursor.fetchone()[0]
        if weapon is None:
            mycursor.execute(f"SELECT weapon_id, MIN(kill_date) FROM kill_logs WHERE game_id = {game_id} AND killer_hash = '{killed_hash}' AND kill_date > '{kill_date}'")
            weapon = mycursor.fetchone()[0]
        print(weapon)
        if weapon is not None:
            print(f"update kill_logs set weapon_killed_id = {weapon} where id = {row_id}")
            mycursor.execute(f"update kill_logs set weapon_killed_id = {weapon} where id = {row_id}")
    mydb.commit()

mydb.close()
