{{ config(materialized='external', location='yearly_trend.csv', format='csv')}}

select
    model_year
    ,count(*) as vehicle_count
from
    {{ ref('enriched_electric_vehicles') }}
group by
    model_year
order by 
    model_year
    ,vehicle_count desc
