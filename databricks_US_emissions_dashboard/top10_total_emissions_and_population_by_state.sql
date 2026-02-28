SELECT county_state_name,
       population,
       CAST(
        REPLACE(`GHG emissions mtons CO2e`, ',', '')
        AS DOUBLE
        ) AS total_emissions
FROM emissions.default.emissions_data
ORDER BY total_emissions DESC
LIMIT 10