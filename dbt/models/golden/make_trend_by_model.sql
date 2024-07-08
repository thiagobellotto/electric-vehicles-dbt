{{ config(materialized='external', location='make_trend_by_model.csv', format='csv')}}

select
    model_year
    ,make
    ,model
    ,count(*) as vehicle_count
from
    {{ ref('enriched_electric_vehicles') }}
group by
    model_year
    ,make
    ,model
order by 
    model_year
    ,make
    ,model
    ,vehicle_count desc    
