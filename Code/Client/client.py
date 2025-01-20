import mysql.connector
from mysql.connector import Error
import unittest
from unittest.mock import Mock, patch

def connect_to_database():
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
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

#done
def list_accidents_in_area(cursor, Urban_or_Rural_Area):
    try:
        query = """
        SELECT L.Accident_Index, L.Longitude, L.Latitude, L.Location_Easting_OSGR, L.Location_Northing_OSGR, L.Junction_Detail
        FROM Location L
        WHERE L.Urban_or_Rural_Area = %s
        LIMIT 100;
        """
        cursor.execute(query, (Urban_or_Rural_Area,))
        results = cursor.fetchall()

        if results:
            print("Accidents in area:", Urban_or_Rural_Area)
            for row in results:
                print(f"Accident Index: {row[0]}, Longitude: {row[1]}, Latitude: {row[2]}, Easting OSGR: {row[3]}, Northing OSGR: {row[4]}, Junction Detail: {row[5]}")
        else:
            print("No accidents found in the specified area.")

    except Exception as e:
        print(f"An error occurred: {e}")

#done
def accidents_weather_conditions(cursor):
    try:
        query = """
        SELECT C.Weather_Conditions, COUNT(*) as Accident_Count
        FROM Conditions C
        INNER JOIN Accidents A ON C.Accident_Index = A.Accident_Index
        GROUP BY C.Weather_Conditions
        ORDER BY Accident_Count DESC;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            print("Number of accidents in different weather conditions:")
            for weather_conditions, accident_count in results:
                print(f"Weather Conditions Code: {weather_conditions}, Accident Count: {accident_count}")
        else:
            print("No accidents found for the specified weather conditions.")

    except Exception as e:
        print(f"An error occurred: {e}")

#done
def accidents_speed_limits(cursor):
    try:
        query = """
        SELECT R.Speed_limit, COUNT(*) as Accident_Count 
        FROM Road R
        INNER JOIN Accidents A ON R.Accident_Index = A.Accident_Index
        GROUP BY R.Speed_limit;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("Number of accidents at different speed limits:")
        for speed_limit, accident_count in results:
            print(f"Speed Limit: {speed_limit}, Accident number: {accident_count}")

    except Exception as e:
        print(f"An error occurred: {e}")
        
#done
def pedestrian_involved_accidents(cursor):
    try:
        query = """
        SELECT A.Accident_Index, L.Pedestrian_Crossing_Human_Control, L.Pedestrian_Crossing_Physical_Facilities 
        FROM Casualties C
        JOIN Accidents A ON C.Accident_Index = A.Accident_Index
        JOIN Location L ON A.Accident_Index = L.Accident_Index
        WHERE C.Casualty_Class = 3;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("Details of pedestrian-related accidents:")
        for accident_index, human_control, physical_facilities in results:
            print(f"Accident Index: {accident_index}, Human Control: {human_control}, Physical Facilities: {physical_facilities}")

    except Exception as e:
        print(f"An error occurred: {e}")

#done
def driver_demographics(cursor):
    try:
        query = """
        SELECT D.Sex_of_Driver, D.Age_Band_of_Driver, COUNT(DISTINCT A.Accident_Index) as Number_of_Accidents 
        FROM Driver D
        JOIN Vehicles V ON D.Accident_Index = V.Accident_Index
        JOIN Accidents A ON V.Accident_Index = A.Accident_Index
        GROUP BY D.Sex_of_Driver, D.Age_Band_of_Driver
        ORDER BY COUNT(DISTINCT A.Accident_Index) DESC;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("Driver demographics in accidents (sorted by number of accidents in descending order):")
        for sex, age_band, num_accidents in results:
            print(f"Sex: {sex}, Age Band: {age_band}, Number of Accidents: {num_accidents}")

    except Exception as e:
        print(f"An error occurred: {e}")

#done
def accidents_road_conditions(cursor):
    try:
        query = """
        SELECT C.Road_Surface_Conditions, COUNT(*) as Number_of_Accidents 
        FROM Conditions C
        JOIN Accidents A ON C.Accident_Index = A.Accident_Index
        GROUP BY C.Road_Surface_Conditions
        ORDER BY COUNT(*) DESC;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("Number of accidents in relation to road surface conditions (in descending order):")
        for road_conditions, num_accidents in results:
            print(f"Road Conditions: {road_conditions}, Number of Accidents: {num_accidents}")

    except Exception as e:
        print(f"An error occurred: {e}")

#done
def accidents_light_conditions(cursor):
    try:
        query = """
        SELECT C.Light_Conditions, COUNT(*) as Accident_Count 
        FROM Conditions C
        GROUP BY C.Light_Conditions
        ORDER BY COUNT(*) DESC;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("Number of accidents by light conditions (in descending order):")
        for light_conditions, accident_count in results:
            print(f"Light Conditions: {light_conditions}, Accident Count: {accident_count}")

    except Exception as e:
        print(f"An error occurred: {e}")

#done
def accidents_at_intersections(cursor):
    try:
        query = """
        SELECT Junction_Control, COUNT(*) as Accident_Count 
        FROM Location 
        WHERE Junction_Control IN (2, 3)
        GROUP BY Junction_Control;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("Number of accidents at intersections(Stop sign and traffic light):")
        for junction_control, accident_count in results:
            control_type = "Auto Traffic Signal" if junction_control == 2 else "Stop Sign"
            print(f"{control_type}: {accident_count} accidents")

    except Exception as e:
        print(f"An error occurred: {e}")

#done
def accidents_involving_young_drivers(cursor):
    try:
        query = """
        SELECT COUNT(DISTINCT Accident_Index) as Number_of_Accidents
        FROM Driver 
        WHERE Age_Band_of_Driver IN (4, 5);
        """
        cursor.execute(query)
        result = cursor.fetchone()

        number_of_accidents = result[0] if result else 0
        print(f"Number of accidents involving young drivers (Age 16-25): {number_of_accidents}")

    except Exception as e:
        print(f"An error occurred: {e}")

#done
def accidents_by_time_of_day(cursor):
    try:
        query = """
        SELECT CASE 
                WHEN Time >= '06:00:00' AND Time < '12:00:00' THEN 'Morning'
                WHEN Time >= '12:00:00' AND Time < '18:00:00' THEN 'Afternoon'
                ELSE 'Night'
            END as Time_of_Day,
            COUNT(*) as Number_of_Accidents
        FROM Timestamp
        GROUP BY Time_of_Day;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("Number of accidents by time of day:")
        for time_of_day, num_accidents in results:
            print(f"{time_of_day}: {num_accidents} accidents")

    except Exception as e:
        print(f"An error occurred: {e}")

#done
def top_accidents_with_most_casualties(cursor):
    try:
        query = """
        SELECT 
            A.Accident_Index, 
            T.Date, 
            T.Time, 
            L.Location_Easting_OSGR, 
            L.Location_Northing_OSGR, 
            C.Weather_Conditions, 
            C.Road_Surface_Conditions,
            A.Number_of_Casualties 
        FROM 
            Accidents A
        LEFT JOIN 
            Timestamp T ON A.Accident_Index = T.Accident_Index
        LEFT JOIN 
            Location L ON A.Accident_Index = L.Accident_Index
        LEFT JOIN 
            Conditions C ON A.Accident_Index = C.Accident_Index
        ORDER BY 
            A.Number_of_Casualties DESC 
        LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("Detailed information on top 10 accidents with the most casualties:")
        for row in results:
            print(f"Accident Index: {row[0]}, Date: {row[1]}, Time: {row[2]}, Easting: {row[3]}, Northing: {row[4]}, Weather Conditions: {row[5]}, Road Conditions: {row[6]}, Number of Casualties: {row[7]}")

    except Exception as e:
        print(f"An error occurred: {e}")

#done
def get_accident_info(cursor, accident_index):
    try:
        query = """
        SELECT 
            A.Accident_Index, 
            A.Accident_Severity, 
            A.Number_of_Vehicles, 
            A.Number_of_Casualties,
            T.Date, 
            T.Time,
            L.Location_Easting_OSGR, 
            L.Location_Northing_OSGR,
            L.Junction_Control, 
            L.Pedestrian_Crossing_Human_Control,
            L.Pedestrian_Crossing_Physical_Facilities,
            C.Weather_Conditions, 
            C.Road_Surface_Conditions,
            C.Light_Conditions
        FROM 
            Accidents A
        LEFT JOIN 
            Timestamp T ON A.Accident_Index = T.Accident_Index
        LEFT JOIN 
            Location L ON A.Accident_Index = L.Accident_Index
        LEFT JOIN 
            Conditions C ON A.Accident_Index = C.Accident_Index
        WHERE 
            A.Accident_Index = %s;
        """
        cursor.execute(query, (accident_index,))
        result = cursor.fetchone()

        if result:
            print(f"Details for Accident Index {accident_index}:")
            print(f"Severity: {result[1]}, Number of Vehicles: {result[2]}, Number of Casualties: {result[3]}, Date: {result[4]}, Time: {result[5]}, Location Easting: {result[6]}, Location Northing: {result[7]}, Junction Control: {result[8]}, Pedestrian Crossing Human Control: {result[9]}, Pedestrian Crossing Physical Facilities: {result[10]}, Weather Conditions: {result[11]}, Road Surface Conditions: {result[12]}, Light Conditions: {result[13]}")
        else:
            print("No accident found with the specified index.")

    except Exception as e:
        print(f"An error occurred: {e}")

#done
def update_driver_info(cursor, connection, accident_index, vehicle_reference, new_age_of_driver, new_sex_of_driver, new_driver_home_area_type):
    try:
        query = """
        UPDATE Driver 
        SET Age_of_Driver = %s, Sex_of_Driver = %s, Driver_Home_Area_Type = %s 
        WHERE Accident_Index = %s AND Vehicle_Reference = %s;
        """
        cursor.execute(query, (new_age_of_driver, new_sex_of_driver, new_driver_home_area_type, accident_index, vehicle_reference))
        connection.commit()
        print(f"Driver information updated for Accident Index: {accident_index}, Vehicle Reference: {vehicle_reference}")

    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()

def update_accident_location(cursor, connection, accident_index, new_longitude, new_latitude):
    try:
        query = """
        UPDATE Location 
        SET Longitude = %s, Latitude = %s 
        WHERE Accident_Index = %s;
        """
        cursor.execute(query, (new_longitude, new_latitude, accident_index))
        connection.commit()
        print(f"Location updated for Accident Index: {accident_index}")

    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()

def update_vehicle_details(cursor, connection, accident_index, vehicle_reference, new_vehicle_type, new_age_of_vehicle):
    try:
        query = """
        UPDATE Vehicles 
        SET Vehicle_Type = %s, Age_of_Vehicle = %s 
        WHERE Accident_Index = %s AND Vehicle_Reference = %s;
        """
        cursor.execute(query, (new_vehicle_type, new_age_of_vehicle, accident_index, vehicle_reference))
        connection.commit()
        print(f"Vehicle details updated for Accident Index: {accident_index}, Vehicle Reference: {vehicle_reference}")

    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
      
def update_accident_severity(cursor, connection, accident_index, new_severity):
    try:
        query = """
        UPDATE Accidents 
        SET Accident_Severity = %s 
        WHERE Accident_Index = %s;
        """
        cursor.execute(query, (new_severity, accident_index))
        connection.commit()
        print(f"Accident severity updated for Accident Index: {accident_index}")

    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()

        
def update_police_attendance(cursor, connection, accident_index, new_police_attendance):
    try:
        query = """
        UPDATE Administration 
        SET Did_Police_Officer_Attend_Scene_of_Accident = %s 
        WHERE Accident_Index = %s;
        """
        cursor.execute(query, (new_police_attendance, accident_index))
        connection.commit()
        print(f"Police attendance status updated for Accident Index: {accident_index}")

    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()


class TestListAccidentsInArea(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = Mock()


    def test_list_accidents_no_results(self):
        # Test the scenario where no results are found
        self.mock_cursor.fetchall.return_value = []
        with patch('builtins.print') as mock_print:
            list_accidents_in_area(self.mock_cursor, 1)
            mock_print.assert_called_with("No accidents found in the specified area.")

    def test_list_accidents_exception(self):
        # Test the scenario where an exception is thrown
        self.mock_cursor.execute.side_effect = Exception("Database error")
        with patch('builtins.print') as mock_print:
            list_accidents_in_area(self.mock_cursor, 1)
            mock_print.assert_called_with("An error occurred: Database error")

class TestAccidentsWeatherConditions(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = Mock()
        self.weather_conditions_sample_data = [
            (1, 10), 
            (2, 5), 
        ]

    def test_accidents_weather_conditions_results(self):
        self.mock_cursor.fetchall.return_value = self.weather_conditions_sample_data
        with patch('builtins.print') as mock_print:
            accidents_weather_conditions(self.mock_cursor)
            mock_print.assert_any_call("Number of accidents in different weather conditions:")
            for weather_conditions, accident_count in self.weather_conditions_sample_data:
                mock_print.assert_any_call(f"Weather Conditions Code: {weather_conditions}, Accident Count: {accident_count}")

    def test_accidents_weather_conditions_no_results(self):
        self.mock_cursor.fetchall.return_value = []
        with patch('builtins.print') as mock_print:
            accidents_weather_conditions(self.mock_cursor)
            mock_print.assert_called_once_with("No accidents found for the specified weather conditions.")

    def test_accidents_weather_conditions_exception(self):
        self.mock_cursor.execute.side_effect = Exception("Database error")
        with patch('builtins.print') as mock_print:
            accidents_weather_conditions(self.mock_cursor)
            mock_print.assert_called_once_with("An error occurred: Database error")

class TestAccidentConditionQueries(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = Mock()
        self.road_conditions_sample_data = [
            (1, 200),
            (2, 120),
            (3, 5)
        ]
        self.light_conditions_sample_data = [
            (1, 300),
            (2, 50),
            (3, 10)
        ]

    def test_accidents_road_conditions_results(self):
        self.mock_cursor.fetchall.return_value = self.road_conditions_sample_data
        with patch('builtins.print') as mock_print:
            accidents_road_conditions(self.mock_cursor)
            mock_print.assert_any_call("Number of accidents in relation to road surface conditions (in descending order):")
            for condition, count in self.road_conditions_sample_data:
                mock_print.assert_any_call(f"Road Conditions: {condition}, Number of Accidents: {count}")

    def test_accidents_light_conditions_results(self):
        self.mock_cursor.fetchall.return_value = self.light_conditions_sample_data
        with patch('builtins.print') as mock_print:
            accidents_light_conditions(self.mock_cursor)
            mock_print.assert_any_call("Number of accidents by light conditions (in descending order):")
            for condition, count in self.light_conditions_sample_data:
                mock_print.assert_any_call(f"Light Conditions: {condition}, Accident Count: {count}")

class TestUpdateDriverInfo(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = Mock()
        self.mock_connection = Mock()
        
        self.accident_index = '200750A61G747'   
        self.vehicle_reference = 1   
        self.new_age_of_driver = 25   
        self.new_sex_of_driver = 1   
        self.new_driver_home_area_type = 1   

    def test_update_driver_info(self):
        with patch('builtins.print') as mock_print:
            update_driver_info(self.mock_cursor, self.mock_connection, self.accident_index,
                               self.vehicle_reference, self.new_age_of_driver,
                               self.new_sex_of_driver, self.new_driver_home_area_type)
            
            self.mock_cursor.execute.assert_called_once_with("""
        UPDATE Driver 
        SET Age_of_Driver = %s, Sex_of_Driver = %s, Driver_Home_Area_Type = %s 
        WHERE Accident_Index = %s AND Vehicle_Reference = %s;
        """, (self.new_age_of_driver, self.new_sex_of_driver, self.new_driver_home_area_type,
              self.accident_index, self.vehicle_reference))
            
            self.mock_connection.commit.assert_called_once()
            
            mock_print.assert_called_once_with(f"Driver information updated for Accident Index: {self.accident_index}, Vehicle Reference: {self.vehicle_reference}")

    def test_update_driver_info_exception(self):
        self.mock_cursor.execute.side_effect = Exception("Database error")
        
        with patch('builtins.print') as mock_print:
            update_driver_info(self.mock_cursor, self.mock_connection, self.accident_index,
                               self.vehicle_reference, self.new_age_of_driver,
                               self.new_sex_of_driver, self.new_driver_home_area_type)
            
            mock_print.assert_called_once_with("An error occurred: Database error")
            
            self.mock_connection.rollback.assert_called_once()

def main():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        
        while True:
            # Header for GET QUERIES
            print("+" + "-" * 77 + "+")
            print("|" + "GET QUERIES".center(77) + "|")
            print("+" + "-" * 77 + "+")

            #GET QUERIES

            get_queries =[
                "1. Number of Accidents by Road Conditions",
                "2. Number of Accidents by Light Conditions",
                "3. Number of Accidents in different Weather Conditions",
                "4. Number of Accidents at Different Speed Limits",
                "5. Number of accidents at intersections(Stop sign and traffic light)",
                "6. Number of Accidents Involving Young Drivers (Age 16-25)",
                "7. Number of accidents by time of day",
                "8. Details of Pedestrian-Related Accidents",
                "9. List All Accidents in a Specific Area (1 for Urban and 2 for Rural)",
                "10. Driver Demographics in Accidents",
                "11. Details of Top 10 Accidents with most casulties",
                "12. Details of Accident"
            ]

            for query in get_queries:
                print("| {:76} |".format(query))

# Separator
            print("+" + "-" * 77 + "+")

# Header for UPDATE QUERIES
            print("|" + "UPDATE QUERIES".center(77) + "|")
            print("+" + "-" * 77 + "+")

# List of UPDATE QUERIES
            update_queries = [
                "13. Update driver information in an accident ",
                "14. Update an existing accident's location",
                "15. Update vehicle information",
                "16. Update accident severity",
                "17. Update police attendance"
            ]

            for query in update_queries:
                print("| {:76} |".format(query))

# Footer for Exit option
            print("+" + "-" * 77 + "+")
            print("| {:76} |".format("-1. Exit"))
            print("| {:76} |".format("T. run unit test"))
            print("+" + "-" * 77 + "+")



            choice = input("Enter your choice: ")

            if choice == "1":
                accidents_road_conditions(cursor)
            elif choice == "2":
                accidents_light_conditions(cursor)
            elif choice == "3":
                accidents_weather_conditions(cursor)
            elif choice == "4":
                accidents_speed_limits(cursor)
            elif choice == "5":
                accidents_at_intersections(cursor)
            elif choice == "6":
                accidents_involving_young_drivers(cursor)
            elif choice == "7":
                accidents_by_time_of_day(cursor)
            elif choice == "8":
                pedestrian_involved_accidents(cursor)
            elif choice == "9":
                area_code = input("Enter Area Code: (1 for Urban and 2 for Rural)")
                list_accidents_in_area(cursor, area_code)
            elif choice == "10":
                driver_demographics(cursor)
            elif choice == "11":
                top_accidents_with_most_casualties(cursor)
            elif choice == "12":
                accident_index = input("Enter accident index to search accident info:")
                get_accident_info(cursor, accident_index)
            elif choice == "13":
                accident_index = input("Enter Accident Index: ")
                vehicle_reference = input("Enter Vehicle Reference: ")
                new_age_of_driver = input("Enter New Age of Driver: ")
                new_sex_of_driver = input("Enter New Sex of Driver (e.g., Male, Female): ")
                new_driver_home_area_type = input("Enter New Driver Home Area Type: ")
                update_driver_info(cursor, connection, accident_index, vehicle_reference, new_age_of_driver, new_sex_of_driver, new_driver_home_area_type)
            elif choice == "14":
                accident_index = input("Enter Accident Index: ")
                new_longitude = input("Enter New Longitude: ")
                new_latitude = input("Enter New Latitude: ")
                update_accident_location(cursor, connection, accident_index, new_longitude, new_latitude)
            elif choice == "15":
                accident_index = input("Enter Accident Index: ")
                vehicle_reference = input("Enter Vehicle Reference: ")
                new_vehicle_type = input("Enter New Vehicle Type: ")
                new_age_of_vehicle = input("Enter New Age of Vehicle: ")
                update_vehicle_details(cursor, connection, accident_index, vehicle_reference, new_vehicle_type, new_age_of_vehicle)
            elif choice == "16":
                accident_index = input("Enter Accident Index: ")
                new_severity = input("Enter New Severity Level (e.g., 1 for Fatal, 2 for Serious, 3 for Slight): ")
                update_accident_severity(cursor, connection, accident_index, new_severity)
            elif choice == "17":
                accident_index = input("Enter Accident Index: ")
                new_police_attendance = input("Enter New Police Attendance Status (1 for Yes, 2 for No ,3 for self completion form): ")
                update_police_attendance(cursor, connection, accident_index, new_police_attendance)
            elif choice == "T":
                unittest.main(argv=['first-arg-is-ignored'], exit=False)
            elif choice == "-1":
                break

        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()

