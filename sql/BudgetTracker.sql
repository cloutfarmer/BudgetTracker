-- BudgetTracker.sql

DROP DATABASE BudgetTracker;
CREATE DATABASE BudgetTracker;
use BudgetTracker;

CREATE TABLE userinfo (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
	hashed_password VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
    role ENUM('admin', 'analyst', 'user', 'businessOwner') NOT NULL
);

CREATE TABLE expense (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100) NOT NULL,
	dateOfTransaction DATE NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES userinfo(user_id)
);

CREATE TABLE income (
    IncomeId INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    TotalAmountOfIncome DECIMAL(10, 2) NOT NULL,
    source VARCHAR(100) NOT NULL,
    dateOfIncome DATE NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES userinfo(user_id)
);

CREATE TABLE savinggoal (
    savingGoalId INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    goalAmount DECIMAL(10, 2) NOT NULL,
    current_amount DECIMAL(10, 2) NOT NULL,
    deadline DATE NOT NULL,
	description TEXT,
    FOREIGN KEY (user_id) REFERENCES userinfo(user_id)
);

CREATE TABLE savinggoalpercat (
    savinggoalpercatId INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category VARCHAR(100) NOT NULL,
    savingAmount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES userinfo(user_id)
);

CREATE TABLE spendinglimit (
    spendinglimitId INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    limitAmount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES userinfo(user_id)
);

CREATE TABLE budget (
    budgetId INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    budgetDate DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES userinfo(user_id)
);

-- Insert data into userinfo
INSERT INTO userinfo (user_id, username, hashed_password, email, role) VALUES 
(1, 'johndoe', 'hashedpass1', 'johndoe@example.com', 'user'),
(2, 'janedoe', 'hashedpass2', 'janedoe@example.com', 'admin'),
(3, 'admin', 'hashedpass3', 'admin@example.com', 'analyst'),
(4, 'bob', 'hashedpass4', 'bob@example.com', 'businessOwner'),
(5, 'cedric', 'hashedpass5', 'cedric@example.com', 'user'),
(6, 'mohammed', 'hashedpass6', 'mohammed@example.com', 'admin'),
(7, 'joe', 'hashedpass7', 'joe@example.com', 'analyst'),
(8, 'maria', 'hashedpass8', 'maria@example.com', 'businessOwner'),
(9, 'alex', 'hashedpass9', 'alex@example.com', 'user'),
(10, 'tyler', 'hashedpass10', 'tyler@example.com', 'admin');

-- Insert data into expense
INSERT INTO expense (user_id, amount, category, dateOfTransaction, description) VALUES 
(1, 120.50, 'Home', '2023-10-01', 'Weekly groceries shopping'),
(1, 50.00, 'Work', '2023-10-05', 'Gasoline top-up'),
(1, 45.00, 'Home', '2023-08-07', 'Electricity bill'),
(1, 78.50, 'Fun', '2023-08-08', 'Movie tickets and snacks'),
(1, 120.00, 'Fun', '2023-07-12', 'Winter clothing purchase'),
(1, 60.00, 'Health', '2023-07-15', 'Monthly prescription meds'),
(1, 250.00, 'Fun', '2023-07-18', 'New headphones'),
(1, 300.00, 'Travel', '2023-04-22', 'Weekend getaway booking'),
(2, 276.00, 'Sam', '2024-01-03', 'Printer ink and paper purchase'),
(2, 303.00, 'Ryan', '2023-10-10', 'Flight booking for business trip'),
(2, 1034.00, 'Hannah', '2022-04-06', 'Materials for new project'),
(2, 250.00, 'Kyle', '2023-02-19', 'Office building maintenance'),
(2, 203.00, 'Sam', '2023-12-24', 'Printer ink and paper purchase'),
(2, 300.00, 'Ryan', '2022-11-10', 'Flight booking for business trip'),
(2, 1320.00, 'Hannah', '2023-03-06', 'Materials for new project'),
(2, 2565.00, 'Kyle', '2023-08-08', 'Office building maintenance'),
(3, 154.00, 'Melanie', '2021-04-02', 'Software license renewal'),
(3, 178.00, 'Stephanie', '2022-06-13', 'Software license renewal'),
(3, 23.00, 'Ryan', '2023-09-22', 'Software license renewal'),
(3, 1320.00, 'Tony', '2024-10-09', 'Software license renewal'),
(3, 11.00, 'Peter', '2022-12-11', 'Software license renewal'),
(3, 94.00, 'Marianne', '2023-09-16', 'Software license renewal'),
(3, 340.00, 'Jess', '2023-03-23', 'Software license renewal'),
(3, 870.00, 'Frank', '2024-01-30', 'Software license renewal'),
(4, 1050.00, 'Supplies', '2023-02-06', 'Materials for new project'),
(4, 250.00, 'Supplies', '2023-11-24', 'Office building maintenance'),
(4, 122.50, 'Food', '2022-12-01', 'Weekly groceries shopping'),
(4, 50.00, 'Work', '2023-04-05', 'Gasoline top-up'),
(4, 45.00, 'Home', '2023-12-07', 'Electricity bill'),
(4, 78.50, 'Supplies', '2023-06-08', 'Movie tickets and snacks'),
(4, 190.00, 'Payment', '2023-07-12', 'Winter clothing purchase'),
(4, 60.00, 'Health', '2023-08-15', 'Monthly prescription meds'),
(4, 250.00, 'Payment', '2023-09-18', 'New headphones'),
(4, 3060.00, 'Travel', '2023-10-22', 'Weekend getaway booking'),
(5, 503.00, 'Health', '2024-02-20', 'Dental checkup and cleaning'),
(5, 12.50, 'Home', '2023-12-01', 'Weekly groceries shopping'),
(5, 345.00, 'Car', '2023-10-05', 'Gasoline top-up'),
(5, 45.00, 'Home', '2023-08-07', 'Electricity bill'),
(5, 32.50, 'Fun', '2023-08-08', 'Movie tickets and snacks'),
(5, 120.00, 'Clothing', '2023-07-12', 'Winter clothing purchase'),
(5, 60.00, 'Health', '2023-07-15', 'Monthly prescription meds'),
(5, 250.00, 'Supplies', '2023-07-18', 'New headphones'),
(5, 1780.00, 'Travel', '2023-04-22', 'Weekend getaway booking'),
(6, 276.00, 'Alex', '2024-01-03', 'Printer ink and paper purchase'),
(6, 303.00, 'Noah', '2023-10-10', 'Flight booking for business trip'),
(6, 1034.00, 'Claire', '2022-04-06', 'Materials for new project'),
(6, 250.00, 'Alex', '2023-02-19', 'Office building maintenance'),
(6, 203.00, 'Noah', '2023-12-24', 'Printer ink and paper purchase'),
(6, 300.00, 'Alex', '2022-11-10', 'Flight booking for business trip'),
(6, 1320.00, 'Claire', '2023-03-06', 'Materials for new project'),
(6, 2565.00, 'Noah', '2023-08-08', 'Office building maintenance'),
(7, 154.00, 'Steph', '2021-04-02', 'Software license renewal'),
(7, 132.00, 'Steph', '2022-06-13', 'Software license renewal'),
(7, 2234.00, 'Tony', '2023-09-22', 'Software license renewal'),
(7, 136.00, 'Tony', '2024-10-09', 'Software license renewal'),
(7, 11.00, 'Tony', '2022-12-11', 'Software license renewal'),
(7, 94.00, 'Marianne', '2023-09-16', 'Software license renewal'),
(7, 322.00, 'Steph', '2023-03-23', 'Software license renewal'),
(7, 95.00, 'Steph', '2024-01-30', 'Software license renewal'),
(8, 150.00, 'Payment', '2023-02-06', 'Materials for new project'),
(8, 250.23, 'Payment', '2023-11-24', 'Office building maintenance'),
(8, 12.50, 'Food', '2022-12-01', 'Weekly groceries shopping'),
(8, 52.00, 'Transportation', '2023-04-05', 'Gasoline top-up'),
(8, 45.00, 'Employee', '2023-12-07', 'Electricity bill'),
(8, 78.50, 'Payment', '2023-06-08', 'Movie tickets and snacks'),
(8, 19.00, 'Payment', '2023-07-12', 'Winter clothing purchase'),
(8, 621.00, 'Health', '2023-08-15', 'Monthly prescription meds'),
(8, 2420.00, 'Payment', '2023-09-18', 'New headphones'),
(8, 300.00, 'Transportation', '2023-10-22', 'Weekend getaway booking'),
(9, 120.50, 'Home', '2023-10-01', 'Weekly groceries shopping'),
(9, 50.00, 'Work', '2023-10-05', 'Gasoline top-up'),
(9, 45.00, 'Home', '2023-08-07', 'Electricity bill'),
(9, 78.50, 'Fun', '2023-08-08', 'Movie tickets and snacks'),
(9, 120.00, 'Fun', '2023-07-12', 'Winter clothing purchase'),
(9, 60.00, 'Health', '2023-07-15', 'Monthly prescription meds'),
(9, 250.00, 'Fun', '2023-07-18', 'New headphones'),
(9, 300.00, 'Travel', '2023-04-22', 'Weekend getaway booking'),
(10, 154.00, 'CEO', '2021-04-02', 'Software license renewal'),
(10, 178.00, 'Manager', '2022-06-13', 'Software license renewal'),
(10, 23.00, 'Intern', '2023-09-22', 'Software license renewal'),
(10, 1320.00, 'Inter', '2024-10-09', 'Software license renewal'),
(10, 11.00, 'Intern', '2022-12-11', 'Software license renewal'),
(10, 94.00, 'Manager', '2023-09-16', 'Software license renewal'),
(10, 340.00, 'CEO', '2023-03-23', 'Software license renewal'),
(10, 870.00, 'CEO', '2024-01-30', 'Software license renewal');

-- Insert data into income
INSERT INTO income (user_id, TotalAmountOfIncome, source, dateOfIncome, description) VALUES 
(1, 1500.00, 'Salary', '2023-10-15', 'Monthly salary payment received'),
(1, 200.00, 'Freelancing', '2023-10-05', 'Freelance graphic design work'),
(1, 150.00, 'Interest', '2023-10-10', 'Bank account interest'),
(1, 1200.00, 'Bonus', '2023-10-25', 'Annual performance bonus'),
(2, 2500.00, 'Consulting', '2023-10-18', 'Consulting fees from client'),
(3, 3000.00, 'Product Sales', '2023-10-07', 'Software product sales revenue'),
(4, 12000.00, 'Project Delivery', '2023-10-20', 'Payment received for completed construction project'),
(5, 3500.00, 'Royalties', '2023-02-25', 'Book royalties received'),
(6, 1500.00, 'Salary', '2023-10-15', 'Monthly salary payment received'),
(6, 20009.00, 'Freelancing', '2023-10-05', 'Freelance graphic design work'),
(7, 8580.00, 'Interest', '2023-10-10', 'Bank account interest'),
(8, 1200.00, 'Bonus', '2023-10-25', 'Annual performance bonus'),
(8, 2500.00, 'Consulting', '2023-10-18', 'Consulting fees from client'),
(8, 3000.00, 'Product Sales', '2023-10-07', 'Software product sales revenue'),
(9, 12000.00, 'Project Delivery', '2023-10-20', 'Payment received for completed construction project'),
(10, 3590.00, 'Royalties', '2023-02-25', 'Book royalties received');

-- Insert data into savinggoal
INSERT INTO savinggoal (user_id, goalAmount, current_amount, deadline, description) VALUES 
(1, 5000.00, 1500.00, '2024-12-31', 'Goal to save for a new car'),
(2, 10000.00, 3000.00, '2024-12-31', 'Goal to renovate home'),
(3, 8000.00, 2000.00, '2025-01-15', 'Investment in new software development'),
(4, 15000.00, 5000.00, '2024-11-30', 'Setting aside funds for next construction project'),
(5, 28000.00, 500.00, '2024-03-01', 'Saving for a luxury vacation'),
(1, 2180.00, 1500.00, '2024-12-31', 'Goal to save for a new car'),
(2, 12000.00, 3000.00, '2024-12-31', 'Goal to renovate home'),
(3, 8400.00, 2000.00, '2025-01-15', 'Investment in new software development'),
(4, 13000.00, 5000.00, '2024-11-30', 'Setting aside funds for next construction project'),
(5, 2500.00, 500.00, '2024-03-01', 'Saving for a luxury vacation');

-- show tables in BudgetTracker;
-- INSERT INTO userinfo (username, hashed_password, email, role) VALUES ('johndoe', 'hashedpassword', 'john@example.com', 'user');
ALTER TABLE userinfo MODIFY email VARCHAR(255) NOT NULL DEFAULT 'default@example.com';
-- ALTER TABLE userinfo MODIFY email VARCHAR(255) NULL;

-- show columns from userinfo;
-- show columns from expense;
-- show columns from income;
-- show columns from savinggoal;
-- show columns from savinggoalpercat;
-- show columns from spendinglimit;
