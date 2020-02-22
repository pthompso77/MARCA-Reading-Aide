-- 02-22
USE `pthompsoDB`;
DROP procedure IF EXISTS `pthompsoDB`.`insert_FullTexts`;

DELIMITER $$
USE `pthompsoDB`$$
CREATE DEFINER=`pthompso`@`%` PROCEDURE `insert_FullText`(IN tokenizedText TEXT, OUT output INT)
BEGIN

INSERT INTO `pthompsoDB`.`FullText`
(`full_text`)
VALUES
('tokenizedText');
COMMIT;

SET output = last_insert_id();

END$$

DELIMITER ;
;
