-- Clear existing database rows for testing
SET FOREIGN_KEY_CHECKS=0;
TRUNCATE TABLE result;
TRUNCATE TABLE vote_table;
TRUNCATE TABLE user_table;
TRUNCATE TABLE candidate_table;
TRUNCATE TABLE party_table;
TRUNCATE TABLE voter_table;
TRUNCATE TABLE address;
SET FOREIGN_KEY_CHECKS=1;

-- 1. Insert Address Mappings (Districts)
INSERT INTO address (DistrictId, Locality, City, State, Zip) VALUES
(234, 'Andheri', 'Mumbai', 'Maharashtra', '400059'),
(235, 'Hadapsar', 'Pune', 'Maharashtra', '411013'),
(236, 'Malviya', 'Lucknow', 'Uttar Pradesh', '226004'),
(237, 'Depalpur', 'Indore', 'Madhya Pradesh', '453115');

-- 2. Insert Voter Records
-- Format: Aadhaar, FirstName, MiddleName, LastName, Sex, Birthday, Age, Phone, Email, DistrictId
INSERT INTO voter_table (Aadhaar, FirstName, MiddleName, LastName, Sex, Birthday, Age, Phone, Email, DistrictId) VALUES
('359146283661', 'Akash', 'Kumar', 'Singh', 'M', '1984-02-16', 37, 9623412913, 'akash@example.com', 234),
('577379407366', 'Dipti', 'Sharma', 'Kumar', 'F', '1998-01-13', 23, 9222325956, 'dipti@example.com', 235),
('782034294038', 'Shlok', 'Vikram', 'Agarwal', 'M', '1988-02-04', 33, 9722768470, 'shlok@example.com', 234),
('616950285641', 'Rashid', 'Ahmed', 'Khan', 'M', '1976-10-17', 44, 9414321457, 'rashid@example.com', 235),
('736741666818', 'Nicole', 'Deepak', 'Dias', 'F', '1991-12-08', 29, 9913542379, 'nicole@example.com', 234),
('569863239187', 'Muskan', 'Harmeet', 'Gupta', 'F', '1990-07-14', 30, 9406269045, 'muskan@example.com', 235),
('111122223333', 'Rohan', 'Kumar', 'Sen', 'M', '1990-05-15', 36, 9876543210, 'rohan@example.com', 234),
('999999999999', 'DECEASED', 'VOTER', 'TEST', 'M', '1970-01-01', 56, 9000000000, 'deceased@example.com', 234);

-- 3. Insert Contesting Political Parties
-- Format: PartyName, Symbol, PartyLeader, LeaderAadhaar
INSERT INTO party_table (PartyName, Symbol, PartyLeader, LeaderAadhaar) VALUES
('BJP', 'Lotus', 'Narendra Modi', '359146283661'),
('INC', 'Hand', 'Rahul Gandhi', '577379407366'),
('AAP', 'Broom', 'Arvind Kejriwal', '736741666818');

-- 4. Insert Nominated Candidates Mapped to Districts
-- Format: Aadhaar, CandidateName, PartyId, DistrictId (Auto increments CandidateId starting at 1)
INSERT INTO candidate_table (Aadhaar, CandidateName, PartyId, DistrictId) VALUES
('782034294038', 'Shlok Agarwal', 1, 234),  -- BJP in Andheri
('616950285641', 'Rashid Khan', 2, 235),     -- INC in Hadapsar
('111122223333', 'Rohan Sen', 2, 234),       -- INC in Andheri
('569863239187', 'Muskan Gupta', 3, 235);     -- AAP in Hadapsar

-- 5. Insert Login Credentials and Status Accounts
-- Note: Passwords are plain text here, but the server supports both plain text and PBKDF2 hashes
-- Format: VoterId, Aadhaar, _Password, IsActive
INSERT INTO user_table (VoterId, Aadhaar, _Password, IsActive) VALUES
('AK1234567', '359146283661', 'password123', 1),   -- Active Citizen
('DP1234568', '577379407366', 'password456', 1),   -- Active Citizen
('RS1234569', '111122223333', 'password789', 1),   -- Active Citizen
('DE1234567', '999999999999', 'password789', 0);   -- Inactive (Lockout check)