DROP SCHEMA IF EXISTS medical_device; 
CREATE DATABASE IF NOT EXISTS medical_device;
USE medical_device; 

DROP TABLE IF EXISTS hospital; 
CREATE table hospital (
hospital_id INT NOT NULL AUTO_INCREMENT, 
hospital_name VARCHAR(64) NOT NULL, 
street_number INT,
street_name VARCHAR(64),
town VARCHAR(64),
state VARCHAR(64), 
zipcode CHAR(5), #char because its limited to 5 characters 
PRIMARY KEY(hospital_id), 
UNIQUE(street_number, street_name, town, state, zipcode)
);  

INSERT INTO hospital (hospital_id, hospital_name, street_number, street_name, town, state, zipcode)
VALUES
    (1, 'St. Mary\'s Hospital', 123, 'Main Street', 'Townville', 'Stateville', '12345'),
    (2, 'General Hospital', 456, 'Oak Avenue', 'Cityville', 'Stateland', '23456'),
    (3, 'Memorial Hospital', 789, 'Elm Road', 'Villageville', 'Statetown', '34567'),
    (4, 'City Medical Center', 321, 'Cedar Lane', 'Hamletville', 'Statecity', '45678'),
    (5, 'Community Hospital', 654, 'Pine Street', 'Townville', 'Stateville', '12345'),
    (6, 'Metropolitan Hospital', 987, 'Birch Avenue', 'Cityville', 'Stateland', '23456'),
    (7, 'Rural Health Center', 210, 'Maple Road', 'Villageville', 'Statetown', '34567'),
    (8, 'County Medical Center', 543, 'Spruce Lane', 'Hamletville', 'Statecity', '45678'),
    (9, 'University Hospital', 876, 'Willow Street', 'Townville', 'Stateville', '12345'),
    (10, 'Mercy Hospital', 109, 'Aspen Avenue', 'Cityville', 'Stateland', '23456');


DROP TABLE IF EXISTS doctor; 
CREATE table doctor ( 
doc_id INT PRIMARY KEY, 
doc_first_name VARCHAR(64), 
doc_last_name VARCHAR(64), 
specialization VARCHAR(64), 
hospital_id INT, 
foreign key (hospital_id) REFERENCES hospital(hospital_id) 
    ON UPDATE CASCADE ON DELETE RESTRICT 
);

INSERT INTO doctor (doc_id, doc_first_name, doc_last_name, specialization, hospital_id)
VALUES
  (901, 'John', 'Doe', 'Cardiology', 1),
  (902, 'Jane', 'Smith', 'Orthopedics', 2),
  (903, 'Michael', 'Johnson', 'Neurology', 3),
  (904, 'Emily', 'Williams', 'Pediatrics', 4),
  (905, 'David', 'Brown', 'Dermatology', 5),
  (906, 'Sarah', 'Taylor', 'Ophthalmology', 6),
  (907, 'Robert', 'Anderson', 'Gastroenterology', 7),
  (908, 'Jennifer', 'Clark', 'Obstetrics and Gynecology', 8),
  (909, 'William', 'Thomas', 'Urology', 9),
  (910, 'Jessica', 'Lee', 'Psychiatry', 10);


DROP TABLE IF EXISTS  patient ;
CREATE TABLE  patient (
	 pt_id int NOT NULL,
     pt_first_name  varchar(100) NOT NULL,
     pt_last_name  varchar(100) NOT NULL,
     check_in  DATETIME NOT NULL,
     check_out  DATETIME DEFAULT NULL ,
    PRIMARY KEY ( pt_id ), 
    hospital_id INT, 
    foreign key (hospital_id) REFERENCES hospital(hospital_id) 
    ON UPDATE CASCADE ON DELETE RESTRICT 
    
); 

INSERT INTO patient (pt_id, pt_first_name, pt_last_name, check_in, check_out, hospital_id)
VALUES
  (11, 'John', 'Doe', '2023-06-01', '2023-06-02', 1),
  (12, 'Jane', 'Smith', '2023-06-02', '2023-06-03', 2),
  (13, 'Michael', 'Johnson', '2023-06-03', '2023-06-05', 3),
  (14, 'Emily', 'Williams', '2023-06-04', '2023-06-06', 4),
  (15, 'David', 'Brown', '2023-06-05', '2023-06-07', 5),
  (16, 'Sarah', 'Taylor', '2023-06-06', '2023-06-07', 6),
  (17, 'Robert', 'Anderson', '2023-06-06', '2023-06-08', 7),
  (18, 'Jennifer', 'Clark', '2023-06-07', '2023-06-08', 8),
  (19, 'William', 'Thomas', '2023-06-08', '2023-06-08', 9); 

/*
DROP TABLE IF EXISTS  bill ;
CREATE TABLE  bill (
	 invoice_id  int NOT NULL,
     charge_upkeep  int NOT NULL,
     charge_machine  int NOT NULL,
     est_charge  int NOT NULL,
     invoice_date  DATETIME NOT NULL,
     pt_id int, 
    PRIMARY KEY ( invoice_id ), 
    foreign key (pt_id) REFERENCES patient(pt_id) 
    ON UPDATE CASCADE ON DELETE RESTRICT 
); 
*/

DROP TABLE IF EXISTS med_device; 
CREATE table med_device ( 
device_id INT PRIMARY KEY, 
device_name VARCHAR(64),
lengt INT, 
width INT, 
height INT, 
life_involvement MEDIUMTEXT, 
quantity INT, 
hospital_id INT, 
    foreign key (hospital_id) REFERENCES hospital(hospital_id) 
    ON UPDATE CASCADE ON DELETE RESTRICT 
);
INSERT INTO med_device (device_id, device_name, lengt, width, height, life_involvement, quantity, hospital_id) VALUES 
	(1001, 'X-ray Machine', 120, 80, 150, 'Critical', 4, 1),
    (1002, 'MRI Scanner', 180, 120, 200, 'Critical', 5, 1),
    (1003, 'Ultrasound Machine', 100, 60, 120, 'Routine', 3, 2),
    (1004, 'Defibrillator', 50, 40, 80, 'Critical', 5, 3),
    (1005, 'Pulse Oximeter', 20, 10, 15, 'Routine', 10, 4), 
    (1006, "Ventilator", 10, 10, 10,  "Crucial to keeping the patients alive", 50, 1),
	(1007, "IV Pull", 5, 7, 20, "Crucial to keeping the patients alive", 60, 2);



DROP TABLE IF EXISTS room;
CREATE TABLE room(
	room_num  int NOT NULL,
    hospital_id INT, 
    PRIMARY KEY ( room_num, hospital_id), 
    foreign key (hospital_id) REFERENCES hospital(hospital_id) 
    ON UPDATE CASCADE ON DELETE RESTRICT 
);
INSERT IGNORE INTO room (room_num, hospital_id)
VALUES
    (100, 1),
    (101, 1),
    (102, 1),
    (103, 2),
    (104, 1),
    (105, 3),
    (106, 1),
    (201, 2),
    (202, 1),
    (203, 4),
    (204, 5),
    (205, 1),
    (206, 1),
    (301, 2),
    (302, 3),
    (303, 3),
    (304, 3),
    (305, 1),
    (306, 1);
    
DROP TABLE IF EXISTS device_type; 
CREATE table device_type(
category VARCHAR(64) PRIMARY KEY 
);
INSERT INTO device_type VALUES ('Surgical'),('Life Preservation'), ('Probing'), ('Monitoring'), ('Drug Delivering');


DROP TABLE IF EXISTS examination; 
CREATE TABLE examination ( 
examNo INT PRIMARY KEY, 
symptom MEDIUMTEXT, 
pt_id INT, 
doc_id INT, 
device_id INT, 
exam_date DATE, 
foreign key (pt_id) REFERENCES patient(pt_id) 
	ON UPDATE CASCADE ON DELETE RESTRICT, 
foreign key (doc_id) REFERENCES doctor(doc_id) 
	ON UPDATE CASCADE ON DELETE RESTRICT, 
foreign key (device_id) REFERENCES med_device(device_id) 
	ON UPDATE CASCADE ON DELETE RESTRICT
); 

INSERT INTO examination (examNo, symptom, pt_id, doc_id, device_id, exam_date)
VALUES
    (1000001, 'Fever and cough', 11, 901, 1001, '2015-06-10'),
    (1000002, 'Joint pain', 12, 902, 1004, '2017-09-22'),
    (1000003, 'Headache and dizziness', 13, 903, 1002, '2018-03-03'),
    (1000004, 'Difficulty in breathing', 14, 904, 1006, '2004-11-17'),
    (1000005, 'Skin rash', 15, 905, 1005, '2013-08-02'),
    (1000006, 'Eye redness and irritation', 16, 906, 1003, '2009-12-05'),
    (1000007, 'Abdominal pain and bloating', 17, 907, 1007, '2002-07-21'),
    (1000008, 'Pregnancy check-up', 18, 908, 1001, '2016-05-09'),
    (1000009, 'Urinary tract infection', 19, 909, 1007, '2011-02-14'),
    (1000010, 'Depression and anxiety', 11, 910, 1005, '2019-10-30');





-- Bridge Tables 
DROP TABLE IF EXISTS med_device_type;
CREATE TABLE  med_device_type  (
	device_id INT, 
    category VARCHAR(64), 
    PRIMARY KEY (device_id, category), 
    foreign key (device_id) REFERENCES med_device(device_id) 
    ON UPDATE CASCADE ON DELETE RESTRICT, 
    foreign key (category) REFERENCES device_type(category) 
    ON UPDATE CASCADE ON DELETE RESTRICT 
); 
INSERT INTO med_device_type (device_id, category)
VALUES
    (1001, 'Surgical'),
    (1002, 'Monitoring'),
    (1003, 'Probing'),
    (1004, 'Life Preservation'),
    (1005, 'Drug Delivering'),
    (1006, 'Life Preservation');



DROP TABLE IF EXISTS examination_med_device; 
CREATE TABLE examination_med_device ( 
examNo INT, 
device_id INT, 
PRIMARY KEY(examNo, device_id), 
foreign key (examNo) REFERENCES examination(examNo) 
	ON UPDATE CASCADE ON DELETE CASCADE, 
foreign key (device_id) REFERENCES med_device(device_id) 
	ON UPDATE CASCADE ON DELETE CASCADE 
); 
INSERT INTO examination_med_device (examNo, device_id)
VALUES
    (1000001, 1001),
    (1000002, 1004),
    (1000003, 1002),
    (1000004, 1006),
    (1000005, 1005),
    (1000006, 1003),
    (1000007, 1007),
    (1000008, 1001),
    (1000009, 1007),
    (1000010, 1005);


/*
DROP TABLE IF EXISTS examination_med_device; 
CREATE TABLE examination_med_device ( 
examNo INT, 
device_id INT, 
PRIMARY KEY(examNo, device_id), 
foreign key (examNo) REFERENCES examination(examNo) 
	ON UPDATE CASCADE ON DELETE RESTRICT, 
foreign key (device_id) REFERENCES med_device(device_id) 
	ON UPDATE CASCADE ON DELETE RESTRICT
); 
INSERT INTO examination_med_device (examNo, device_id)
VALUES
    (1000001, 1001),
    (1000002, 1004),
    (1000003, 1002),
    (1000004, 1006),
    (1000005, 1005),
    (1000006, 1003),
    (1000007, 1007),
    (1000008, 1001),
    (1000009, 1007),
    (1000010, 1005);
*/

    
DROP TABLE IF EXISTS room_med_device;
CREATE TABLE room_med_device (
    device_id INT,
    room_num INT,
    hospital_id INT,
    PRIMARY KEY (room_num, device_id, hospital_id),
    FOREIGN KEY (device_id) REFERENCES med_device(device_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (room_num, hospital_id) REFERENCES room(room_num, hospital_id) ON UPDATE CASCADE ON DELETE RESTRICT
);
INSERT INTO room_med_device (device_id, room_num, hospital_id)
VALUES
    (1001, 101, 1),
    (1002, 102, 1),
    (1003, 103, 2),
    (1004, 104, 1),
    (1005, 105, 3),
    (1006, 106, 1),
    (1007, 105, 3);


# find all the medical device types (filter kind of ) 
# filter by room, etc. 
# add a medical device to the table 
# move a medical devie from one room to another 
# which room has the most medical devices compared to another one 

DROP TABLE IF EXISTS room_patient; 
CREATE TABLE room_patient(
    room_num  int, 
    pt_id INT, 
	PRIMARY KEY(room_num, pt_id), 
	foreign key (pt_id) REFERENCES patient(pt_id) 
		ON UPDATE CASCADE ON DELETE RESTRICT, 
	foreign key (room_num) REFERENCES room(room_num ) 
		ON UPDATE CASCADE ON DELETE RESTRICT
); 
