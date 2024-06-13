-- Computes and store the average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    ALTER TABLE users ADD weighted_score INT NOT NULL;
    ALTER TABLE users ADD tw INT NOT NULL;

    UPDATE users
        SET weighted_score = (
            SELECT SUM(corrections.score * projects.weight)
            FROM corrections
                INNER JOIN projects
                    ON corrections.project_id = projects.id
            WHERE corrections.user_id = users.id
            );

    UPDATE users
        SET tw = (
            SELECT SUM(projects.weight)
                FROM corrections
                    INNER JOIN projects
                        ON corrections.project_id = projects.id
                WHERE corrections.user_id = users.id
            );

    UPDATE users
        SET users.average_score = IF(users.tw = 0, 0, users.weighted_score / users.tw);
    ALTER TABLE users
        DROP COLUMN weighted_score;
    ALTER TABLE users
        DROP COLUMN tw;
END;
//
DELIMITER ;
