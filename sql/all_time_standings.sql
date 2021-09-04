SELECT
    manager_initials
    , first_place_count
    , second_place_count
    , third_place_count
    , made_playoffs_count
    , regular_season_win_rate
    , season_count
FROM
    robboli-broc.fantasy_football.managers
ORDER BY
    first_place_count DESC
    , second_place_count DESC
    , third_place_count DESC
    , made_playoffs_count DESC
    , regular_season_win_rate DESC
    , season_count DESC