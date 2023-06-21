-- Procedures Functions, Triggers, etc. for the project
USE medical_device; 

-- 1.2 Create new/add inventory into medical device entry (CREATE) 
-- DROP PROCEDURE IF EXISTS createDevice; 
-- DELIMITER $$ 
-- CREATE PROCEDURE createDevice(IN device_id_p INT, IN device_name_p VARCHAR(64), IN length_p INT, 
-- 							IN width_p INT, IN height_p INT, life_involvement MEDIUMTEXT, 
--                             IN quantity_p INT,  IN hospital_id_p  INT) 

-- BEGIN 
-- DECLARE count_device INT; 
-- -- need to check on the existence of the medical device 
-- SELECT COUNT(*) INTO count_device
-- FROM med_device  
-- WHERE device_id= device_id_p; 

-- IF  count_device = 0 THEN -- NO deevice in tabel 
-- 	INSERT INTO med_device (device_id, device_name, lengt, width, height, life_involvement, quantity, hospital_id)
-- 	VALUES (device_id_p, device_name_p, length_p, width_p, height_p, life_involvement,
-- 			 quantity_p, hospital_id_p);
-- ELSEIF count_device > 0 THEN 
-- 	UPDATE med_device
--     SET quantity = quantity + quantity_p
--     WHERE device_id = device_id_p;
-- END IF; 
-- END$$ 
-- DELIMITER ; 

DROP PROCEDURE IF EXISTS createDevice; 
DELIMITER $$ 
CREATE PROCEDURE createDevice(IN device_id_p INT, IN device_name_p VARCHAR(64), IN length_p INT, 
							IN width_p INT, IN height_p INT, life_involvement MEDIUMTEXT, 
                            IN quantity_p INT,  IN hospital_id_p  INT) 
# number of tuples inserted not null, correct in application 

BEGIN 
DECLARE count_device INT; 
-- need to check on the existence of the medical device 
SELECT COUNT(*) INTO count_device
FROM med_device  
WHERE device_id = device_id_p; 

IF  count_device = 0 THEN -- NO deevice in tabel 
	INSERT INTO med_device (device_id, device_name, lengt, width, height, life_involvement, quantity, hospital_id)
	VALUES (device_id_p, device_name_p, length_p, width_p, height_p, life_involvement,
			 quantity_p, hospital_id_p);
ELSEIF count_device > 0 THEN 
	SIGNAL SQLSTATE '45000'
	SET MESSAGE_TEXT = 'Device already exists';
END IF; 
END$$ 
DELIMITER ; 

# creating device 
# CALL createDevice(1001, 'X-ray Machine', 120, 80, 150, 'Critical', 4, 1);



-- update device 
DROP PROCEDURE IF EXISTS updateDevice;
DELIMITER $$
CREATE PROCEDURE updateDevice(
    IN device_id_p INT,
    IN device_name_p VARCHAR(64),
    IN length_p INT,
    IN width_p INT,
    IN height_p INT,
    IN life_involvement MEDIUMTEXT,
    IN quantity_p INT,
    IN hospital_id_p INT
)
BEGIN
    DECLARE count_device INT;
    
    -- Check if the device exists
    SELECT COUNT(*) INTO count_device
    FROM med_device
    WHERE device_id = device_id_p;
    
    IF count_device = 1 THEN -- Device exists, perform update
        UPDATE med_device
        SET
            device_name = device_name_p,
            length = length_p,
            width = width_p,
            height = height_p,
            life_involvement = life_involvement,
            quantity = quantity_p,
            hospital_id = hospital_id_p
        WHERE device_id = device_id_p;
    ELSEIF count_device = 0 THEN -- Device doesn't exist
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Device does not exist';
    END IF;
END$$
DELIMITER ;


-- delete device (only have to check if device exists) 

DROP PROCEDURE IF EXISTS deleteDevice;
DELIMITER $$
CREATE PROCEDURE deleteDevice(
    IN device_id_p INT
)
BEGIN
    DECLARE count_device INT;
    
    -- Check if the device exists
    SELECT COUNT(*) INTO count_device
    FROM med_device
    WHERE device_id = device_id_p;
    
    IF count_device = 1 THEN -- Device exists, perform deletion
        DELETE FROM med_device
        WHERE device_id = device_id_p;
    ELSEIF count_device = 0 THEN -- Device doesn't exist
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Device does not exist';
    END IF;
END$$
DELIMITER ;



-- 2. Determine what room each medical device is in (READ) 
-- or am i trying to find the medical devices in each room? 
-- realized this isn't necessary just need to pull up the bridge table 

SELECT room_num, GROUP_CONCAT(device_id) as devices FROM room_med_device 
	GROUP BY room_num;

DROP PROCEDURE IF EXISTS filter_byRoom; 
DELIMITER $$ 
CREATE PROCEDURE filter_byRoom(IN room_num_p INT)
BEGIN 
	SELECT devices FROM 
	(SELECT room_num, GROUP_CONCAT(device_id) as devices FROM room_med_device 
	GROUP BY room_num) as t
    WHERE room_num = room_num_p; 
END$$ 
DELIMITER ; 

# CALL filter_byRoom(105); 


-- DROP PROCEDURE IF EXISTS filterRoom; 
-- DELIMITER $$ 
-- CREATE PROCEDURE filterRoom(IN device_id_p INT)
-- BEGIN 
-- 	DECLARE count_device INT; 
--     DECLARE device_exists INT; 
--     
--     SELECT COUNT(*) INTO count_device
--     FROM room_med_device 
--     WHERE device_id = device_id_p; 
--     
--     SELECT COUNT(*) INTO device_exists 
--     FROM med_device 
--     WHERE device_id = device_id_p; 
--     
--     IF device_exists = 0 THEN 
-- 		SIGNAL SQLSTATE '45000' 
--         SET MESSAGE_TEXT = 'Device does not exist';
-- 	END IF; 

-- 	IF count_device > 0 THEN 
-- 		SELECT * FROM room_med_device 
-- 		WHERE device_id = device_id_p; 
-- 	ELSE 
-- 		SIGNAL SQLSTATE '45000' 
--         SET MESSAGE_TEXT = 'Device is not assigned to a room ';
-- 	END IF; 
-- END$$ 
-- DELIMITER ; 

-- CALL filterRoom(1008); 


-- 3. Filter by Device Type (READ) 
-- INPUT THE DEVICE TYPE and outputs all of the device id's that are in it (lowkey shouldn't group concat and I should 
-- find the information of those devices  
-- DROP PROCEDURE IF EXISTS filterType; 
-- DELIMITER $$ 
-- CREATE PROCEDURE filterType(IN category_p VARCHAR(64))
-- BEGIN 
-- 	DECLARE count_category INT; 
-- -- need to check on the existence of the room 
-- 	SELECT COUNT(*) INTO count_category
-- 	FROM med_device 
-- 	INNER JOIN med_device_type USING (device_id) 
-- 	WHERE category = category_p; 
-- 	
-- 	IF count_category > 0 THEN 
-- 	SELECT d.* FROM med_device as d 
--     INNER JOIN med_device_type USING (device_id) 
-- 		WHERE category = category_p; 
-- 	ELSEIF count_category = 0 THEN 
-- 		SIGNAL SQLSTATE '45000'
-- 		SET MESSAGE_TEXT = 'category doesnt exist';
-- 	END IF; 
-- END$$ 
-- DELIMITER ; 

# CALL filterType('Life Preservatio'); 

-- consolidated list of all of the device_id from med_device_type for easy access for 
DROP PROCEDURE IF EXISTS filterType_grouped; 
DELIMITER $$ 
CREATE PROCEDURE filterType_grouped(IN category_p VARCHAR(64))
BEGIN 
	SELECT GROUP_CONCAT(device_id) FROM med_device_type 
	GROUP BY category
    HAVING category_p = category ; 
END$$ 
DELIMITER ; 

# CALL filterType_grouped('Life Preservation'); 

# unsure if group_concat is a single item so I'll just add it 
DROP FUNCTION IF EXISTS filterType_grouped2; 
delimiter $$ 
	CREATE FUNCTION filterType_grouped2 (category_p VARCHAR(64)) 
		RETURNS VARCHAR(64) DETERMINISTIC 
		CONTAINS SQL 
		BEGIN 
			DECLARE grp_device VARCHAR(128); 
			SELECT GROUP_CONCAT(device_id) into grp_device FROM med_device_type 
			GROUP BY category
            HAVING category_p = category; 
            RETURN(grp_device); 
		END$$
DELIMITER ; 

# SELECT filterType_grouped2('Life Preservation'); 

-- -- Is doctor 
-- DROP PROCEDURE IF EXISTS isDoctor; 
-- DELIMITER $$ 
-- CREATE PROCEDURE isDoctor(IN doctor_id_p INT, IN doc_first_name_p VARCHAR(64), IN doc_last_name_p VARCHAR(64))
-- BEGIN 
-- 	DECLARE count_doctor INT; 
-- -- need to check on the existence of the room 
-- 	SELECT COUNT(*) INTO count_doctor
-- 	FROM doctor 
-- 	WHERE doc_id = doctor_id_p and doc_first_name = doc_first_name_p and  doc_last_name = doc_last_name_p;
--     
--     IF count_doctor = 0 THEN 
-- 		SIGNAL SQLSTATE '45000'
-- 		SET MESSAGE_TEXT = 'Invalid Doctor Name or ID';
--     END IF; 
-- END$$ 
-- DELIMITER ; 

-- # CALL isDoctor(900, 'John','Doe'); 
 
-- your hospital 
DROP PROCEDURE IF EXISTS yourHospital; 
DELIMITER $$ 
CREATE PROCEDURE yourHospital(IN doctor_id_p INT)
BEGIN 
-- need to check on the existence of the room 
	SELECT hospital_id 
	FROM doctor 
	WHERE doc_id = doctor_id_p; 
END$$ 
DELIMITER ; 

# CALL yourHospital(901); 


-- -- FInd doctor information 
-- DROP PROCEDURE IF EXISTS doctorInfo; 
-- DELIMITER $$ 
-- CREATE PROCEDURE doctorInfo(IN doctor_id_p INT, IN doc_first_name_p VARCHAR(64), IN doc_last_name_p VARCHAR(64))
-- BEGIN 
-- 	DECLARE count_doctor INT; 
-- -- need to check on the existence of the room 
-- 	SELECT COUNT(*) INTO count_doctor
-- 	FROM doctor 
-- 	WHERE doc_id = doctor_id_p and doc_first_name = doc_first_name_p and  doc_last_name = doc_last_name_p;
--     
-- 	IF count_doctor > 0 THEN 
-- 		SELECT * FROM doctor
-- 		WHERE doc_id = doctor_id_p;
--     ELSEIF count_doctor = 0 THEN 
-- 		SIGNAL SQLSTATE '45000'
-- 		SET MESSAGE_TEXT = 'Invalid Doctor Name or ID';
--     END IF; 
-- END$$ 
-- DELIMITER ; 

-- # CALL doctorInfo(901, 'John','Doe'); 



-- 4. Filter by Doctor? input the name and you will receive the medical instruments that are checked out by that doctor 


-- SELECT * FROM med_device INNER JOIN 
-- examination USING(device_id); 

-- DROP PROCEDURE IF EXISTS filterDoctor; 
-- DELIMITER $$ 
-- CREATE PROCEDURE filterDoctor(IN doctor_id_p INT)
-- BEGIN 
-- 	DECLARE count_doctor INT; 
--     
--     SELECT COUNT(*) INTO count_doctor 
--     FROM med_device as d INNER JOIN 
--     examination USING(device_id) WHERE doc_id = doctor_id_p; 
--     
--     

-- 	IF count_doctor > 0 THEN 
-- 		SELECT * FROM med_device as d INNER JOIN 
-- 		examination USING(device_id)
-- 		WHERE doc_id = doctor_id_p;
-- 	ELSE 
-- 		SIGNAL SQLSTATE '45000'
-- 		SET MESSAGE_TEXT = 'No Devices Currently Used By Doctor';
-- 	END IF; 
-- END$$ 
-- DELIMITER ; 

-- CALL filterDoctor(909); 


-- not med devices but partients 


-- DROP PROCEDURE IF EXISTS filterPatient; 
-- DELIMITER $$ 
-- CREATE PROCEDURE filterPatient(IN doctor_id_p INT)
-- BEGIN 
-- 	SELECT p.* FROM patient as p 
--     WHERE doc_id = doctor_id_p; 
-- END$$ 
-- DELIMITER ; 

-- CALL filterPatient(901); 






-- 5. Move a medical device from one room to another (UPDATE) 
-- They choose the medical device and assign it to a different room

-- DROP PROCEDURE IF EXISTS availableRooms;

-- DELIMITER $$

-- CREATE PROCEDURE availableRooms (IN d_id_p INT)
-- BEGIN
--     DECLARE hosp_id INT;

--     SELECT hospital_id INTO hosp_id
--     FROM doctor
--     WHERE doc_id = d_id_p;

--     SELECT r.*
--     FROM room AS r
--     WHERE r.room_num NOT IN (
--         SELECT room_num
--         FROM patient
--         WHERE hospital_id = hosp_id
--     )
--     AND r.hospital_id = hosp_id;
-- END$$

-- DELIMITER ;

-- CREATE PROCEDURE availableMove (IN d_id_p INT)
-- BEGIN
-- SELECT * FROM room
-- WHERE room_num != old_room_p and hospital_id != old_hosp_p;


-- DROP PROCEDURE IF EXISTS moveDevice; 
-- DELIMITER $$ 
-- CREATE PROCEDURE moveDevice(IN device_id_p INT, IN old_room_p INT, IN old_hosp_p INT, IN new_room_p INT, IN new_hosp_p INT)
-- BEGIN 
-- 	DECLARE room_tmp INT; 
--     DECLARE count_dev INT; -- if old device and place exists 
--     DECLARE count_dev2 INT; -- if new place exists 
--     
--     
--     IF old_room_p = new_room_p AND old_hosp_p = new_hosp_p THEN
--         SIGNAL SQLSTATE '45000'
--         SET MESSAGE_TEXT = 'Old room and old hospital cannot be the same as new room and new hospital.';
--     END IF;
--     
--     SELECT COUNT(*) INTO count_dev2
--     FROM room
--     WHERE room_num = new_room_p and hospital_id = new_hosp_p; 
--     
--     -- old device exists 
--     SELECT COUNT(*) INTO count_dev
-- 	FROM room_med_device
-- 	WHERE device_id = device_id_p and room_num = old_room_p and hospital_id = old_hosp_p; 
--     
--     

--     IF count_dev > 0 and count_dev2 > 0 THEN  -- device exists 
-- 		UPDATE room_med_device 
--         SET room_num = new_room_p, hospital_id = new_hosp_p 
--         WHERE device_id= device_id_p and room_num = old_room_p and hospital_id = old_hosp_p;
--     ELSEIF count_dev2 = 0 THEN 
-- 		SIGNAL SQLSTATE '45000'
-- 		SET MESSAGE_TEXT = 'Invalid New room/Hosp';
--     
-- 	ELSEIF count_dev = 0 THEN 
-- 		SIGNAL SQLSTATE '45000'
--       SET MESSAGE_TEXT = 'Device does not exists or device does not fall within the old room/old hosp';
-- 	END IF; 
-- END$$ 
-- DELIMITER ; 

-- CALL moveDevice(1001, 101, 1, 101, 3); 




/* 



THIS NEEDS A PROCEDURE 
device_id_p 
device_name_p
tracking_num_p 
new_room 

first of all does it exist? IF SO THEN have to take the new_room and change it to thwat was requested 

*/ 



-- 6. Device with the most inventory?  (READ) 
DROP FUNCTION IF EXISTS mostQuantity; 
delimiter $$ 
	CREATE FUNCTION mostquantity() 
		RETURNS INT DETERMINISTIC 
		CONTAINS SQL 
		BEGIN 
			DECLARE device_id_temp INT; #local variable that will be returned 
			DECLARE device_name_temp VARCHAR(64); 
            DECLARE device_inv_temp INT; 
            DECLARE final_result VARCHAR(128); 
			
            SELECT device_id, device_name, quantity INTO device_id_temp, device_name_temp, device_inv_temp FROM med_device 
				WHERE quantity = (SELECT max(quantity) FROM med_device);
            RETURN(final_result); 
		END$$
DELIMITER ; 

SELECT mostQuantity();  

-- DROP PROCEDURE IF EXISTS mostQuantity2; 
-- delimiter $$ 
-- 	CREATE PROCEDURE mostQuantity2() 
-- 		BEGIN 
--             SELECT d.* FROM med_device as d 
-- 				ORDER BY quantity ; 
-- 		END$$
-- DELIMITER ; 

# CALL mostQuantity2();  

/*
DROP PROCEDURE IF EXISTS patientInfo; 
DELIMITER $$ 
CREATE PROCEDURE patientInfo(IN pt_id_p INT)
BEGIN 
	-- Existence of Doctor 
	DECLARE count_patient INT; 
	
	SELECT COUNT(*) INTO count_patient
	FROM patient 
	WHERE pt_id = pt_id_p; 
    
	IF count_patient > 0 THEN 
		SELECT * FROM patient
		WHERE  pt_id = pt_id_p; 
    ELSEIF count_doctor = 0 THEN 
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Invalid Patient ID';
    END IF; 
END$$ 
DELIMITER ; 
 
# CALL patientInfo(29); 
 
 
-- Patient examinations all of em 
DROP PROCEDURE IF EXISTS allExam; 
DELIMITER $$ 
CREATE PROCEDURE allExam(IN pt_id_p INT)
BEGIN 
	DECLARE count_exam INT; 
    
    SELECT COUNT(*) INTO count_exam 
    FROM examination 
    WHERE pt_id = pt_id_p; 

	IF count_exam > 0 THEN 
		SELECT e.* FROM examination as e 
		WHERE pt_id = pt_id_p; 
	ELSE 
    SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'No Patient Examinations';
	END IF; 
END$$ 
DELIMITER ; 

# CALL allExam(29); 
 */

-- 10. Deletion of examination 
/*
DROP PROCEDURE IF EXISTS ArchiveOldExaminations; 
DELIMITER $$ 
CREATE PROCEDURE ArchiveOldExaminations(IN pt_id_p INT, IN old_date_p DATE) 
BEGIN 
	DECLARE has_old_exams INT;

    -- Check if there are any examinations with dates less than old_date_p for the specified pt_id_p
    SELECT COUNT(*) INTO has_old_exams
    FROM examination
    WHERE exam_date < old_date_p AND pt_id = pt_id_p;
 

	IF has_old_exams > 0 THEN
			CREATE TABLE IF NOT EXISTS archived_examination (
            -- Define the columns of the table here
            examNo INT,
            symptom VARCHAR(128),
            pt_id INT,
            doc_id INT,
            device_id INT,
            exam_date DATE
        );

        -- Insert the old examinations into the archived_examination table
        INSERT INTO archived_examination (examNo, symptom, pt_id, doc_id, device_id, exam_date)
        SELECT examNo, symptom, pt_id, doc_id, device_id, exam_date
        FROM examination
        WHERE exam_date < old_date_p AND pt_id = pt_id_p;

        -- Delete the old examinations from the examination table
        DELETE FROM examination
        WHERE exam_date < old_date_p AND pt_id = pt_id_p;
	ELSE 
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'There are no examinations before this date';
	END IF;
END$$ 
DELIMITER ; 

CALL ArchiveOldExaminations(24, '2023-09-01');
*/


-- 9. Maybe want to do a loop similar to where you add a column to a table and then go through it and update 
-- patient id and have to delete it if it doesn't work 

SELECT p.pt_id, COUNT(e.examNo) FROM patient as p
LEFT OUTER JOIN examination as e USING(pt_id) 
GROUP By pt_id; 

/*
SELECT tid, COUNT(attack.location) FROM township
            LEFT OUTER JOIN attack ON attack.location = township.tid
			GROUP BY tid;
DROP PROCEDURE IF EXISTS initialize_num_attack; 
delimiter $$ 
CREATE PROCEDURE initialize_num_attack(IN townid INT) 
BEGIN 
	-- Alter TABLE township
	-- ADD numAttacks INT; 
UPDATE township
SET numAttacks = (SELECT num FROM (SELECT tid, COUNT(attack.location) as num FROM township
				LEFT OUTER JOIN attack ON attack.location = township.tid
					GROUP BY tid) as t WHERE t.tid = townid)
WHERE township.tid = townid; 
END$$
DELIMITER ; 
*/ 

/*
DROP PROCEDURE IF EXISTS initialize_num_exam; 
delimiter $$ 
CREATE PROCEDURE initialize_num_exam(IN patientid INT) 
BEGIN 
-- Alter TABLE patient
-- ADD numExams INT; 
UPDATE patient
SET numExams = (SELECT num FROM (SELECT p.pt_id, COUNT(e.examNo) as num FROM patient as p
LEFT OUTER JOIN examination as e USING(pt_id) 
GROUP By pt_id) as t WHERE t.pt_id = patientid) 
WHERE patient.pt_id = patientid; 
END$$
DELIMITER ; 


-- CALL initialize_num_attack(4); 

DROP PROCEDURE IF EXISTS callProcedureMultipleTimes; 
delimiter $$ 
CREATE PROCEDURE callProcedureMultipleTimes()
	BEGIN
	DECLARE n INT DEFAULT 0;
	DECLARE i INT DEFAULT 0;
	SELECT COUNT(*) FROM patient INTO n;

	SELECT MAX(pt_id)+1 INTO n FROM patient; 
	SELECT MIN(pt_id) INTO i FROM patient; 
	WHILE i<n DO 
		CALL initialize_num_exam(i); 
		SET i = i + 1;
	END WHILE;
END$$
DELIMITER ; 

CALL callProcedureMultipleTimes();  

-- Trigger if it is actually deleted 
DROP TRIGGER IF EXISTS exam_after_delete; 
DELIMITER $$ 
CREATE TRIGGER exam_after_delete
	AFTER DELETE ON examination
		FOR EACH ROW 
        BEGIN 
			DECLARE count_patient INT;
            declare num_exams_tmp int;
            select numExams into num_exams_tmp from patient where pt_id = old.pt_id;
            
            SELECT COUNT(*) INTO count_patient
			FROM patient
			WHERE pt_id = old.pt_id;
            
			IF count_patient > 0 THEN
                update patient set numExams = num_exams_tmp-1 where pt_id = old.pt_id;
			END IF; 
        END$$ 
DELIMITER ; 

# CALL DeleteOldExaminations('2005-01-01');

*/

-- check to see all rooms that are available at that designated hospital based on the doctor 

-- DROP PROCEDURE IF EXISTS availableRooms;

-- DELIMITER $$

-- CREATE PROCEDURE availableRooms (IN d_id_p INT)
-- BEGIN
--     DECLARE hosp_id INT;

--     SELECT hospital_id INTO hosp_id
--     FROM doctor
--     WHERE doc_id = d_id_p;

--     SELECT r.*
--     FROM room AS r
--     WHERE r.room_num NOT IN (
--         SELECT room_num
--         FROM patient
--         WHERE hospital_id = hosp_id
--     )
--     AND r.hospital_id = hosp_id;
-- END$$

-- DELIMITER ;

# CALL availableRooms(901); 




-- 10. Add patient (don't want to delete) 
-- default for the checkout time is null 
-- DROP PROCEDURE IF EXISTS createPatient; 
-- DELIMITER $$ 
-- CREATE PROCEDURE createPatient(IN pt_first_name_p VARCHAR(100) , 
-- 								IN pt_last_name_p VARCHAR(100), 
--                                 IN pt_check_in_p DATETIME, 
--                                 IN room_num_p INT, 
--                                 IN d_id_p INT) 
-- -- if this exists pt_id exists 
-- -- return an error 



-- BEGIN 
-- DECLARE pt_id_temp INT; 
-- DECLARE count_pt INT; 
-- DECLARE hosp_id int;
-- DECLARE count_room int; 



-- SELECT pt_id INTO pt_id_temp 
-- FROM patient 
-- WHERE pt_first_name = pt_first_name_p and pt_last_name = pt_last_name_p; 

-- SELECT COUNT(*) INTO count_pt
-- FROM patient 
-- WHERE pt_id = pt_id_temp and room_num = room_num_p; 

-- IF count_pt > 0 THEN 
-- SIGNAL SQLSTATE '45000'
--       SET MESSAGE_TEXT = 'Patient already exists';
-- END IF; 

-- SELECT hospital_id into hosp_id
-- FROM doctor 
-- WHERE doc_id = d_id_p; 

-- SELECT COUNT(*) into count_room 
-- FROM patient 
-- WHERE room_num = room_num_p and hospital_id = hosp_id; 

-- IF count_room > 0 THEN -- this table is already assigned to a patient in that hospital 
-- SIGNAL SQLSTATE '45000'
--       SET MESSAGE_TEXT = 'Room already assigned to different patient';
-- END IF; 
--          
-- INSERT INTO patient(pt_first_name, pt_last_name, check_in, doc_id, room_num, hospital_id) VALUES
-- (pt_first_name_p, pt_last_name_p, pt_check_in_p, d_id_p, room_num_p, hosp_id); 
-- end$$
-- DELIMITER ;

-- CALL createPatient("Ac", "Ventura", '2023-06-15 14:30:00', 101, 901); 



-- 11. procedure where you're able to to add the time (check out procedure) 

-- DROP PROCEDURE IF EXISTS enterCheckOut; 
-- DELIMITER $$ 
-- CREATE PROCEDURE enterCheckOut(IN pt_id_p INT, IN check_out_p DATETIME)
-- BEGIN 
--     DECLARE count_pt INT; 
--     DECLARE checkout_time DATETIME;
--     
--     SELECT COUNT(*) INTO count_pt
--     FROM patient
--     WHERE pt_id = pt_id_p; 
--     
--     IF count_pt > 0 THEN 
--         SELECT check_out INTO checkout_time
--         FROM patient
--         WHERE pt_id = pt_id_p; 
--         
--         IF checkout_time IS NULL THEN
--             UPDATE patient
--             SET check_out = check_out_p
--             WHERE pt_id = pt_id_p;
--         ELSE
--             SIGNAL SQLSTATE '45000'
--             SET MESSAGE_TEXT = 'Check-out time already exists for the patient.';
--         END IF;
-- 	ELSE 
-- 		SIGNAL SQLSTATE '45000'
--             SET MESSAGE_TEXT = 'patient does not exist.';
--     END IF; 
-- END$$  
-- DELIMITER ;

-- CALL enterCheckOut(19,  '2023-06-20 14:30:00');

-- DROP PROCEDURE IF EXISTS enterCheckOut; 
-- DELIMITER $$ 
-- CREATE PROCEDURE enterCheckOut(IN pt_id_p INT, IN check_out_p DATETIME)
-- BEGIN 
--     DECLARE count_pt INT; 
--     
--     -- checks to see if that patient exists 
--     SELECT COUNT(*) INTO count_pt
-- 	FROM patient
-- 	WHERE pt_id_p = pt_id; 
--     
--     IF count_pt > 0 THEN 
-- 		UPDATE 
--         patient SET check_out = check_out_p
--         WHERE pt_id = pt_id_p; 
-- 	END IF; 
-- END$$  
-- DELIMITER ; 

# CALL enterCheckOut(20,  '2023-06-20 14:30:00');

-- 12. Trigger that asks for more information on that hospital 

-- Proc
-- DROP PROCEDURE IF EXISTS removePatient; 
-- DELIMITER //
-- CREATE PROCEDURE removePatient(IN pt_id_p INT)
-- BEGIN
-- 	DECLARE count_pt INT; 
--     
--     SELECT COUNT(*) INTO count_pt
-- 	FROM patient
-- 	WHERE pt_id_p = pt_id; 
--     
--     
--     
--     IF count_pt = 1 THEN -- Device exists, perform deletion
-- 	    DELETE FROM patient
-- 		WHERE pt_id = pt_id_p;
-- 	ELSEIF count_pt = 0 THEN -- Device doesn't exist
--         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Patient does not exist';
-- 	END IF; 
-- END //
-- DELIMITER ;

-- CALL removePatient(24); 



-- -- 12. Filter By Hospital 
-- DROP PROCEDURE IF EXISTS filterHospital; 
-- DELIMITER $$ 
-- CREATE PROCEDURE filterHospital(IN hospital_id_p INT)
-- BEGIN 	
-- 	DECLARE count_device INT; 
--     
--     SELECT COUNT(*) INTO count_device
--     FROM med_device 
--     WHERE hospital_id = hospital_id_p; 

-- 	IF count_device > 0 THEN 
-- 	SELECT * FROM med_device 
--     WHERE hospital_id = hospital_id_p; 
--     ELSE
-- 		SIGNAL SQLSTATE '45000'
-- 		SET MESSAGE_TEXT = 'No devices exist that selected hospital';
-- 	END IF; 
-- END$$ 
-- DELIMITER ; 

-- CALL filterHospital(1); 

# CALL filterHospital(13); 

-- Proc
DROP PROCEDURE IF EXISTS addRoom; 
DELIMITER $$ 
CREATE PROCEDURE addRoom(IN num INT, IN hospID INT)
BEGIN
	DECLARE count_room INT; 
-- need to check on the existence of the room 
	SELECT COUNT(*) INTO count_room
	FROM room 
	WHERE room_num = num and hospital_id = hospID ; 

	IF  count_room = 0 THEN -- NO room in tabel 
		INSERT INTO room (room_num, hospital_id)
		VALUES (num, hospID);
	ELSEIF count_room > 0 THEN 
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Device already exists';
	END IF; 
END$$ 
DELIMITER ; 

# CALL addRoom(107,1); 



-- Proc
DROP PROCEDURE IF EXISTS removeRoom; 
DELIMITER $$
CREATE PROCEDURE removeRoom(IN num INT,  IN hospID INT)
BEGIN
	DECLARE count_room INT;
    
    -- Check if the device exists
    SELECT COUNT(*) INTO count_room
	FROM room 
	WHERE room_num = num and hospital_id = hospID ; 
    
    IF count_room = 1 THEN -- Device exists, perform deletion
		DELETE FROM room
		WHERE room_num = num and hospital_id = hospID ;
    ELSEIF count_room = 0 THEN -- Device doesn't exist
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Device does not exist';
	END IF; 
END$$ 
DELIMITER ; 

# CALL removeRoom(107,1); 


-- Proc
DROP PROCEDURE IF EXISTS removeHospital; 
DELIMITER //
CREATE PROCEDURE removeHospital(IN id INT)
BEGIN
	DECLARE count_hosp INT; 
-- need to check on the existence of the room 
	SELECT COUNT(*) INTO count_hosp
	FROM hospital 
	WHERE hospital_id = id; 
    
    IF count_hosp = 1 THEN -- Device exists, perform deletion
		DELETE FROM hospital
		WHERE hospital_id = id;
	ELSEIF count_hosp  = 0 THEN -- Device doesn't exist
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Device does not exist';
	END IF; 
END //

DELIMITER ;

# CALL removeHospital(12); 

-- Proc
DROP PROCEDURE IF EXISTS addHosp; 
DELIMITER //
CREATE PROCEDURE addHosp(IN id INT, IN name VARCHAR(64), streetNum INT, streetName VARCHAR(64), t VARCHAR(64),s VARCHAR(64), z CHAR(5))
BEGIN
DECLARE count_hosp INT; 
-- need to check on the existence of the room 
	SELECT COUNT(*) INTO count_hosp
	FROM hospital 
	WHERE hospital_id = id; 

	IF  count_hosp = 0 THEN -- NO room in tabel 
		INSERT INTO hospital(hospital_id, hospital_name, street_number, street_name, town, state, zipcode)
		VALUES (id, name, streetNum, streetName, t, s, z);
	ELSEIF count_hosp > 0 THEN 
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Hospital already exists';
	END IF; 
END //
DELIMITER ;

# CALL addHosp(12, 'New Hospital', '1112', 'street', 'town', 'ma', '11355'); 


-- Proc
/*
DROP PROCEDURE IF EXISTS addExam; 
DELIMITER //
CREATE PROCEDURE addExam(symp VARCHAR(128), patientID INT, deviceID INT, IN exam_date_p DATE)
BEGIN
	DECLARE checkInDate DATETIME;
    DECLARE checkOutDate DATETIME;
    DECLARE patientDoctorID INT;
    DECLARE count_device INT; 
    
    SELECT COUNT(*) into count_device
    FROM med_device
    WHERE device_id = deviceID; 
    
    IF count_device = 0 THEN 
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid medical device entered';
	END IF; 
    
    -- Get check-in and check-out dates for the patient
    SELECT check_in, check_out, doc_id INTO checkInDate, checkOutDate, patientDoctorID
    FROM patient
    WHERE pt_id = patientID;
    
    IF (exam_date_p >= checkInDate AND exam_date_p <= checkOutDate) OR (exam_date_p >= checkInDate ) THEN
        -- Check if the doctor matches the patient's assigned doctor
            -- Insert examination record
		INSERT INTO examination(symptom, pt_id, doc_id, device_id, exam_date)
		VALUES (symp, patientID, patientDoctorID, deviceID, exam_date_p);
    ELSE
        -- Signal an error if exam_date_p is not within the patient's check-in and check-out dates
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid exam date. Please make sure the exam date is within the patient\'s check-in and check-out dates.';
    END IF;

END //

DELIMITER ;

CALL addExam('symptom', 11, 1008, '2023-06-01 00:00:00'); 

*/


-- DROP PROCEDURE IF EXISTS hasExam; 
-- DELIMITER $$ 
-- CREATE PROCEDURE hasExam(IN pt_id_p INT)
-- BEGIN 
-- 	DECLARE count_exam INT; 
--     
--     SELECT COUNT(*) INTO count_exam 
--     FROM examination 
--     WHERE pt_id = pt_id_p; 

-- 	IF count_exam = 0 THEN 
--     SIGNAL SQLSTATE '45000'
-- 		SET MESSAGE_TEXT = 'No Patient Examinations';
-- 	END IF; 
-- END$$ 
-- DELIMITER ; 
