-- Insert sample districts
INSERT IGNORE INTO address VALUES(234,"Andheri","Mumbai","Maharashtra","400059");
INSERT IGNORE INTO address VALUES(235,"Hadapsar","Pune","Maharashtra","411013");

-- Insert sample voters
INSERT IGNORE INTO voter_table VALUES("359146283661","Akash","Kumar","Singh","M","1984-02-16",37,9623412913,"akash@example.com",234);
INSERT IGNORE INTO voter_table VALUES("577379407366","Dipti","Sharma","Kumar","F","1998-01-13",23,9222325956,"dipti@example.com",235);
INSERT IGNORE INTO voter_table VALUES("782034294038","Shlok","Vikram","Agarwal","M","1988-02-04",33,9722768470,"shlok@example.com",234);
INSERT IGNORE INTO voter_table VALUES("616950285641","Rashid","Ahmed","Khan","M","1976-10-17",44,9414321457,"rashid@example.com",235);

-- Insert parties
INSERT IGNORE INTO party_table(PartyName, Symbol, PartyLeader, LeaderAadhaar) VALUES("BJP","Lotus","Narendra Modi","359146283661");
INSERT IGNORE INTO party_table(PartyName, Symbol, PartyLeader, LeaderAadhaar) VALUES("INC","Hand","Rahul Gandhi","577379407366");

-- Insert candidates
INSERT IGNORE INTO candidate_table(Aadhaar, CandidateName, PartyId, DistrictId) VALUES("782034294038","Shlok Agarwal",1,234);
INSERT IGNORE INTO candidate_table(Aadhaar, CandidateName, PartyId, DistrictId) VALUES("616950285641","Rashid Khan",2,235);

-- Insert users
INSERT IGNORE INTO user_table(VoterId, Aadhaar, _Password) VALUES("AK1234567","359146283661","password123");
INSERT IGNORE INTO user_table(VoterId, Aadhaar, _Password) VALUES("DP1234568","577379407366","password456");

-- Insert sample inactive voter for lockout testing (IsActive = 0)
INSERT IGNORE INTO voter_table VALUES("999999999999","DECEASED","VOTER","TEST","M","1970-01-01",56,9000000000,"deceased@example.com",234);
INSERT IGNORE INTO user_table(VoterId, Aadhaar, _Password, IsActive) VALUES("DE1234567","999999999999","password789",0);
