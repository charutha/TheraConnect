-- DROP DATABASE theraconnect_patronus;
CREATE DATABASE IF NOT EXISTS theraconnect_patronus1;
USE theraconnect_patronus1;

CREATE TABLE IF NOT EXISTS User(
	U_id INTEGER AUTO_INCREMENT,
	Username VARCHAR(20) UNIQUE NOT NULL,
	Password VARCHAR(20) NOT NULL,
	First_name VARCHAR(20) NOT NULL,
	Last_name VARCHAR(20) NOT NULL,
	Date_Of_Birth DATE NOT NULL,
    Age INTEGER NOT NULL,
	Date_Of_Joining DATE NOT NULL,
	Phone VARCHAR(10) NOT NULL,
	Email VARCHAR(255) NOT NULL,
	Address VARCHAR(255),
	Sex ENUM("F","M","O"),
	PRIMARY KEY (U_id)
	);
-- DESC user;

CREATE TABLE IF NOT EXISTS MHP(
	M_id INTEGER AUTO_INCREMENT,
    Username VARCHAR(20) UNIQUE NOT NULL,
    Password VARCHAR(20) NOT NULL,
    First_Name VARCHAR(20) NOT NULL,
    Last_Name VARCHAR(20) NOT NULL,
    Date_Of_Birth DATE NOT NULL,
    Age INTEGER NOT NULL,
    Date_Of_Joining DATE NOT NULL,
    Phone VARCHAR(10) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    Sex ENUM("M","F","O"),
    Qualification VARCHAR(255) NOT NULL,
    Experience INTEGER NOT NULL,
    Rating INTEGER NOT NULL DEFAULT 0,
    Rate_per_hour DECIMAL(10,2) NOT NULL,
    PRIMARY KEY(M_id)
    );
-- DESC MHP; 

CREATE TABLE IF NOT EXISTS Speciality(
	M_id INTEGER NOT NULL,
    Trauma_Informed BIT(1) DEFAULT 0 NOT NULL,
    Disability_Friendly BIT(1) DEFAULT 0 NOT NULL,
    Queer_Friendly BIT(1) DEFAULT 0 NOT NULL,
    Child_Specialist BIT(1) DEFAULT 0 NOT NULL,
    FOREIGN KEY(M_id) REFERENCES MHP(M_id)
    );
-- DESC Speciality;

-- DROP Table Schedule;
CREATE TABLE IF NOT EXISTS Schedule(
	M_id INTEGER NOT NULL,
    Day VARCHAR(20) UNIQUE NOT NULL,
    Date DATE UNIQUE NOT NULL,
    9_10AM BIT(1) DEFAULT 0 NOT NULL,
	10_11AM BIT(1) DEFAULT 0 NOT NULL,
    11_12AM BIT(1) DEFAULT 0 NOT NULL,
    12_1PM BIT(1) DEFAULT 0 NOT NULL,
    1_2PM BIT(1) DEFAULT 0 NOT NULL,
    2_3PM BIT(1) DEFAULT 0 NOT NULL,
    3_4PM BIT(1) DEFAULT 0 NOT NULL,
    4_5PM BIT(1) DEFAULT 0 NOT NULL,
    FOREIGN KEY (M_id) REFERENCES MHP(M_id),
    PRIMARY KEY (M_id,Date)
	);
-- DESC Schedule;
CREATE TABLE IF NOT EXISTS Appointment(
	A_id INTEGER AUTO_INCREMENT,
    U_id INTEGER NOT NULL,
    M_id INTEGER NOT NULL,
    Date DATE NOT NULL,
    Start_time TIME NOT NULL,
    End_time TIME,
    Mode ENUM("Online","Offline"),
    Location VARCHAR(255),
    Status ENUM("Pending","Upcoming","Cancelled","Completed"),
    PRIMARY KEY(A_id),
    FOREIGN KEY(U_id) REFERENCES User(U_id),
    FOREIGN KEY(M_id) REFERENCES MHP(M_id)
    );
-- DESC Appointment;

CREATE TABLE IF NOT EXISTS Review(
	M_id INTEGER NOT NULL,
	U_id INTEGER NOT NULL,
    Date DATE NOT NULL,
    Title VARCHAR(20) NOT NULL,
    Comment VARCHAR(255) NOT NULL,
    Rating INTEGER NOT NULL,
    PRIMARY KEY (M_id,U_id),
    FOREIGN KEY (M_id) REFERENCES MHP(M_id),
    FOREIGN KEY (U_id) REFERENCES User(U_id)
    );
-- DESC Review;

CREATE TABLE IF NOT EXISTS Payment_History(
	U_id INTEGER NOT NULL,
    A_id INTEGER NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    Method_Of_Payment ENUM("CASH","PAYTM","Google Pay") NOT NULL,
    Status ENUM("Paid","Pending","Failed","Refunded","Cancelled") NOT NULL,
    PRIMARY KEY (U_id,A_id),
    FOREIGN KEY (U_id) REFERENCES User(U_id),
    FOREIGN KEY (A_id) REFERENCES Appointment(A_id)
    );
-- DESC Payment_History;
-- DROP TABLE Medicine;
CREATE TABLE IF NOT EXISTS Medicine(
    Med_Name VARCHAR(20) NOT NULL UNIQUE
	); 
-- DROP TABLE Prescription_History;
CREATE TABLE IF NOT EXISTS Prescription_History(
	A_id INTEGER NOT NULL,
	Med_Name VARCHAR(20),
    Start_Date DATE,
    End_Date DATE,
    Frequency INTEGER NOT NULL,
    Intake_Time ENUM("BF","AF","N") NOT NULL,
    Additional_Instructions VARCHAR(255),
    PRIMARY KEY (A_id,Med_Name),
    FOREIGN KEY (A_id) REFERENCES Appointment(A_id)
    );
-- DESC Prescription_History;

-- DROP PROCEDURE GetReviewsByTime;
-- procedure
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS GetReviewsByTime(IN MHP_ID INT)
BEGIN
    SELECT U.Username, R.*,
        CASE
            WHEN R.Date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH) THEN 'In the Past Month'
            WHEN R.Date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) THEN 'In the Past 6 Months'
            WHEN R.Date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) THEN 'In the Past Year'
            ELSE 'Over a Year Ago'
        END AS review_time_category
    FROM Review R
    INNER JOIN User U ON R.U_id = U.U_id
    WHERE R.M_id = MHP_ID
    ORDER BY
        CASE
            WHEN R.Date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH) THEN 1
            WHEN R.Date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) THEN 2
            WHEN R.Date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) THEN 3
            ELSE 4
        END;
END //
DELIMITER ;
SELECT * FROM Appointment;
-- SELECT * FROM Schedule;
-- trigger
DELIMITER //
CREATE TRIGGER IF NOT EXISTS insert_doctor_rating
AFTER INSERT ON review
FOR EACH ROW
BEGIN
    DECLARE doctor_id INT;
    DECLARE new_rating INT;
    SET doctor_id = NEW.M_ID;
    SELECT AVG(Rating) INTO new_rating FROM review WHERE M_ID = doctor_id;
    UPDATE mhp SET Rating = new_rating WHERE M_ID = doctor_id;
END;
//
DELIMITER ;

-- trigger
DELIMITER //
CREATE TRIGGER IF NOT EXISTS update_doctor_rating
AFTER UPDATE ON review
FOR EACH ROW
BEGIN
    DECLARE doctor_id INT;
    DECLARE new_rating INT;
    SET doctor_id = NEW.M_ID;
    SELECT AVG(Rating) INTO new_rating FROM review WHERE M_ID = doctor_id;
    UPDATE mhp SET Rating = new_rating WHERE M_ID = doctor_id;
END;
//
DELIMITER ;
-- function
DELIMITER //
CREATE FUNCTION IF NOT EXISTS CalculateTotalPrice(doctor_id INT, num_hours INT) RETURNS DECIMAL(10, 2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE rate DECIMAL(10, 2);
    DECLARE total_price DECIMAL(10, 2);
    SELECT rate_per_hour INTO rate FROM mhp WHERE M_ID = doctor_id;
    SET total_price = rate * num_hours;
    RETURN total_price;
END;
//
DELIMITER ;
-- procedure
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS  GetCustomAppointmentView(IN custom_A_id INT)
BEGIN
  SET @sql = CONCAT('CREATE OR REPLACE VIEW CustomAppointmentView AS
    SELECT U.Username, U.First_Name, U.Last_Name, U.Age, U.Phone, U.Email, U.Sex, A.Date, A.Start_time, A.End_time, A.Mode, A.Location
    FROM User U
    JOIN Appointment A ON A.U_id = U.U_id
    WHERE A.A_id = ', custom_A_id);

  PREPARE stmt FROM @sql;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END;
//
DELIMITER ;

-- CALL GetCustomAppointmentView(1);

-- SELECT * FROM CustomAppointmentView;

SELECT * FROM MHP;
