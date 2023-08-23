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

, matchups_per_season AS (
    SELECT
        1.0 * COUNT(m.matchup_id) / COUNT(DISTINCT m.season_id) AS avg_matchups_per_season
    FROM
        robboli-broc.fantasy_football.matchups AS m
    INNER JOIN
        robboli-broc.staging.seasons AS s
        ON m.season_id = s.season_id
        AND s.last_completed_week = s.total_weeks
    WHERE
        m.is_completed = 1
        AND m.is_median_matchup = 0
)

SELECT
    tsw.ranking
    , tsw.manager_initials
    , CONCAT(CAST(tsw.year AS STRING), ' Week ', CAST(tsw.week AS STRING)) AS week
    , tsw.points
    , mps.avg_matchups_per_season
FROM
    top_single_weeks AS tsw
CROSS JOIN
    matchups_per_season AS mps
ORDER BY
    ranking