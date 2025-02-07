
!pip install geopandas folium matplotlib owslib plotly pandas shapely

import folium
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from IPython.display import display, HTML


def adicionar_camada_wms(mapa, wms_url, layer_name, nome_exibicao):
    folium.raster_layers.WmsTileLayer(
        url=wms_url,
        layers=layer_name,
        name=nome_exibicao,
        fmt='image/png',
        transparent=True,
        attr='GeoPortal SGB'
    ).add_to(mapa)


def corrigir_orientacao(gdf):
    gdf['geometry'] = gdf['geometry'].apply(
        lambda geom: geom if geom.exterior.is_ccw else Polygon(geom.exterior.coords[::-1])
    )
    return gdf


m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)


wms_urls = {
    'Corrida de Massa': "http://geoportal.sgb.gov.br/server/services/gestaoterritorial/corrida_de_massa/MapServer/WMSServer?service=WMS",
    'Enxurrada': "http://geoportal.sgb.gov.br/server/services/gestaoterritorial/enxurrada/MapServer/WMSServer?service=WMS",
    'Perigo': "http://geoportal.sgb.gov.br/server/services/gestaoterritorial/perigo/MapServer/WMSServer?service=WMS",
    'Risco Geológico': "http://geoportal.sgb.gov.br/server/services/gestaoterritorial/risco/MapServer/WMSServer?service=WMS"
}

for camada, url in wms_urls.items():
    adicionar_camada_wms(m, url, '0', camada)


folium.LayerControl().add_to(m)


display(m)


dados = pd.DataFrame({
    'Ano': [2018, 2019, 2020, 2021, 2022, 2023],
    'Corrida de Massa': [15, 20, 25, 22, 30, 35],
    'Enxurrada': [10, 12, 18, 20, 25, 28],
    'Perigo': [5, 8, 10, 12, 14, 15]
})


fig = px.line(dados, x='Ano', y=['Corrida de Massa', 'Enxurrada', 'Perigo'],
              title='Ocorrências de Desastres Naturais por Ano',
              labels={'value':'Número de Ocorrências', 'variable':'Tipo de Desastre'},
              markers=True)
fig.update_traces(line=dict(width=3))
fig.show()


dados.to_csv('desastres_naturais_brasil.csv', index=False)


display(HTML(dados.to_html(index=False)))


print("Mapas WMS carregados com sucesso! Visualize os desastres naturais diretamente no mapa interativo.")
print("Gráficos interativos e dados exportados com sucesso!")
