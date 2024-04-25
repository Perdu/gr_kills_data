import sys
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="gr_kills",
    password="gr_kills",
    database="gr_kills"
)

cursor = conn.cursor()

if len(sys.argv) < 2:
    print("Usage: python querys.py (1|n)")
    sys.exit(1)

if sys.argv[1] == "1":
    cursor.execute("""
    CREATE TEMPORARY TABLE temp_nb_deaths AS 
    SELECT killed_hash, COUNT(*) AS nb_deaths 
    FROM kill_logs 
    WHERE killed_hash NOT IN (SELECT DISTINCT killer_hash FROM kill_logs) 
    GROUP BY killed_hash;
    """)

    cursor.execute("""
    SELECT nb_deaths, COUNT(*) AS frequency
    FROM temp_nb_deaths
    GROUP BY nb_deaths;
    """)

    result = cursor.fetchall()

    df = pd.DataFrame(result, columns=['nb_deaths', 'frequency'])

    plt.bar(df['nb_deaths'], df['frequency'])
    plt.xlabel('Number of Deaths')
    plt.ylabel('Frequency')
    plt.xlim(0,100) # remove extreme values
    plt.title('Distribution of Number of Deaths')

elif sys.argv[1] == "2":
    cursor.execute("""
    CREATE TEMPORARY TABLE temp_duration_deaths AS select distinct killed_hash, TIMESTAMPDIFF(SECOND, MIN(kill_date), MAX(kill_date)) as duration from kill_logs where killed_hash not in (select unique killer_hash from kill_logs) group by killed_hash;
    """)

    cursor.execute("""
    SELECT duration, COUNT(*) AS frequency from temp_duration_deaths where duration > 0
    GROUP BY duration;
    """)

    result = cursor.fetchall()

    df = pd.DataFrame(result, columns=['duration', 'frequency'])

    plt.hist(df['duration'], bins=10, edgecolor='black')
    plt.xlabel('Time before last and first recorded death (s)')
    plt.ylabel('Frequency')
    plt.title('Distribution of average time players stay')


elif sys.argv[1] == "3":
    cursor.execute("""
    CREATE TEMPORARY TABLE temp_duration_deaths AS select distinct killed_hash, TIMESTAMPDIFF(SECOND, MIN(kill_date), MAX(kill_date)) as duration from kill_logs where killed_hash not in (select unique killer_hash from kill_logs) group by killed_hash;
    """)

    cursor.execute("""
    SELECT duration, COUNT(*) AS frequency from temp_duration_deaths where duration > 0 and duration < 10800
    GROUP BY duration;
    """)

    result = cursor.fetchall()

    df = pd.DataFrame(result, columns=['duration', 'frequency'])

    plt.hist(df['duration'], bins=10, edgecolor='black')
    plt.xlabel('Time before last and first recorded death (s)')
    plt.ylabel('Frequency')
    plt.title('Distribution of average time players stay (when staying less than 3h)')


plt.show()

cursor.close()
conn.close()
