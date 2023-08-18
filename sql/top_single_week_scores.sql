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
        1.0 * COUNT(matchup_id) / COUNT(DISTINCT season_id) AS avg_matchups_per_season
    FROM
        robboli-broc.fantasy_football.matchups
    WHERE
        is_median_matchup = 0
)

SELECT
    tsw.ranking
    , tsw.manager_initials
    , CAST(tsw.year AS STRING) AS year
    , tsw.week
    , tsw.points
    , mps.avg_matchups_per_season
FROM
    top_single_weeks AS tsw
INNER JOIN
    matchups_per_season AS mps
    ON 1=1
ORDER BY
    ranking