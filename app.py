    #######SETUP INICIAL
def trigger():    
    import streamlit as st
    import utils
    # notebook plots
    import seaborn as sns
    import matplotlib.pyplot as plt
    from googlemaps import Client as GoogleMaps
    
    ###LIBS API INTEGRAÇAO GOOGLE SHEETS
    import gspread
    
    # importing libs
    import numpy as np
    import pandas as pd
    # model object
    
    from dotenv import load_dotenv
    
    # maps
    import os
    from sqlalchemy import create_engine
    from matplotlib import cycler
    import statsmodels.api as sm
    import pydeck as pdk
    import plotly.figure_factory as ff
    import plotly.express as pexp
    import kaleido
    
    from PIL import Image, ImageDraw,ImageOps
    from math import radians
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    import smtplib
    from email import encoders
    import big_query
    import df_cleaner
    import build_report_images
    import linear_regression
    
       
    #styles
    colors = cycler('color',
                    ['#13C0B1', '#D83573', '#FAA446', '#7864C8', '#20B1DF', '#A3B243', '#AF86C2', '#DB866B', '#649ECB', '#90D6CD'])
    plt.rc('axes', prop_cycle=colors)
    #plt.rcParams['axes.spines.top'] = Falsestyle_map = {'fillColor': '#13C0B1', 'color': '#13C0B1'}
    
    
    load_dotenv()
    
    ###### INICIALIZA ENGINE
    host = os.environ['DATABASE_URL']
    conn = create_engine(host)
    
    ####### AUTENTICAÇAO GOOGLE SHEETS
    credentials = {
      "type": "service_account",
      "project_id": "full-building-pricing",
      "private_key_id": "80385e620e6b93fc8dee56a69f8d1785bd80eb77",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDOBDRGNGjmH+8b\nNjs/VAKYuwIwX94Xa7xEl8ettl8pLqjsvwPjplSXgIKKgJNE3k1dWJbnn6dUUyJU\nBKY9yToWBMRtCe4YtDkWD9/fR5IzGQh9I4vbOmX+6+7CRfAgn1HgT5fLAU4+xljf\nbIso+qSw3WRtvDj2GNNxR4/D0j0eENwhcU2sdPis4SMwMQX4CtmqajDTJedKLlbj\nLNHHmtwK5DtpR8qu8v+MIb/0h5qy7KRywXWawiySeKdved0rh+1/619CxREx8fRf\nfuBbUPblXsd4aCxdSdhE6ipXJQudHEwvXoTwCGESdNz8tM1PFN8LAzROsIHkgE8X\n942gyFVtAgMBAAECggEABAeYbCnsEvN1J/LOHHizGk17umC0Ek1oEwfMmJNa78Fh\nY+WymK1xG/Hs27+uSChFZ1OE+oZCOoe4jqzBznvIPpQ2Svm12T1BNpmPfY/dUx5X\n7t0XCCE8ZUzN6g/kvznOjkgp36DCNb+HqOS37h1ej+hGTB0xftYEE/dCrFTJUqd+\nlfXv6dGwk8cXM2NEa2d3H8lfo7Q55fv1LTyXvLgGkZLEAvl+WUOx64nSXUrtL1JD\nYABHkBHdb5r/KLbMIM8ORcrBAzTww0Lw0bBIioBDkvBV4X+H7LQP8nA2nOr2Iym9\nMlqrU5t9hUYagoG/MbjchpUs2RuXn/1+7nfFu5JV0QKBgQDny/bhp/U99ZgtIVPq\nhj2MxorLR2o55T7RUVFtlPpKtxVVj+vz1gnECJ+dFmUVO6JL7XALr5TjWHIU+KCd\nJMBDbksernFrT2z5cIpawvKGfRv+vwOrCculOmNUB/826TRRAXd3isYX65PKqmkP\nhSGBHWTS1556xoNji+yuZbpQlQKBgQDjhx60ChcLpHB8n2VDfaW7wVMKL5jExwnu\nLPPwr9lJNvG1jX2GS5eTp/xfy11RjbAD/k65ly0Qskz0aqzoUMDbr4a6r52as3f2\noknZafTw0Oxyw9rOFdjaz9yZfkNQ6dnPbPStCxHFrJiK4WRic143/uSSBDZ8tMKP\n+GGA14yDeQKBgEcyjRhu4JMxdpaWIBJvPUSaT1N1EhnKYmsk0SAZnG+KoNDxLgZt\nff5qr6wujsng0U8FFV9hhRf3uMLcQ2lBOpT7sbMw3cGaWdycRsLuElRg5VJwFY5Z\nqeWMc6oB8tBI/TrMeoeLZqE+SNz9Ttvnho0EHE3u0MzhYMYY2pAOyxWpAoGAPysd\nYBjJCydtP3w1bgZtQ/JJbrOGM2ObIzABzdnUdpo1gxU0O1uzSoBB9gqM7v5qVsF8\n89O/5DnMWbNgK+N3l8ZknmHxXKjk7mliHWVoZo9qhfZQQhUYrq807Lx8TfOO0CLM\nz1oaZgokE7K93wNurhcrOErJIdhBiB0KXO37CekCgYEA3aM+tzOcPm1wFQf+Hncx\nuO0R/F02TgLBOIM0lZEUSlRhKyBc357kCAnY6bP/ypX33cZ0vIQ1uoUYwULG0Gd8\nv4l9JSF4C+13y761kDTRlg/Hqo32b0JpqWOoCHcCuTu3ZgrvOBz8d3fpVbmvXBl9\n8ac32KSg7QFUTsOphu4KtoQ=\n-----END PRIVATE KEY-----\n",
      "client_email": "admin-583@full-building-pricing.iam.gserviceaccount.com",
      "client_id": "103304329065362639626",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/admin-583%40full-building-pricing.iam.gserviceaccount.com"
    }
    
    sheet_url = 'https://docs.google.com/spreadsheets/d/1w9F_zwKzHvmXr0ledojpHRiBchPXI7-RJDoMc5gVtoI'
    SCOPE = 'https://www.googleapis.com/auth/spreadsheets.currentonly'
    ###API_EXECUTABLE = 'M0f323sO4FMlxHJGofYsyZ1KrnsFW2JIv'
    
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open_by_url(sheet_url)
    worksheet = sh.get_worksheet(0)
    inputs_list = worksheet.row_values(4)
    print(inputs_list)
    
    ###### INPUT DE INFORMAÇÕES
         ### VARIAVEIS PARA TESTE NO NOTEBOOK
    email = inputs_list[0]
    address = inputs_list[1]
    area = int(inputs_list[2])
    bedrooms = int(inputs_list[3])
    bathrooms = int(inputs_list[4])
    development_year = int(inputs_list[5])
    radius = float(inputs_list[6])/100000
    new_buildings = inputs_list[7]
    #### GEOCODIFICA O ENDEREÇO 
    GMKey = 'AIzaSyBBPI4BGU_gTB2hpAINs7olQ0hRa6eBJeI'  ###LEMBRAR DEPOIS DE COLOCAR ISSO NO ENV
    gmaps = GoogleMaps(GMKey)
    try:
        geocode_result = gmaps.geocode(address)
    
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
    except:
        latitude = -23.56187859878245
        longitude = -46.6921353737258
    
    cm = sns.light_palette((260, 75, 60), input="husl", as_cmap=True)
    
    ######PREPARA QUERY GRANDE PARA MODELO
    df = big_query.big_query(latitude,longitude,radius,conn)
    
    ############# DATA CLEANING
    df_clean = df_cleaner.df_cleaner(df,latitude,longitude)
    
    #############REGRESSÃO PRECIFICAÇÃO  
    pred_mob,pred_n_mob,dataset_size = linear_regression.regression_lin(df_clean,area,development_year,bedrooms,bathrooms)
   
    #############RELATORIO GERAL
    build_report_images.trigger(df_clean,area,pred_mob,pred_n_mob,latitude,longitude,development_year)
    
    ####CREATE PRICING TABLE AS IMAGE
    ac_premium = 200
    garage_premium = 150
    dict_data = {'Valor Mobiliado':[pred_mob],'Valor Não Mobiliado':[pred_n_mob],'Premio Ar Condicionado':[ac_premium],'Premio Garagem':[garage_premium]}
    df_results = pd.DataFrame(dict_data)
    plt.figure(figsize = [10,6])
    ax = plt.subplot(111, frame_on=False) # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    pd.plotting.table(ax,df_results)
    plt.savefig('table_image.png')

#### MERGING ALL IMAGES INTO ONE
    ac_premium = 200
    garage_premium = 150

####CREATE PRICING TABLE AS IMAGE
    dict_data = {'Valor Mobiliado':[pred_mob],'Valor Não Mobiliado':[pred_n_mob],'Premio Ar Condicionado':[ac_premium],'Premio Garagem':[garage_premium],'Datapoints Modelagem Preço' : [dataset_size]}
    df_results = pd.DataFrame(dict_data)
    plt.figure(figsize = [10,6])
    ax = plt.subplot(111, frame_on=False) # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    pd.plotting.table(ax,df_results)
    plt.savefig('table_image.png')

#### MERGING ALL IMAGES INTO ONE
    result = Image.new("RGB", (1000, 1700),color = (255, 255, 255))
    im1 = Image.open('area_distribution.png')
    im2 = Image.open('bedrooms_distribution.png')
    im3 = Image.open('pricing_per_tipology.png')
    im4 = Image.open('pricing_per_sqm_distribution.png')
    im5 = Image.open('table_image.png')
    im6 = Image.open('building_year_distribution.png')
    im7 = Image.open('pricing_per_construction_year.png')
    im8 = Image.open('map_bedrooms_price.png')
    im8 = im8.resize((400,400))
    im8 = ImageOps.expand(im8, border=(1,1,1,1), fill="black")
    d = ImageDraw.Draw(im8)
    d.text((2,380),"Buildings colored by bedrooms per unit and sized by price per area",fontsize = 24,fill=(0,0,0))
    im9 = Image.open('map_age_price.png')
    im9 = im9.resize((400,400))
    im9 = ImageOps.expand(im9, border=(1,1,1,1), fill="black")
    d = ImageDraw.Draw(im9)
    d.text((2,380),"Buildings colored by construction year per unit and sized by price per area",fontsize = 24,fill=(0,0,0))

    result.paste(im5,(0,-320))
    result.paste(im1,(0,100))
    result.paste(im2,(450,100))
    result.paste(im3,(0,440))
    result.paste(im4,(450,440))
    result.paste(im6,(0,780))
    result.paste(im7,(450,780))
    result.paste(im8,(30,1120))
    result.paste(im9,(480,1120))
    d = ImageDraw.Draw(result)
    d.text((300,10),("{} - {} m²").format(address,area),fontsize = 48,fill=(0,0,0))


    result.save('report.pdf')
    
     
    sender_adress = "rolando.yucabot@gmail.com"
    passw = "1234!@#$" 
    toaddr = email
    
    # instance of MIMEMultipart
    msg = MIMEMultipart()
      
    # storing the senders email address  
    msg['From'] = sender_adress
      
    # storing the receivers email address 
    msg['To'] = toaddr
      
    # storing the subject 
    msg['Subject'] = "Relatorio Full Building - {address}".format(address = address)
      
    # string to store the body of the mail
    body = "Segue anexo seu relatorio"
      
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
      
    # open the file to be sent 
    filename = "report.pdf"
    attachment = open("report.pdf",'rb')
      
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
      
    # To change the payload into encoded form
    p.set_payload(attachment.read())
          
    # encode into base64
    encoders.encode_base64(p)
       
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
      
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
      
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
      
    # start TLS for security
    s.starttls()
      
    # Authentication
    s.login(sender_adress, passw)
      
    # Converts the Multipart msg into a string
    text = msg.as_string()
      
    # sending the mail
    s.sendmail(sender_adress, toaddr, text)
      
    # terminating the session
    s.quit()
    
trigger()