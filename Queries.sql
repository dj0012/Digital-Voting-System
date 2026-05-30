-- # What if a person changes their phone number permanently?
UPDATE voter_table SET Phone = 9283478293 WHERE Aadhaar = "577379407366";


-- # What will you do if for some political reason voting needs to occur again and you have to delete all rows from the vote and result table?
TRUNCATE result;
TRUNCATE vote_table;
SELECT * FROM result;
SELECT * FROM vote_table;


-- # Do you want to know how many people voted from a particular district?
CREATE OR REPLACE VIEW district_vote_count AS
SELECT DistrictId, SUM(Vote_Count) AS 'Total_District_Votes'
FROM result
GROUP BY DistrictId;

SELECT * FROM district_vote_count;
DROP VIEW IF EXISTS district_vote_count;


-- # Do you know how many votes each party got from all the districts combined?
CREATE OR REPLACE VIEW party_vote_count AS
SELECT r.PartyId, pt.PartyName, SUM(r.Vote_Count) AS 'Total_Count'
FROM result r
INNER JOIN party_table pt ON pt.PartyId = r.PartyId
GROUP BY r.PartyId, pt.PartyName
ORDER BY Total_Count DESC;

SELECT * FROM party_vote_count;
DROP VIEW IF EXISTS party_vote_count;


-- # What will we do with a person's information who is inactive / deceased?
-- # Safe lookup to count inactive voters
SELECT COUNT(*) FROM user_table WHERE IsActive = FALSE;

-- # Clean deletion of inactive voter records using secure ANSI joins
DELETE vt, ut 
FROM voter_table vt 
INNER JOIN user_table ut ON vt.Aadhaar = ut.Aadhaar 
WHERE ut.IsActive = FALSE;


-- # Want all the details related to each candidate?
CREATE OR REPLACE VIEW candidate_detail AS
SELECT ct.CandidateId, pt.PartyName, vt.Aadhaar, vt.FirstName, vt.MiddleName, vt.LastName, vt.Sex, vt.Birthday, vt.Age, vt.Phone, vt.Email, ct.DistrictId
FROM candidate_table ct 
LEFT JOIN voter_table vt ON ct.Aadhaar = vt.Aadhaar
INNER JOIN party_table pt ON pt.PartyId = ct.PartyId;

SELECT * FROM candidate_detail;
DROP VIEW IF EXISTS candidate_detail;
