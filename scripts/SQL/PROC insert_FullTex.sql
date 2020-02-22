/* replaced 02-19 to include email in the insert (if not null)
CREATE DEFINER=`pthompso`@`%` PROCEDURE `insert_FullText`(IN tokenizedText TEXT)
BEGIN
INSERT INTO `pthompsoDB`.`FullText`
(`full_text`)
VALUES
(tokenizedText);
END
*/

USE `pthompsoDB`;
DROP procedure IF EXISTS `insert_FullText`;

DELIMITER $$
USE `pthompsoDB`$$
CREATE DEFINER=`pthompso`@`%` PROCEDURE `insert_FullText`(IN tokenizedText TEXT, IN userEmail VARCHAR(255))
BEGIN
DECLARE fulltextID INT DEFAULT 0;

INSERT INTO `pthompsoDB`.`FullText`
(`full_text`)
VALUES
(tokenizedText);

SET fulltextID = LAST_INSERT_ID();

INSERT INTO `pthompsoDB`.`user_FullText_assoc`
(`email`,
`FullTextID`)
VALUES
(userEmail,
fulltextID);
COMMIT;

END$$

DELIMITER ;

