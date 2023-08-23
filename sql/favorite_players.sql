WITH player_counts_by_manager AS (
    SELECT
        manager_id
        , manager_initials
        , REGEXP_REPLACE(REPLACE(player_name, '.', ''), '(\\s(jr|sr).*|(\\s(i|v)(i|v)+)).*', '') AS player_name
        , COUNT(1) AS seasons_drafted_count
    FROM
        robboli-broc.staging.draft_picks
    WHERE
        player_position != 'def'
    GROUP BY
        1,2,3
)

SELECT
    manager_initials
    , STRING_AGG(INITCAP(player_name) || ' (' || seasons_drafted_count || ')', ', ' ORDER BY seasons_drafted_count DESC) AS favorite_players
FROM
    player_counts_by_manager
WHERE
    seasons_drafted_count > 2
GROUP BY
    1
ORDER BY
    1