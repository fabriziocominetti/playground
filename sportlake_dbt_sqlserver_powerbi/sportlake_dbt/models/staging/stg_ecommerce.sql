{{ config(materialized='view') }}

with source as (
    select * from {{
        source('sportlake_raw', 'raw_ecommerce')
    }}
)

select
    order_id,
    customer_id,
    product_name,
    cast(order_date as date) as order_date,
    cast(total_amount as float) as order_amount
from source
