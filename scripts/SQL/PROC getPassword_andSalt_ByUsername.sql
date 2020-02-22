/*
USE `pthompsoDB`;
DROP procedure IF EXISTS `getPassword_andSalt_ByUsername`;

DELIMITER $$
USE `pthompsoDB`$$
CREATE PROCEDURE `getPassword_andSalt_ByUsername` (IN usernameIn VARCHAR(16))
BEGIN
SELECT `password`, `NaCl` FROM `pthompsoDB`.`userAccounts`
WHERE `username` = usernameIn;
END$$

DELIMITER 
*/


-- THEN CHANGED

USE `pthompsoDB`;
DROP procedure IF EXISTS `getPassword_andSalt_ByUsername`;

DELIMITER $$
USE `pthompsoDB`$$
CREATE DEFINER=`pthompso`@`%` PROCEDURE `getPassword_andSalt_ByUsername`(IN usernameIn VARCHAR(16), OUT password VARCHAR(32), OUT NaCl VARCHAR(32))
BEGIN
SELECT `password`, `NaCl` FROM `pthompsoDB`.`userAccounts`
WHERE `username` = usernameIn;
END$$

DELIMITER ;

