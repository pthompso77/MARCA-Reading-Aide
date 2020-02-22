/* -- DROP TABLE `userAccounts;
CREATE TABLE `userAccounts` (
  `email` varchar(2000) NOT NULL,
  `username` varchar(2000) NOT NULL,
  `password` varchar(2000) NOT NULL,
  `NaCl` varchar(2000) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
*/


-- 02-22
-- DROP TABLE `userAccounts`;
CREATE TABLE `userAccounts` (
  `email` varchar(2000) NOT NULL,
  -- DROPPED 02-22 `username` varchar(2000) NOT NULL,
  `password` varchar(2000) NOT NULL,
  `NaCl` varchar(2000) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `sessionID` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- DON'T NEED USERNAME
ALTER TABLE `pthompsoDB`.`userAccounts` 
DROP COLUMN `username`;
