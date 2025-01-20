drop table if exists Road;
drop table if exists Location;
drop table if exists Administration;
drop table if exists Timestamp;
drop table if exists Conditions;
drop table if exists Driver;
drop table if exists Events;
drop table if exists Vehicles;
drop table if exists Casualties;
drop table if exists Accidents;

-- CREATING MAIN TABLES

-- CREATING ACCIDENTS TABLE
select '---------------------------------------------------------------------------------------' as '';
select 'Create Accidents' as '';
create table Accidents (
  Accident_Index char(13) check(length(Accident_Index) = 13),
  Accident_Severity int,
  Number_of_Vehicles int,
  Number_of_Casualties int,
  primary key (Accident_Index)
);

-- LOADING DATA INTO THE ACCIDENTS TABLE
load data infile '/var/lib/mysql-files/07-Accidents/Accidents0515.csv'
ignore into table Accidents
fields terminated by ',' 
enclosed by '"'
lines terminated by '\n'
(Accident_Index, @skip, @skip, @skip, @skip, @skip, Accident_Severity, Number_of_Vehicles, 
Number_of_Casualties, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, 
@skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip);

  
-- CREATING CASUALTIES TABLE

select '---------------------------------------------------------------------------------------' as '';
select 'Create Casualties' as '';
create table Casualties (
  Accident_Index char(13) check(length(Accident_Index) = 13),
  Vehicle_Reference int,
  Casualty_Reference int,
  Casualty_Class int,
  Sex_of_Casualty int,
  Age_of_Casualty int,
  Age_Band_of_Casualty int,
  Casualty_Severity int,
  Pedestrian_Location int,
  Pedestrian_Movement int,
  Car_Passenger int,
  Bus_or_Coach_Passenger int,
  Pedestrian_Road_Maintenance_Worker int,
  Casualty_Type int,
  Casualty_Home_Area_Type int,
  primary key(Accident_Index, Casualty_Reference),
  foreign key(Accident_Index) references Accidents(Accident_Index)
  );

-- LOADING DATA INTO THE CASUALTIES TABLE

load data infile '/var/lib/mysql-files/07-Accidents/Casualties0515.csv'
ignore into table Casualties
fields terminated by ',' 
enclosed by '"'
lines terminated by '\n'
(Accident_Index, Vehicle_Reference, Casualty_Reference, Casualty_Class, Sex_of_Casualty, 
Age_of_Casualty, Age_Band_of_Casualty, Casualty_Severity, Pedestrian_Location, 
Pedestrian_Movement, Car_Passenger, Bus_or_Coach_Passenger,
Pedestrian_Road_Maintenance_Worker, Casualty_Type, Casualty_Home_Area_Type);

-- CREATING VEHICLES TABLE

select '---------------------------------------------------------------------------------------' as '';
select 'Create Vehicles' as '';
create table Vehicles (
  Accident_Index char(13) check(length(Accident_Index) = 13),
  Vehicle_Reference int,
  Vehicle_Type int,
  Vehicle_Location_Restricted_Lane int,
  Junction_Location int,
  Was_Vehicle_Left_Hand_Drive int,
  Engine_Capacity_CC int,
  Propulsion_Code int,
  Age_of_Vehicle int,
  primary key (Accident_Index, Vehicle_Reference),
  foreign key(Accident_Index) references Accidents(Accident_Index)  
  );

-- LOADING DATA INTO THE VEHICLES TABLE

load data infile '/var/lib/mysql-files/07-Accidents/Vehicles0515.csv'
ignore into table Vehicles
fields terminated by ',' 
enclosed by '"'
lines terminated by '\n'
(Accident_Index, Vehicle_Reference, Vehicle_Type, @skip, @skip, Vehicle_Location_Restricted_Lane, 
Junction_Location, @skip, @skip, @skip, @skip, @skip, Was_Vehicle_Left_Hand_Drive, @skip, @skip, 
@skip, @skip, Engine_Capacity_CC, Propulsion_Code, Age_of_Vehicle, @skip, @skip);

-- CREATING CONTEXT TABLES

-- CREATING ROAD TABLE

select '---------------------------------------------------------------------------------------' as '';
select 'Create Road' as '';
create table Road (
  Accident_Index char(13) check(length(Accident_Index) = 13),
  1st_Road_Class int,
  1st_Road_Number int,
  Road_Type int,
  Speed_limit int,
  2nd_Road_Class int,
  2nd_Road_Number int,
  foreign key(Accident_Index) references Accidents(Accident_Index)
  );

-- LOADING DATA INTO THE ROAD TABLE

load data infile '/var/lib/mysql-files/07-Accidents/Accidents0515.csv'
ignore into table Road
fields terminated by ',' 
enclosed by '"'
lines terminated by '\n'
(Accident_Index, @skip, @skip, @skip, @skip, @skip, @skip, @skip, 
@skip, @skip, @skip, @skip, @skip, @skip, 
1st_Road_Class, 1st_Road_Number, Road_Type, Speed_limit, 
@skip, @skip, 
2nd_Road_Class, 2nd_Road_Number, 
@skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip);

-- CREATING LOCATION TABLE

select '---------------------------------------------------------------------------------------' as '';
select 'Create Location' as '';
create table Location (
  Accident_Index char(13) check(length(Accident_Index) = 13),
  Location_Easting_OSGR int,
  Location_Northing_OSGR int,
  Longitude float(6),
  Latitude float(6),
  Junction_Detail int,
  Junction_Control int,
  Pedestrian_Crossing_Human_Control int,
  Pedestrian_Crossing_Physical_Facilities int,
  Urban_or_Rural_Area int,
  LSOA_of_Accident_Location char(9),
  foreign key(Accident_Index) references Accidents(Accident_Index)
  );

-- LOADING DATA INTO THE LOCATION TABLE

load data infile '/var/lib/mysql-files/07-Accidents/Accidents0515.csv'
ignore into table Location
fields terminated by ',' 
enclosed by '"'
lines terminated by '\n'
(Accident_Index, Location_Easting_OSGR, Location_Northing_OSGR, Longitude, Latitude, @skip, @skip, 
@skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, Junction_Detail, 
Junction_Control, @skip, @skip, Pedestrian_Crossing_Human_Control, 
Pedestrian_Crossing_Physical_Facilities, 
@skip, @skip, @skip, @skip, @skip, Urban_or_Rural_Area, @skip, LSOA_of_Accident_Location);

-- CREATING ADMINISTRATION TABLE

select '---------------------------------------------------------------------------------------' as '';
select 'Create Administration' as '';
create table Administration (
   Accident_Index char(13) check(length(Accident_Index) = 13),
   Police_Force int,
   Local_Authority_District int,
   Local_Authority_Highway char(9),
   Did_Police_Officer_Attend_Scene_of_Accident int,
   foreign key(Accident_Index) references Accidents(Accident_Index)
  );

-- LOADING DATA INTO THE ADMINISTRATION TABLE

load data infile '/var/lib/mysql-files/07-Accidents/Accidents0515.csv'
ignore into table Administration
fields terminated by ',' 
enclosed by '"'
lines terminated by '\n'
(Accident_Index, @skip, @skip, @skip, @skip, Police_Force, @skip, @skip, 
@skip, @skip, @skip, @skip, Local_Authority_District, Local_Authority_Highway, @skip, @skip, 
@skip, @skip, @skip, 
@skip, @skip, @skip, @skip, @skip, 
@skip, @skip, @skip, @skip, @skip, @skip, Did_Police_Officer_Attend_Scene_of_Accident, @skip);

-- CREATING TIMESTAMP TABLE

select '---------------------------------------------------------------------------------------' as '';
select 'Create Timestamp' as '';
create table Timestamp (
  Accident_Index char(13) check(length(Accident_Index) = 13),
  Date date,
  Day_of_Week int,
  Time Time,
  foreign key(Accident_Index) references Accidents(Accident_Index)
  );

-- LOADING DATA INTO THE TIMESTAMP TABLE

load data infile '/var/lib/mysql-files/07-Accidents/Accidents0515.csv'
ignore into table Timestamp
fields terminated by ',' 
enclosed by '"'
lines terminated by '\n'
(Accident_Index, @skip, @skip, @skip, @skip, @skip, @skip, @skip, 
@skip, Date, Day_of_Week, Time, @skip, @skip, @skip, @skip, @skip, @skip, @skip, 
@skip, @skip, @skip, @skip, @skip, 
@skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip);

-- CREATING CONDITIONS TABLE

select '---------------------------------------------------------------------------------------' as '';
select 'Create Conditions' as '';
create table Conditions (
  Accident_Index char(13) check(length(Accident_Index) = 13),
  Light_Conditions int,
  Weather_Conditions int,
  Road_Surface_Conditions int,
  Special_Conditions_at_Site int,
  Carriageway_Hazards int,
  foreign key(Accident_Index) references Accidents(Accident_Index)
  );

-- LOADING DATA INTO THE CONDITIONS TABLE

load data infile '/var/lib/mysql-files/07-Accidents/Accidents0515.csv'
ignore into table Conditions
fields terminated by ',' 
enclosed by '"'
lines terminated by '\n'
(Accident_Index, @skip, @skip, @skip, @skip, @skip, @skip, @skip, 
@skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, @skip, 
@skip, @skip, @skip, @skip, @skip, 
Light_Conditions, Weather_Conditions, Road_Surface_Conditions, Special_Conditions_at_Site, 
Carriageway_Hazards, @skip, @skip, @skip);

-- CREATING DRIVER TABLE

select '---------------------------------------------------------------------------------------' as '';
select 'Create Driver' as '';
create table Driver (
  Accident_Index char(13) check(length(Accident_Index) = 13),
  Journey_Purpose_of_Driver int,
  Sex_of_Driver int,
  Age_of_Driver int,
  Age_Band_of_Driver int,
  Driver_IMD_Decile int,
  Driver_Home_Area_Type int,
  foreign key(Accident_Index) references Vehicles(Accident_Index)
  );

-- LOADING DATA INTO THE DRIVER TABLE

load data infile '/var/lib/mysql-files/07-Accidents/Vehicles0515.csv'
ignore into table Driver
fields terminated by ',' 
enclosed by '"'
lines terminated by '\n'
(Accident_Index, @skip, @skip, @skip, @skip, @skip, @skip, 
@skip, @skip, @skip, @skip, @skip, @skip, Journey_Purpose_of_Driver, Sex_of_Driver, 
Age_of_Driver, Age_Band_of_Driver, @skip,
@skip, @skip, Driver_IMD_Decile, Driver_Home_Area_Type);

-- CREATING EVENTS TABLE

select '---------------------------------------------------------------------------------------' as '';
select 'Create Events' as '';
create table Events (
  Accident_Index char(13) check(length(Accident_Index) = 13),
  Towing_and_Articulation int,
  Vehicle_Manoeuvre int,
  Skidding_and_Overturning int,
  Hit_Object_in_Carriageway int,
  Vehicle_Leaving_Carriageway int,
  Hit_Object_off_Carriageway int,
  1st_Point_of_Impact int,
  foreign key(Accident_Index) references Vehicles(Accident_Index)
  );

-- LOADING DATA INTO THE EVENTS TABLE

load data infile '/var/lib/mysql-files/07-Accidents/Vehicles0515.csv'
ignore into table Events
fields terminated by ',' 
enclosed by '"'
lines terminated by '\n'
(Accident_Index, @skip, @skip, Towing_and_Articulation, Vehicle_Manoeuvre, @skip, @skip, 
Skidding_and_Overturning, Hit_Object_in_Carriageway, Vehicle_Leaving_Carriageway, 
Hit_Object_off_Carriageway, 1st_Point_of_Impact, @skip, 
@skip, @skip, @skip, @skip, @skip,
@skip, @skip, @skip, @skip);