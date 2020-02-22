CREATE TABLE `userAccounts` (
  `email` varchar(255) NOT NULL,
  `username` varchar(16) NOT NULL,
  `password` varchar(32) NOT NULL,
  `NaCl` varchar(32) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- then...

ALTER TABLE `pthompsoDB`.`userAccounts` 
ADD COLUMN `sessionID` VARCHAR(2000) NULL AFTER `create_time`;
