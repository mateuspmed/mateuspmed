# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 16:42:19 2021

@author: Mateus Medeiros
"""
import statsmodels.api as sm
import numpy as np

def regression_lin(df_clean,area,development_year,bedrooms,bathrooms):
     print(df_clean.head())
     if df_clean[df_clean['construction_year'] < 0].shape[0] == df_clean.shape[0]:
        df_ols = df_clean[['total_monthly_amount', 'area', 'price_per_area', 'parking_lots',
                          'bedrooms','bathrooms','furnished', 'air_conditioning', 'distance_to_FB',
                          'gas_shower','unit_type']]
        print('sem ano de construção')
    
    
     else:
        df_ols = df_clean[['total_monthly_amount', 'area', 'price_per_area', 'parking_lots',
                        'bedrooms','bathrooms','furnished', 'air_conditioning', 'distance_to_FB',
                        'construction_year', 'gas_shower','unit_type']]
    
        df_ols = df_ols[df_ols['construction_year'] > 0]
    
     df_ols = df_ols[df_ols['unit_type']!='HOME']
    
     df_ols.fillna(False, inplace=True)
     df_ols['intercept'] = 1
     df_ols['log_area'] = np.log(df_ols['area'])
    
     print(area)
     print(df_ols['area'].min())
     print(df_ols['area'].max())
     df_ols = df_ols[(df_ols['area'] >= area - 15) & (df_ols['area'] <= area + 15)]
     print(f'Making predictions with {df_ols.shape} datapoints')
     dataset_size =  df_ols.shape
     if 'construction_year' in df_ols.columns:
        reg = sm.OLS(np.log(df_ols['total_monthly_amount']),
                     df_ols[['intercept', 'parking_lots', 'log_area',
                             'bedrooms','bathrooms','furnished', 'air_conditioning', 'construction_year',
                             'gas_shower']]).fit()
    
        intercept = 1
        parking_lots = 0
        furnished = 1
        air_conditioning = 0
        year = development_year
    
        log_area = np.log(area)
    
        pred_mob = reg.predict([intercept, parking_lots, log_area, bedrooms, bathrooms, furnished,
                            air_conditioning, year, 1])[0]
    
        pred_mob = round(np.exp(pred_mob) + 400,2)
    
        pred_n_mob = reg.predict([intercept, parking_lots, log_area, bedrooms, bathrooms, 0,
                            air_conditioning, year, 1])[0]
    
        pred_n_mob = round(np.exp(pred_n_mob) + 400,2)
        
    
     else:
        reg = sm.OLS(np.log(df_ols['total_monthly_amount']),
                     df_ols[['intercept', 'parking_lots', 'log_area',
                             'bedrooms','bathrooms','furnished', 'air_conditioning',
                             'gas_shower']]).fit()
    
        intercept = 1
        parking_lots = 0
        bathrooms = 1
        furnished = 1
        air_conditioning = 0
    
        log_area = np.log(area)
    
        pred_mob = reg.predict([intercept, parking_lots, log_area, bedrooms, bathrooms, furnished,
                            air_conditioning, 1])[0]
    
        pred_mob = round(np.exp(pred_mob) + 400,2)
    
        pred_n_mob = reg.predict([intercept, parking_lots, log_area, bedrooms, bathrooms, 0,
                            air_conditioning, 1])[0]
    
        pred_n_mob = round(np.exp(pred_n_mob) + 400,2)
     print(pred_mob,pred_n_mob,dataset_size)
        
     return pred_mob,pred_n_mob,dataset_size

    