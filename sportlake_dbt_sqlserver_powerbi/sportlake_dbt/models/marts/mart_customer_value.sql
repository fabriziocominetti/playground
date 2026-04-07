{{ config(materialized='table') }}

with customers as (
    select * from {{
        ref('stg_customers')
    }}
),

ticketing as (
    select
        customer_id,
        count(ticket_id) as total_tickets_bought,
        sum(ticket_price) as lifetime_ticket_spend
    from {{ ref('stg_ticketing') }}
    group by customer_id
),

ecommerce as (
    select
        customer_id,
        count(order_id) as total_merch_orders,
        sum(order_amount) as lifetime_merch_spend
    from {{ ref('stg_ecommerce') }}
    group by customer_id
)

select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.membership_tier,
    c.joined_at,
    coalesce(t.total_tickets_bought, 0) as total_tickets_bought,
    coalesce(t.lifetime_ticket_spend, 0) as lifetime_ticket_spend,
    coalesce(e.total_merch_orders, 0) as total_merch_orders,
    coalesce(e.lifetime_merch_spend, 0) as lifetime_merch_spend,
    (coalesce(t.lifetime_ticket_spend, 0) + coalesce(e.lifetime_merch_spend, 0)) as total_lifetime_value
from customers c
left join ticketing t
    on c.customer_id = t.customer_id
left join ecommerce e
    on c.customer_id = e.customer_id
