# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 15:51:45 2021

@author: Mateus Medeiros
"""
import pandas as pd
import numpy as np
from math import radians

######PREPARA QUERY GRANDE PARA MODELO
def big_query(latitude,longitude,radius,conn):
    query = """
with distinct_properties as (
  select distinct
    parcel_id,
    construction_year
  from
    p798.properties
)
SELECT distinct
    -- Listings variables     
    listings.id,
    listings.source,
    listings.url,
    coalesce(listings.latitude, listings.inferred_latitude) as latitude,
    coalesce(listings.longitude, listings.inferred_longitude) as longitude,
    listings.area,
    listings.bathrooms,
    listings.bedrooms,
    listings.suites,
    listings.parking_lots,
    listings.unit_type,
    listings.rent_amount,
    listings.iptu_amount,
    listings.condo_amount,
    -- Apartment amenities     
    listings.amenities,
    case when listings.amenities ? 'CHUVEIRO_A_GAS' then 1 else 0 end as gas_shower,
    case when listings.source = '5A' then listings.last_published_time else listings.first_published_time end as first_published_time,
    listings.created_at as first_crawled_at,
    listings.updated_at as last_crawled_at,
    case when listings.near_subway = 'False' then 0 else 1 end as near_subway,
    case when listings.furnished = 'False' then 0 else 1 end as furnished,
    case when listings.air_conditioning = 'False' then 0 else 1 end as air_conditioning,
    listings.address,
    listings.neighbourhood,
    construction_year,
    listings.inactivated_time,
    for_rent,
    for_sale
     
FROM
    listings.dwd_listings as listings
LEFT JOIN
  distinct_properties pp on pp.parcel_id = listings.parcel_id
WHERE true
     and
    ((listings.source != '5A' and listings.first_published_time >= NOW() - interval '180 day') or
     (listings.source = '5A' and listings.last_published_time >= NOW() - interval '180 day'))
    and unit_type != 'HOME'
    -- and listings.city = 'São Paulo'   
    and bedrooms > 0 and bedrooms < 8   
    and bathrooms > 0 and bathrooms < 8
    and coalesce(longitude,inferred_longitude) between {lon} - {radius}/2 and {lon} + {radius}/2
    and coalesce(latitude,inferred_latitude) between {lat} - {radius}/2 and {lat} + {radius}/2
    """.format(lon = longitude, lat = latitude,radius = radius)

    print('big_query_start')

    df = pd.read_sql(query, conn)
 
    print('big_query_ok')
    return df
    