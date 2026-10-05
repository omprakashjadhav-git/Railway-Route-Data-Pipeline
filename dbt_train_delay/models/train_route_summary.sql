SELECT
    train_number,
    train_name,
    COUNT(*) AS total_stations,
    MAX(total_route_distance_km) AS total_route_distance_km,
    MAX(sequence) AS final_station_sequence
FROM {{ ref('stg_train_routes') }}
GROUP BY
    train_number,
    train_name