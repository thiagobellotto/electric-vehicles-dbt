select
    "County" as county
    ,"City" as city
    ,"State" as state
    ,"Model Year" as model_year
    ,"Make" as make
    ,"Model" as model
    ,"Electric Range" as electric_range
    ,"Vehicle Location" as vehicle_location
from {{ source('external_source', 'electric_vehicles') }}
