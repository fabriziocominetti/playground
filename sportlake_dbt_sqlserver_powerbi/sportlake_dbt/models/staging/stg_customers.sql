{{ config(materialized='view') }}

with source as (
    select * from {{
        source('sportlake_raw', 'raw_customers')
    }}
)

select
    customer_id,
    first_name,
    last_name,
    email,
    city,
    membership_tier,
    cast(join_date as date) as joined_at
from source
