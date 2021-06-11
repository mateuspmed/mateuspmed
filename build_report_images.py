# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 15:54:00 2021

@author: Mateus Medeiros
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import plotly.figure_factory as ff
import plotly.express as pexp
import kaleido
from PIL import Image, ImageDraw

def trigger(df_clean,area,pred_mob,pred_n_mob,latitude,longitude,development_year):
   #############RELATORIO GERAL

#########DISTRIBUICAO POR AREA
    fig, ax = plt.subplots()
    ax = sns.distplot(df_clean[(df_clean['distance_to_FB']<=1)]['area'], hist=True, kde=False)
    plt.axvline(x=df_clean.area.median(),linewidth=2, color='b', label="median", alpha=0.5)
    percent = np.percentile(df_clean['area'],90)
    plt.axvline(x=percent,linewidth=2, color='g', label="90percentile", alpha=0.5)
    plt.axvline(x=area,linewidth=2, color='r', label="my_unit", alpha=0.5)
    plt.ylabel("Quantity")
    plt.xlabel("Area Distribution (m²) ")
    plt.legend(["median", "90percentile","my_unit"])
    plt.savefig('area_distribution.png')


#############DISTRIBUICAO POR QUARTOS
    fig, ax = plt.subplots()
    ax = sns.countplot(df_clean[(df_clean['distance_to_FB']<=1)]['bedrooms'])
    plt.ylabel("Quantity")
    plt.xlabel("Bedrooms per Unit")
    plt.savefig('bedrooms_distribution.png')

##############PRECO POR NUM DE QUARTOS
    fig, ax = plt.subplots()
    ax = sns.boxplot(x="bedrooms", y="total_monthly_amount", data=df_clean)
    plt.ylabel("Total Monthly Package Cost")
    plt.xlabel("Bedrooms per Unit")
    plt.savefig('pricing_per_tipology.png')


############PRECO POR METRO QUADRADO
    fig, ax = plt.subplots()
    ax = sns.distplot(df_clean[(df_clean['distance_to_FB']<=1)]['price_per_area'], hist=True, kde=False)
    plt.axvline(x=df_clean.price_per_area.median(),linewidth=2, color='b', label="median", alpha=0.5)
    percent = np.percentile(df_clean['price_per_area'],90)
    plt.axvline(x=percent,linewidth=2, color='g', label="90percentile", alpha=0.5)
    plt.axvline(x=pred_mob/area,linewidth=2, color='r', label="suggested_my_unit", alpha=0.5)
    plt.ylabel("Quantity")
    plt.xlabel("Price per area (R$/m²) ")
    plt.legend(["median", "90percentile","suggested_my_unit"])
    plt.savefig('pricing_per_sqm_distribution.png')

############DISTRIBUIÇÃO DE IDADE DO PREDIO
    fig, ax = plt.subplots()
    ax = sns.distplot(df_clean[(df_clean['distance_to_FB']<=1) & (df_clean['construction_year']>0)]['construction_year'], hist=True, kde=False)
    fig.text(0.5,0.3,'This distribution only use datapoints \n with known construction year',fontsize = 8)
    plt.axvline(x=df_clean.construction_year.median(),linewidth=2, color='b', label="median", alpha=0.5)
    percent = np.percentile(df_clean['construction_year'],90)
    plt.axvline(x=percent,linewidth=2, color='g', label="90percentile", alpha=0.5)
    plt.axvline(x=development_year,linewidth=2, color='r', label="my_unit", alpha=0.5)
    plt.ylabel("Quantity")
    plt.xlabel("Construction Year")
    plt.legend(["median", "90percentile","my_unit"])
    plt.savefig('building_year_distribution.png')

############DISTRIBUIÇÃO DE PREÇO POR METRO QUADRADO PELA IDADE DOS IMOVEIS
    df_clean['construction_year_tier'] = pd.cut(df_clean['construction_year'],4,precision = 0)
    fig, ax = plt.subplots()
    ax = sns.boxplot(x="construction_year_tier", y="price_per_area", data=df_clean[(df_clean['distance_to_FB']<=1) & (df_clean['construction_year']>0)])
    plt.ylabel("Price per area (R$/m²)")
    plt.xlabel("Construction Year")
    plt.savefig('pricing_per_construction_year.png')

############PONTOS NO MAPA POR QUARTOS E PREÇO/M2
    token_mapbox = 'pk.eyJ1IjoibWF0ZXVzcG1lZCIsImEiOiJja3Bwc2FobXQwamF0MnZxanNzb21pa3Y2In0.6TkrFMdQzBpBcKytvK5lFQ'
    pexp.set_mapbox_access_token(token_mapbox)
    fig = pexp.scatter_mapbox(df_clean[(df_clean['distance_to_FB']<=1)], lat="latitude", lon="longitude",color="bedrooms", size="price_per_area",
                   size_max=15, zoom=15,center = dict(lat = latitude, lon = longitude))
    fig.write_image("map_bedrooms_price.png")

############PONTOS NO MAPA POR IDADE E PREÇO/M2
    fig = pexp.scatter_mapbox(df_clean[(df_clean['distance_to_FB']<=1) & (df_clean['construction_year']>0)], lat="latitude", lon="longitude",color="construction_year", size="price_per_area",
                   size_max=15, zoom=15,center = dict(lat = latitude, lon = longitude))
    fig.write_image("map_age_price.png")