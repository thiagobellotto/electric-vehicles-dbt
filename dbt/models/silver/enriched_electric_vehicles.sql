with base as (
    select
        county
        ,city
        ,state
        ,cast(model_year as integer) as model_year
        ,make
        ,model
        ,electric_range
        ,cast(split_part(replace(replace(vehicle_location, 'POINT (', ''), ')', ''), ' ', 1) as string) as longitude
        ,cast(split_part(replace(replace(vehicle_location, 'POINT (', ''), ')', ''), ' ', 2) as string) as latitude
    from {{ ref('raw_electric_vehicles') }}
),

range_categories as (
    select
        *
        ,case
            when cast(electric_range as integer) = 0 then 'No Range'
            when cast(electric_range as integer) <= 50 then 'Short Range'
            when cast(electric_range as integer) <= 150 then 'Medium Range'
            when cast(electric_range as integer) > 150 then 'Long Range'
            else 'Unknown'
        end as range_category
    from base
)

select
    county
    ,city
    ,state
    ,model_year
    ,make
    ,model
    ,electric_range
    ,range_category
    ,longitude
    ,latitude
from range_categories
where state = 'WA' and model_year >= 2010 and model_year <= 2023
