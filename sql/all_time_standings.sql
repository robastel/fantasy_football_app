SELECT
    manager_initials
    , first_place_count
    , second_place_count
    , third_place_count
    , made_playoffs_count
    , league_rating
    , regular_season_win_rate
    , regular_season_first_place_count
    , regular_season_most_points_count
    , regular_season_single_week_most_points_count
    , season_count
FROM
    robboli-broc.fantasy_football.managers
ORDER BY
    first_place_count DESC
    , second_place_count DESC
    , third_place_count DESC
    , made_playoffs_count DESC
    , league_rating DESC
    , regular_season_win_rate DESC
    , regular_season_first_place_count DESC
    , regular_season_most_points_count DESC
    , regular_season_single_week_most_points_count DESC
    , season_count DESC