SELECT county_state_name,
       population,
       CAST(
        REPLACE(`GHG emissions mtons CO2e`, ',', '')
        AS DOUBLE
        ) / NULLIF(
          CAST(
            REPLACE(`population`, ',', '')
            AS DOUBLE
            ), 0
          ) AS emissions_per_person
FROM emissions.default.emissions_data
ORDER BY emissions_per_person DESC