CREATE TABLE registration.registrationInfo (
    ID INT AUTO_INCREMENT PRIMARY KEY,         -- Unique identifier for each record
    FullName VARCHAR(100) NOT NULL,            -- Full name of the user
    Email VARCHAR(100) UNIQUE NOT NULL,        -- Email address (must be unique)
    PhoneNumber VARCHAR(15) NOT NULL,          -- Phone number of the user
    DateOfBirth DATE NOT NULL,                 -- Date of Birth
    Gender ENUM('Male', 'Female', 'Other'),    -- Gender of the user
    Location VARCHAR(40) NOT NULL,             -- Address of the user
    RegistrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Date of registration
);
