SELECT
    manager_id
    , manager_initials
    , points
FROM
    robboli-broc.fantasy_football.matchups
WHERE
    is_completed = 1
    AND is_median_matchup = 0