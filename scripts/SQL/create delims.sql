CREATE TABLE `Highlight_Delims` (
  `fulltext_ID` int NOT NULL,
  `highlight_delim_start` int NOT NULL,
  `highlight_delim_end` int NOT NULL,
  PRIMARY KEY (`fulltext_ID`,`highlight_delim_start`),
  CONSTRAINT `text_highlight_FK` FOREIGN KEY (`fulltext_ID`) REFERENCES `FullText` (`FullText_ID`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Paragraph_Delims` (
  `fulltext_ID` int NOT NULL,
  `paragraph_delim_start` int NOT NULL,
  `paragraph_delim_end` int NOT NULL,
  PRIMARY KEY (`fulltext_ID`,`paragraph_delim_start`),
  CONSTRAINT `text_paragraph_FK` FOREIGN KEY (`fulltext_ID`) REFERENCES `FullText` (`FullText_ID`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Sentence_Delims` (
  `fulltext_ID` int NOT NULL,
  `sentence_delim_start` int NOT NULL,
  `sentence_delim_end` int NOT NULL,
  PRIMARY KEY (`fulltext_ID`,`sentence_delim_start`),
  CONSTRAINT `text_sentence_FK` FOREIGN KEY (`fulltext_ID`) REFERENCES `FullText` (`FullText_ID`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
