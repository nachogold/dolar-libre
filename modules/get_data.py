#TO DO:
#AGREGAR LOGS QUE SE ENVÍEN A UN ARCHIVO

from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

def get_data():
    #initialize parameters
    current_timestamp = datetime.utcnow()
    try:
        #dolarhoy
        url = 'https://dolarhoy.com/'
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        compra = soup.find("div",class_='compra')
        venta = soup.find("div",class_='venta')

        valor_compra = compra.text.split('$')[1]
        valor_venta = venta.text.split('$')[1]

        df_dolarhoy = pd.DataFrame()
        df_dolarhoy.at[0, 'site'] = 'dolarhoy'
        df_dolarhoy.at[0, 'timestamp'] = current_timestamp
        df_dolarhoy.at[0, 'compra'] = float(valor_compra)
        df_dolarhoy.at[0, 'venta'] = float(valor_venta)
    except:
        print('error dolarhoy')

    try:
        #cronista
        url = 'https://www.cronista.com/MercadosOnline/moneda.html?id=ARSB'
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        compra = soup.find("div",class_='buy-value')
        venta = soup.find("div",class_='sell-value')

        venta.text.split('$')#[1].replace(',','.')

        valor_compra = compra.text.split('$')[1].replace(',','.')
        valor_venta = venta.text.split('$')[1].replace(',','.')

        df_cronista = pd.DataFrame()
        df_cronista.at[0, 'site'] = 'cronista'
        df_cronista.at[0, 'timestamp'] = current_timestamp
        df_cronista.at[0, 'compra'] = float(valor_compra)
        df_cronista.at[0, 'venta'] = float(valor_venta)
    except:
        print('error cronista')

    try:
        #ambito
        #ambito genera los valores de compra y venta via JS, por lo que BS no sirve. Encontré la url de donde trae la data y puedo traer el json con requests.
        #Para encontrar esta url ir a inspeccionar, tab de "Network" y sub-tab de "Fetch/XHR". Ahi estan todas las requests hechas desde el sitio y se puede ver: la respuesta, que archivo js lo hizo, etc.
        url = 'https://mercados.ambito.com//dolar/informal/variacion'
        values = requests.get('https://mercados.ambito.com//dolar/informal/variacion').json() 

        compra = values['compra']
        venta = values['venta']

        valor_compra = compra.replace(',','.')
        valor_venta = venta.replace(',','.')

        df_ambito = pd.DataFrame()
        df_ambito.at[0, 'site'] = 'ambito'
        df_ambito.at[0, 'timestamp'] = current_timestamp
        df_ambito.at[0, 'compra'] = float(valor_compra)
        df_ambito.at[0, 'venta'] = float(valor_venta)
    except:
        print('error ambito')

    try:
        #calculamos promedio y generamos df final
        df_combined = pd.concat([df_dolarhoy, df_cronista, df_ambito], ignore_index=True)

        compra_promedio = df_combined['compra'].mean()
        venta_promedio = df_combined['venta'].mean()

        df_promedio = pd.DataFrame()
        df_promedio.at[0, 'site'] = 'promedio'
        df_promedio.at[0, 'timestamp'] = current_timestamp
        df_promedio.at[0, 'compra'] = float(compra_promedio)
        df_promedio.at[0, 'venta'] = float(venta_promedio)

        df_final= pd.concat([df_combined, df_promedio], ignore_index=True)
    except:
        print('error armado df_final')

    return df_final
