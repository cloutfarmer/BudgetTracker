use BudgetTracker;

-- drop table spendinglimit;
-- drop table savinggoalpercat;
drop table savinggoal;
drop table income;
drop table expense;
drop table userinfo;

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

-- show tables in BudgetTracker;
-- INSERT INTO userinfo (username, hashed_password, email, role) VALUES ('johndoe', 'hashedpassword', 'john@example.com', 'user');
ALTER TABLE userinfo MODIFY email VARCHAR(255) NOT NULL DEFAULT 'default@example.com';
-- ALTER TABLE userinfo MODIFY email VARCHAR(255) NULL;

show columns from userinfo;
show columns from expense;
show columns from income;
show columns from savinggoal;
-- show columns from savinggoalpercat;
-- show columns from spendinglimit;


