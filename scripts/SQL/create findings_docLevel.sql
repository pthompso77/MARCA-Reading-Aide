CREATE TABLE `pthompsoDB`.`findings_docLevel` (
  `findings_docLevel_ID` INT NOT NULL AUTO_INCREMENT,
  `doc_id` INT NOT NULL,
  `paragraph_id` INT NOT NULL,
  `topic_id` INT NOT NULL,
  `confidence_measure` DECIMAL NULL,
  PRIMARY KEY (`findings_docLevel_ID`),
  INDEX `paragraph_FK_idx` (`doc_id` ASC, `paragraph_id` ASC),
  INDEX `finding_topic_FK_idx` (`topic_id` ASC),
  CONSTRAINT `finding_paragraph_FK`
    FOREIGN KEY (`doc_id` , `paragraph_id`)
    REFERENCES `pthompsoDB`.`paragraphs` (`doc_id` , `paragraph_number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `finding_topic_FK`
    FOREIGN KEY (`topic_id`)
    REFERENCES `pthompsoDB`.`topics` (`topics_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
