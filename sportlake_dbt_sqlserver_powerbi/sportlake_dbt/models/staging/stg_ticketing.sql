{{ config(materialized='view') }}

with source as (
    select * from {{
        source('sportlake_raw', 'raw_ticketing')
    }}
)

select
    ticket_id,
    customer_id,
    match_name,
    cast(match_date as date) as match_date,
    sector as stadium_sector,
    cast(price as float) as ticket_price
from source
