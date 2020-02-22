CREATE TABLE `pthompsoDB`.`paragraphs` (
  `doc_id` INT NOT NULL COMMENT 'ID of document this paragraph belongs to',
  `paragraph_number` INT NOT NULL COMMENT 'Number representing the order in which this paragraph text falls in the document (ex. 1 for the first paragraph, 2 for the second).',
  `paragraph_text` TEXT NOT NULL,
  INDEX `doc_paragraph_FK_idx` (`doc_id` ASC),
  PRIMARY KEY (`doc_id`, `paragraph_number`),
  CONSTRAINT `doc_paragraph_FK`
    FOREIGN KEY (`doc_id`)
    REFERENCES `pthompsoDB`.`documents` (`docID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
