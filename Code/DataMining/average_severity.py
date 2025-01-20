import pandas as pd
import mysql.connector
from mysql.connector import Error
import time

# ====================== Data Aggregation from Database ======================

start_time = time.time()
username = ' '
password = ' '
try:
    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=" ",
        database=" "
    )
    if connection.is_connected():
        print("Successfully connected to the database")
except Error as e:
    print(f"Error connecting to database: {e}")
    exit()

cursor = connection.cursor()

query = """
SELECT
    Accidents.Accident_Severity,
    (SELECT Time FROM Timestamp WHERE Accidents.Accident_Index = Timestamp.Accident_Index LIMIT 1) as Time,
    (SELECT Road_Type FROM Road WHERE Accidents.Accident_Index = Road.Accident_Index LIMIT 1) as Road_Type,
    (SELECT Speed_limit FROM Road WHERE Accidents.Accident_Index = Road.Accident_Index LIMIT 1) as Speed_limit,
    (SELECT Junction_Control FROM Location WHERE Accidents.Accident_Index = Location.Accident_Index LIMIT 1) as Junction_Control,
    (SELECT Light_Conditions FROM Conditions WHERE Accidents.Accident_Index = Conditions.Accident_Index LIMIT 1) as Light_Conditions,
    (SELECT Weather_Conditions FROM Conditions WHERE Accidents.Accident_Index = Conditions.Accident_Index LIMIT 1) as Weather_Conditions,
    (SELECT Road_Surface_Conditions FROM Conditions WHERE Accidents.Accident_Index = Conditions.Accident_Index LIMIT 1) as Road_Surface_Conditions,
    (SELECT Vehicle_Type FROM Vehicles WHERE Accidents.Accident_Index = Vehicles.Accident_Index LIMIT 1) as Vehicle_Type,
    (SELECT Age_of_Vehicle FROM Vehicles WHERE Accidents.Accident_Index = Vehicles.Accident_Index LIMIT 1) as Age_of_Vehicle,
    (SELECT Vehicle_Manoeuvre FROM Events WHERE Accidents.Accident_Index = Events.Accident_Index LIMIT 1) as Vehicle_Manoeuvre,
    (SELECT Journey_Purpose_of_Driver FROM Driver WHERE Accidents.Accident_Index = Driver.Accident_Index LIMIT 1) as Journey_Purpose_of_Driver,
    (SELECT Age_Band_of_Driver FROM Driver WHERE Accidents.Accident_Index = Driver.Accident_Index LIMIT 1) as Age_Band_of_Driver
FROM 
    Accidents
"""

cursor.execute(query)
column_names = cursor.column_names
rows = cursor.fetchall()

cursor.close()
connection.close()

print(f"Number of entries retrieved: {len(rows)}\n")

data = pd.DataFrame(rows, columns=column_names)

# Preprocess Age_of_Vehicle into 5 groups
# -1. Unknown
# 1. New: Less than or equal to 3 years
# 2. Fairly New: More than 3 years and up to 7 years
# 3. Old: More than 7 years and up to 15 years
# 4. Very Old: More than 15 years
data['Age_of_Vehicle'] = pd.cut(data['Age_of_Vehicle'],
                               bins=[-float('inf'), -1, 3, 7, 15, float('inf')],
                               labels=[-1, 1, 2, 3, 4])

# Preprocess Time into 5 groups
# 1. Early Morning: 0 to 5 hours
# 2. Morning: 5 to 12 hours
# 3. Afternoon: 12 to 17 hours
# 4. Evening: 17 to 21 hours
# 5. Night: 21 to 24 hours
data['Time'] = data['Time'].dt.components.hours
data['Time'] = pd.cut(data['Time'],
                     bins=[0, 5, 12, 17, 21, 24],
                     labels=[1, 2, 3, 4, 5],
                     include_lowest=True)

# Bin speed limits 20, 15, 10, and 0 together at a value of 20
data['Speed_limit'] = data['Speed_limit'].replace([20, 15, 10, 0], 20)

weights = {1: 10, 2: 3, 3: 1}

data['Weighted_Severity'] = data['Accident_Severity'].map(weights)

attributes = ['Age_Band_of_Driver', 'Age_of_Vehicle', 'Vehicle_Manoeuvre', 'Speed_limit']

for attribute in attributes:
    grouped = data.groupby(attribute)['Weighted_Severity']
    avg_severity = grouped.mean().sort_values(ascending=False)
    count = grouped.count()
    print(f"\nAverage severities of {attribute}:")
    print("{:<6} {:<10} {:<10}".format('Key', 'Severity', 'Count'))
    for index in avg_severity.index:
        print("{:<6} {:<10.2f} {:<10}".format(index, avg_severity[index], count[index]))