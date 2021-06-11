# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 15:44:39 2021

@author: Mateus Medeiros
"""
import pandas as pd
from math import radians
import utils
import numpy as np

def df_cleaner(df,latitude,longitude):
        # Padroniza o nome dos bairros
        #df = utils.standardize_listings_neighbourhood(df, 'neighbourhood')
        
        # separa em diferentes tipologias
        df_aps, df_casas, df_flats = utils.separa_tipos_imoveis(df, 'unit_type')
    
        # inferência de condo e iptu para apartamentos
        df_aps, _ = utils.infer_numeric_by_region(df_aps, 'neighbourhood', 'iptu_amount')
        df_aps, _ = utils.infer_numeric_by_region(df_aps, 'neighbourhood', 'condo_amount')
    
        # inferência de condo e iptu para casas
        df_casas, _ = utils.infer_numeric_by_region(df_casas, 'neighbourhood', 'iptu_amount')
        df_casas['condo_amount'].fillna(0, inplace=True)
        df_casas, _ = utils.infer_numeric_by_region(df_casas, 'neighbourhood', 'condo_amount')
        df_casas['condo_amount_infer'].fillna(0, inplace=True)
    
        # inferência de condo e iptu para flats
        df_flats, _ = utils.infer_numeric_by_region(df_flats, 'neighbourhood', 'iptu_amount')
        df_flats, _ = utils.infer_numeric_by_region(df_flats, 'neighbourhood', 'condo_amount')
    
        # concatena os dfs
        df_clean = pd.concat([df_aps, df_casas, df_flats], axis=0)
    
        print(len(df_clean))
        # condo_amount_final e iptu_amount_final baseado nos valores aferidos e inferidos
        df_clean.loc[((df_clean.condo_amount == 0) | (df_clean.condo_amount.isnull() == True)), 'condo_amount_final'] = df_clean.loc[((df_clean.condo_amount == 0) | (df_clean.condo_amount.isnull() == True)), 'condo_amount_infer']
        df_clean.loc[~((df_clean.condo_amount == 0) | (df_clean.condo_amount.isnull() == True)), 'condo_amount_final'] = df_clean.loc[~((df_clean.condo_amount == 0) | (df_clean.condo_amount.isnull() == True)), 'condo_amount']
        df_clean['condo_inferred'] = -10
        df_clean.loc[((df_clean.condo_amount == 0) | (df_clean.condo_amount.isnull() == True)), 'condo_inferred'] = 1
        df_clean.loc[~((df_clean.condo_amount == 0) | (df_clean.condo_amount.isnull() == True)), 'condo_inferred'] = 0
    
        df_clean.loc[((df_clean.iptu_amount == 0) | (df_clean.iptu_amount.isnull() == True)), 'iptu_amount_final'] = df_clean.loc[((df_clean.iptu_amount == 0) | (df_clean.iptu_amount.isnull() == True)), 'iptu_amount_infer']
        df_clean.loc[~((df_clean.iptu_amount == 0) | (df_clean.iptu_amount.isnull() == True)), 'iptu_amount_final'] = df_clean.loc[~((df_clean.iptu_amount == 0) | (df_clean.iptu_amount.isnull() == True)), 'iptu_amount']
        df_clean['iptu_inferred'] = -10
        df_clean.loc[((df_clean.iptu_amount == 0) | (df_clean.iptu_amount.isnull() == True)), 'iptu_inferred'] = 1
        df_clean.loc[~((df_clean.iptu_amount == 0) | (df_clean.iptu_amount.isnull() == True)), 'iptu_inferred'] = 0
    
        # mantem apenas propriedades q temos infos de condo e iptu
        df_clean = df_clean[(df_clean['condo_amount_final'].isnull() == False) & (df_clean['iptu_amount_final'].isnull() == False)].copy()
        df_clean.drop(['iptu_amount', 'condo_amount', 'iptu_amount_infer', 'condo_amount_infer'], axis=1, inplace=True)
    
        # fill suites and parking lots
        df_clean['suites'].fillna(0, inplace=True)
        df_clean['parking_lots'].fillna(0, inplace=True)
    
        # fill last_crawled at with the first_crawled_at values
        df_clean['last_crawled_at'].fillna(df_clean['first_crawled_at'], inplace=True)
    
        # removing time zones
        df_clean['first_published_time'] = df_clean['first_published_time'].apply(lambda x: x.replace(tzinfo=None))
        df_clean['first_crawled_at'] = df_clean['first_crawled_at'].apply(lambda x: x.replace(tzinfo=None))
        df_clean['last_crawled_at'] = df_clean['last_crawled_at'].apply(lambda x: x.replace(tzinfo=None))
        df_clean['inactivated_time'] = df_clean['inactivated_time'].apply(lambda x: x.replace(tzinfo=None))
    
        # remoção de duplicados
        df_clean = utils.clean_duplicates_crawler(df_clean, publication_date_var='first_published_time')
        df_clean.set_index('id', inplace=True)
    
        df_clean['fb_latitude'] = float(latitude)
        df_clean['fb_longitude'] = float(longitude)
        
        
    
        def haversine(lat_1, lon_1, lat_2, lon_2):
            lat_1 = radians(lat_1)
            lon_1 = radians(lon_1)
            
            lat_2 = radians(lat_2)
            lon_2 = radians(lon_2)
        
            radians_distance = 2 * np.arcsin(np.sqrt((np.sin((lat_1 - lat_2) / 2))**2 + np.cos(lat_1) * np.cos(lat_2) * (np.sin((lon_1 - lon_2) / 2))**2))
            km_distance = radians_distance * 6371000 / 1000
        
            return km_distance
    
        df_clean['distance_to_FB'] = df_clean.apply(lambda row: haversine(row['latitude'], 
                                                                      row['longitude'], 
                                                                      row['fb_latitude'], 
                                                                      row['fb_longitude']), axis=1)
    
    
        df_clean['total_monthly_amount'] = df_clean['rent_amount'] + df_clean['condo_amount_final'] + df_clean['iptu_amount_final']
        df_clean['price_per_bedroom'] = df_clean['total_monthly_amount']/df_clean['bedrooms']
        df_clean['price_per_area'] = df_clean['total_monthly_amount']/df_clean['area']
    
        df_clean = df_clean[df_clean['total_monthly_amount'] <= 15000]
        df_clean = df_clean[df_clean['bedrooms']>0]
        df_clean = df_clean[df_clean['bathrooms']>0]
        df_clean = df_clean[df_clean['bedrooms']<=5]
        df_clean = df_clean[df_clean['bathrooms']<=5]
        df_clean = df_clean[df_clean['parking_lots']<=5]
        df_clean = df_clean[df_clean['area']<=400]
        return df_clean