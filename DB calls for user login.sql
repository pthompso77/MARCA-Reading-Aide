-- get password and salt by email address
SELECT password, NaCl FROM pthompsoDB.userAccounts WHERE email = 'email@here.there';

-- get email address by sessionID
SELECT email
FROM userAccounts
WHERE sessionID = 'singsongdadadoo';

--  create new user
INSERT INTO userAccounts
(email, password, NaCl, sessionID)
VALUES
('testemail1@mail.com',
'biglonghashthing',
'saltywalty',
NULL);

	--  update email address
	UPDATE userAccounts
	SET email = 'testemail1@mail.com'
	WHERE email = 'testemail2@mail.com';
	
 	-- update password
	UPDATE userAccounts
	SET password = 'anotherbighashdigest',
    NaCl = 'newsaltysalty'
	WHERE email = 'testemail1@mail.com';
	
--  set sessionID
UPDATE userAccounts
SET sessionID = 'another-sessionID9847847'
WHERE email = 'testemail1@mail.com';

 	-- unset sessionID
	UPDATE userAccounts
	SET sessionID = NULL
	WHERE email = 'testemail1@mail.com';