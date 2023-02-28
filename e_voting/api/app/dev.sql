-- Initial Admin User
INSERT INTO users(nin, name, address, ward, state, lga, email, password, mobile_no, dob, gender, role, accredited)
VALUES ('12345678901', 'Mahadi Abuhuraira', 'Kofar doka', 'Kwarbai A','Kaduna', 'Zaria', 'mamt4real@evoting.com', '$2b$12$OpodI/WRRHJZJTo.Q3.pYONkC4XbmRYLaM63LQkTcTLv2vfeb9XHS', '08078786767','12-12-1990','male','admin',TRUE);

-- Sample user
INSERT INTO users(nin, name, address, ward, state, lga, email, password, mobile_no, dob, gender, role, accredited)
VALUES ('12345678902', 'Random user one', 'Sabon Gari', 'Kwarbai B','Kaduna', 'Makarfi', 'user1@evoting.com', '$2b$12$OpodI/WRRHJZJTo.Q3.pYONkC4XbmRYLaM63LQkTcTLv2vfeb9XHS', '08078786768','12-12-1999','male','user',TRUE);


-- random parties
INSERT INTO party(name, fullname, party_logo_url) VALUES ('APC','All Progressive Congress', 'apc.jpg');
INSERT INTO party(name, fullname, party_logo_url) VALUES ('LP','Labour Party', 'lp.jpg');
INSERT INTO party(name, fullname, party_logo_url) VALUES ('PDP','People Democratic Party', 'pdp.jpg');
INSERT INTO party(name, fullname, party_logo_url) VALUES ('NNPP','New Nigeria Political Party', 'nnpp.jpg');