CREATE TABLE `pthompsoDB`.`topics` (
  `topics_ID` INT NOT NULL AUTO_INCREMENT,
  `topic` VARCHAR(45) NULL COMMENT 'Might want to represent this differently',
  PRIMARY KEY (`topics_ID`),
  UNIQUE INDEX `topic_UNIQUE` (`topic` ASC));
