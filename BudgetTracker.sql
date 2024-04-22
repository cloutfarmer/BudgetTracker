DROP DATABASE BudgetTracker;
CREATE DATABASE BudgetTracker;
use BudgetTracker;

-- drop table spendinglimit;
-- drop table savinggoalpercat;
-- drop table income;
-- drop table expense;
--  drop table userinfo;

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
    savinggoalpercatId INT AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE spendinglimit (
    spendinglimitId INT AUTO_INCREMENT PRIMARY KEY
);

-- Insert data into userinfo
INSERT INTO userinfo (username, hashed_password, email, role) VALUES 
('johndoe', 'hashedpass1', 'johndoe@example.com', 'user'),
('janedoe', 'hashedpass2', 'janedoe@example.com', 'analyst'),
('adminuser', 'hashedpass3', 'admin@example.com', 'admin'),
('bobbuilder', 'hashedpass4', 'bob@example.com', 'businessOwner');

-- Insert data into expense
INSERT INTO expense (user_id, amount, category, dateOfTransaction, description) VALUES 
(1, 120.50, 'Groceries', '2023-10-01', 'Weekly groceries shopping'),
(1, 50.00, 'Transportation', '2023-10-05', 'Gasoline top-up'),
(1, 45.00, 'Utilities', '2023-08-07', 'Electricity bill'),
(1, 78.50, 'Entertainment', '2023-08-08', 'Movie tickets and snacks'),
(1, 120.00, 'Entertainment', '2023-07-12', 'Winter clothing purchase'),
(1, 60.00, 'Healthcare', '2023-07-15', 'Monthly prescription meds'),
(1, 250.00, 'Entertainment', '2023-07-18', 'New headphones'),
(1, 300.00, 'Travel', '2023-04-22', 'Weekend getaway booking'),
(1, 120.50, 'Groceries', '2023-04-01', 'Weekly groceries shopping'),
(1, 50.00, 'Transportation', '2023-04-05', 'Gasoline top-up'),
(1, 45.00, 'Utilities', '2023-04-07', 'Electricity bill'),
(1, 78.50, 'Entertainment', '2023-02-08', 'Movie tickets and snacks'),
(1, 120.00, 'Entertainment', '2023-02-12', 'Winter clothing purchase'),
(1, 60.00, 'Healthcare', '2023-02-15', 'Monthly prescription meds'),
(1, 250.00, 'Entertainment', '2023-01-18', 'New headphones'),
(1, 300.00, 'Travel', '2023-01-22', 'Weekend getaway booking'),
(2, 200.00, 'Work', '2023-10-03', 'Printer ink and paper purchase'),
(2, 300.00, 'Travel', '2023-10-10', 'Flight booking for business trip'),
(3, 150.00, 'Work', '2023-10-02', 'Software license renewal'),
(4, 1000.00, 'Work', '2023-10-06', 'Materials for new project'),
(4, 250.00, 'Maintenance', '2023-10-08', 'Office building maintenance');

-- Insert data into income
INSERT INTO income (user_id, TotalAmountOfIncome, source, dateOfIncome, description) VALUES 
(1, 1500.00, 'Salary', '2023-10-15', 'Monthly salary payment received'),
(1, 200.00, 'Freelancing', '2023-10-05', 'Freelance graphic design work'),
(1, 150.00, 'Interest', '2023-10-10', 'Bank account interest'),
(1, 1200.00, 'Bonus', '2023-10-25', 'Annual performance bonus'),
(2, 2500.00, 'Consulting', '2023-10-18', 'Consulting fees from client'),
(3, 3000.00, 'Product Sales', '2023-10-07', 'Software product sales revenue'),
(4, 12000.00, 'Project Delivery', '2023-10-20', 'Payment received for completed construction project');

-- Insert data into savinggoal
INSERT INTO savinggoal (user_id, goalAmount, current_amount, deadline, description) VALUES 
(1, 5000.00, 1500.00, '2024-12-31', 'Goal to save for a new car'),
(2, 10000.00, 3000.00, '2024-12-31', 'Goal to renovate home'),
(3, 8000.00, 2000.00, '2025-01-15', 'Investment in new software development'),
(4, 15000.00, 5000.00, '2024-11-30', 'Setting aside funds for next construction project');

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


