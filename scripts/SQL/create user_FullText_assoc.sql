CREATE TABLE `pthompsoDB`.`user_FullText_assoc` (
  `email` VARCHAR(255) NOT NULL,
  `FullTextID` INT(11) NOT NULL,
  PRIMARY KEY (`email`, `FullTextID`),
  UNIQUE INDEX `FullTextID_UNIQUE` (`FullTextID` ASC),
  CONSTRAINT `FullText_FK`
    FOREIGN KEY (`FullTextID`)
    REFERENCES `pthompsoDB`.`FullText` (`FullText_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `userEmail_FK`
    FOREIGN KEY (`email`)
    REFERENCES `pthompsoDB`.`userAccounts` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);
