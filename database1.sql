-- Create the database
CREATE DATABASE IF NOT EXISTS StudentManagement;
USE StudentManagement;

-- Create table for storing student information
CREATE TABLE IF NOT EXISTS Students (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,
    IDNumber VARCHAR(20) NOT NULL UNIQUE,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    YearLevel VARCHAR(20) NOT NULL,
    Age INT NOT NULL,
    Email VARCHAR(100) NOT NULL,
    SHS VARCHAR(100) NOT NULL,
    Address VARCHAR(200) NOT NULL,
    StudentType ENUM('Regular', 'Irregular') NOT NULL
);

-- Create table for storing subjects
CREATE TABLE IF NOT EXISTS Subjects (
    SubjectID INT AUTO_INCREMENT PRIMARY KEY,
    SubjectCode VARCHAR(10) NOT NULL UNIQUE,
    SubjectName VARCHAR(100) NOT NULL,
    YearLevel DECIMAL(3,1) NOT NULL,
    Units INT NOT NULL,
    LecHours INT NOT NULL,
    LabHours INT NOT NULL,
    Prerequisite VARCHAR(100)
);

-- Create table for storing grades
CREATE TABLE IF NOT EXISTS Grades (
    GradeID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT,
    Student_Name VARCHAR(100),
    Year_Level INT,
    Course_No VARCHAR(20),
    Grade FLOAT,
    Semester VARCHAR(20),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (Course_No) REFERENCES Subjects(Course_No)
);

-- Insert sample data into Students table
INSERT INTO Students (IDNumber, FirstName, LastName, YearLevel, Age, Email, SHS, Address, StudentType) VALUES
('2021-322138', 'Tricia', 'Alvarez', '3RD YEAR', 22, 'alvarez.tricia@student.capsu.edu.ph', 'Ivisan National High School', 'Basiao Ivisan Capiz', 'Regular'),
('2021-322156', 'Lander', 'Arroyo', '3RD YEAR', 22, 'arroyo.lander@student.capsu.edu.ph', 'Capiz National High School', 'Dinginan Roxas city capiz', 'Regular'),
('2021-322145', 'Pedro', 'Arostique', '3RD YEAR', 20, 'arostique.pedro@student.capsu.edu.ph', 'Capiz National High School', 'brgy.Vll roxas city capiz', 'Regular'),
('2021-322148', 'Tine', 'Balgos', '3RD YEAR', 21, 'balgos.tine@student.cpasu.edu.ph', 'Roxas City School For Philippines Craftsmen', 'San Jose roxas city capiz', 'Regular'),
('2021-322130', 'Marian', 'Buenafe', '3RD YEAR', 23, 'buenafe.maria@student.capsu.edu.ph', 'Filamer Christian University', 'Sitio Canary punta tabuc roxas city capiz', 'Regular');

-- Insert curriculum data into Subjects table
INSERT INTO Subjects (SubjectCode, SubjectName, YearLevel, Units, LecHours, LabHours, Prerequisite) VALUES
('GE101', 'Understanding the Self/Pag-unawa sa Sarili', 1.1, 3, 3, 0, NULL),
('GE102', 'The Contemporary World/Ang kasalukuyang Daigdig', 1.1, 3, 3, 0, NULL),
('GE103', 'Art Appreciation/Pagpapahalaga sa Sining', 1.1, 3, 3, 0, NULL),
('GE104', 'Mathematics in the Modern World/Matematika sa Makabagong Mundo', 1.1, 3, 3, 0, NULL),
('CS101', 'Introduction to Computing', 1.1, 3, 2, 3, NULL);

-- Transform and insert grades data
-- This part assumes that the data has been transformed into a suitable format for SQL insertion

-- Example transformed data insertion for Grades table
INSERT INTO Grades (StudentID, Course_No, Grade, Semester) VALUES
((SELECT StudentID FROM Students WHERE IDNumber = '2021-322138'), (SELECT Course_No FROM Subjects WHERE SubjectCode = 'GE101'), '1.50', 'Fall 2023'),
((SELECT StudentID FROM Students WHERE IDNumber = '2021-322138'), (SELECT Course_No FROM Subjects WHERE SubjectCode = 'GE102'), '1.50', 'Fall 2023'),
((SELECT StudentID FROM Students WHERE IDNumber = '2021-322156'), (SELECT Course_No FROM Subjects WHERE SubjectCode = 'GE101'), '2.00', 'Fall 2023'),
((SELECT StudentID FROM Students WHERE IDNumber = '2021-322156'), (SELECT Course_No FROM Subjects WHERE SubjectCode = 'GE102'), '2.00', 'Fall 2023');

-- Continue inserting transformed data for all students and subjects...

-- Query to retrieve data for verification
SELECT s.FirstName, s.LastName, s.StudentType, sub.SubjectName, g.Grade, g.Semester
FROM Students s
JOIN Grades g ON s.StudentID = g.StudentID
JOIN Subjects sub ON g.Course_No = sub.Course_No;
