SET FOREIGN_KEY_CHECKS=0;

-- Create address table
CREATE TABLE IF NOT EXISTS address(
  DistrictId integer NOT NULL,
  Locality VARCHAR(30) NOT NULL,
  City VARCHAR(30) NOT NULL,
  State VARCHAR(30) NOT NULL, 
  Zip VARCHAR(10) NOT NULL,
  PRIMARY KEY (DistrictId));

-- Create voter_table (without FK constraint initially)
CREATE TABLE IF NOT EXISTS voter_table(
  Aadhaar char(15) NOT NULL unique, 
  FirstName VARCHAR(30) NOT NULL,
  MiddleName VARCHAR(30) NOT NULL,
  LastName VARCHAR(50) NOT NULL,
  Sex char(7) not null,
  Birthday DATE NOT NULL,
  Age int not null,
  Phone Numeric NOT NULL, 
  Email varchar(50) NOT NULL,
  DistrictId integer NOT NULL, 
  PRIMARY KEY (Aadhaar),
  FOREIGN KEY (DistrictId) references address(DistrictId));

-- Create party_table
CREATE TABLE IF NOT EXISTS party_table(
  PartyId int not null auto_increment ,
  PartyName varchar(50) not null unique,
  Symbol Varchar(20) not null unique,
  PartyLeader varchar(50) not null,
  LeaderAadhaar char(15) not null unique,
  PRIMARY KEY (PartyId),
  FOREIGN KEY (LeaderAadhaar) references voter_table(Aadhaar));

-- Create candidate_table
CREATE TABLE IF NOT EXISTS candidate_table(
  CandidateId int not null auto_increment ,
  Aadhaar char(15) not null unique,
  CandidateName varchar(100),
  PartyId int not null,
  DistrictId int not null,
  PRIMARY KEY (CandidateId),
  FOREIGN KEY (Aadhaar) references voter_table(Aadhaar),
  FOREIGN KEY (DistrictId) references address(DistrictId),
  FOREIGN KEY (PartyId) references party_table(PartyId));

-- Create user_table
CREATE TABLE IF NOT EXISTS user_table(
  VoterId varchar(10) not null,
  Aadhaar char(15) not null unique,
  _Password varchar(255) not null,
  IsActive BOOLEAN DEFAULT TRUE,
  PRIMARY KEY (VoterId),
  FOREIGN KEY (Aadhaar) references voter_table(Aadhaar));

-- Create vote_table
CREATE TABLE IF NOT EXISTS vote_table(
  VoteId int not null auto_increment,
  Aadhaar char(15) not null unique,
  PartyId int not null,
  CandidateId int not null,
  DistrictId int not null,
  PRIMARY KEY (VoteId),
  FOREIGN KEY (Aadhaar) references user_table(Aadhaar),
  FOREIGN KEY (CandidateId) references candidate_table(CandidateId),
  FOREIGN KEY (DistrictId) references address(DistrictId),
  FOREIGN KEY (PartyId) references party_table(PartyId));

-- Create result table
CREATE TABLE IF NOT EXISTS result(
  ResultId int not null auto_increment,
  CandidateId int not null,
  PartyId int not null,
  DistrictId int not null,
  Vote_Count int not null,
  PRIMARY KEY (ResultId),
  FOREIGN KEY (CandidateId) references candidate_table(CandidateId),
  FOREIGN KEY (DistrictId) references address(DistrictId),
  FOREIGN KEY (PartyId) references party_table(PartyId));

SET FOREIGN_KEY_CHECKS=1;

-- Create trigger for vote counting
DROP TRIGGER IF EXISTS Vote_counting;
DELIMITER //
CREATE TRIGGER Vote_counting
AFTER INSERT ON vote_table
FOR EACH ROW
BEGIN 
  IF NOT EXISTS (SELECT CandidateId FROM result WHERE result.CandidateId = NEW.CandidateId)
  THEN
    INSERT INTO result(CandidateId, PartyId, DistrictId, Vote_Count) VALUES(NEW.CandidateId, NEW.PartyId, NEW.DistrictId, 1);
  ELSE
    UPDATE result SET Vote_Count = Vote_Count + 1 WHERE CandidateId = NEW.CandidateId;
  END IF; 
END //
DELIMITER ;
