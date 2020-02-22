-- DROP TABLE `pthompsoDB`.`user_FullText_assoc`;

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


-- changed 02-22

-- DROP TABLE `pthompsoDB`.`user_FullText_assoc`;

CREATE TABLE `pthompsoDB`.`user_FullText_assoc` (
  `user_text_assoc_ID` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(2000) NOT NULL,
  `FullTextID` INT(11) NOT NULL,
  PRIMARY KEY (`user_text_assoc_ID`),
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