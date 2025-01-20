import time
import numpy as np
import pandas as pd
import mysql.connector
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from mysql.connector import Error


# ====================== Data Aggregation from Database ======================

start_time = time.time();
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
        with open('output.txt', 'w') as f:
            f.write("Successfully connected to the database\n")
except Error as e:
    with open('output.txt', 'w') as f:
        f.write(f"Error connecting to database: {e}\n")
    exit()

cursor = connection.cursor()

# This SQL query selects attributes related to accidents from different tables in the database.
# For each accident in the Accidents table, it selects the FIRST entry of each attribute to avoid bias.
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

with open('output.txt', 'a') as f:
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    f.write(f"Number of entries retrieved: {len(rows)}\n")
    f.write(f"Retrieving data took {minutes} minute(s) and {seconds} second(s)\n")

# ====================== Data Training And Testing ======================

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

predictor_attributes = ['Time', 'Road_Type', 'Junction_Control', 'Speed_limit',
                        'Light_Conditions', 'Weather_Conditions', 'Road_Surface_Conditions',
                        'Vehicle_Type', 'Vehicle_Manoeuvre', 'Journey_Purpose_of_Driver',
                        'Age_Band_of_Driver', 'Age_of_Vehicle']

target_attribute = 'Accident_Severity'
data = data.dropna(subset=predictor_attributes + [target_attribute])

# DecisionTreeClassifier's attributes are ordinal by default
# So I am binning each foreign key with LabelEncoder
label_encoder = LabelEncoder()
for attribute in predictor_attributes:
    data[attribute] = label_encoder.fit_transform(data[attribute])

# Perform random over sampling
# Before:
# - Severity Level: 3,  Percentage: 85.11343872163751%,  Count: 1515575
# - Severity Level: 2,  Percentage: 13.59501261615823%,  Count: 242080
# - Severity Level: 1,  Percentage: 1.2915486622042587%, Count: 22998
# After:
# - Severity Level: 3,  Percentage: 33.33%,              Count: 1515575
# - Severity Level: 2,  Percentage: 33.33%,              Count: 1515575
# - Severity Level: 1,  Percentage: 33.33%,              Count: 1515575
ros = RandomOverSampler(random_state=123) # The random_state for reproducibility.
x, y = ros.fit_resample(data[predictor_attributes], data[target_attribute])

# Train the model
start_time = time.time()
clf = DecisionTreeClassifier()
clf.fit(x, y)

# Perform cross-validation
cvs = cross_val_score(clf, x, y, cv=10) # 10-fold cross-validation
end_time = time.time()
    
with open('output.txt', 'a') as f:
    # Validation scores
    f.write("\nAverage accuracy from cross validation:\n" + str(np.mean(cvs)) + "\n\n")
    f.write("Cross validation scores of each model: \n")
    for score in cvs:
        f.write(str(score) + "\n")

    # Most important predictors
    importances = clf.feature_importances_
    feature_importances = pd.DataFrame({"attribute": predictor_attributes, "importance": importances})
    feature_importances = feature_importances.sort_values("importance", ascending=False)
    f.write("\nAttribute importances:\n")
    f.write(feature_importances.to_string(index=False))

    # Time to run
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    f.write(f"\n\nTraining, testing, and validation took {minutes} minute(s) and {seconds} second(s)\n")