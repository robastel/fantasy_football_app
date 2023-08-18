WITH top_single_weeks AS
(
    SELECT
        manager_initials
        , year
        , week
        , points
        , RANK() OVER(ORDER BY points DESC) AS ranking
    FROM
        robboli-broc.fantasy_football.matchups
    WHERE
        is_completed = 1
        AND is_median_matchup = 0
)

SELECT
    ranking
    , manager_initials
    , CAST(year AS STRING) AS year
    , week
    , points
FROM
    top_single_weeks
ORDER BY
    ranking