import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# df = pd.DataFrame(data)
df = pd.read_excel("tipos_residuos.xlsx", sheet_name="Sheet1")
df_location = pd.read_excel("tipos_residuos.xlsx", sheet_name="Sheet2")

# Configuração inicial
st.set_page_config(page_title="Dashboard dos Resíduos", page_icon="🗑️", layout="wide")

# Sidebar - Filtros
st.sidebar.header("Selecione os Filtros")

categorias = st.sidebar.multiselect(
    "Categoria",
    options=df["categoria"].unique(),
    default=df["categoria"].unique(),
    key="categorias"
)

# Filtrar o dataframe de acordo com as opções selecionadas
df_selecao = df.query("categoria in @categorias")

locais = {
    "Jundiaí - SP": {"latitude": -23.1865, "longitude": -46.8845},
    "Itatiba - SP": {"latitude": -23.0068, "longitude": -46.8387},
    "Americana - SP": {"latitude": -22.7392, "longitude": -47.3236},
    "Ribeirão Preto - SP": {"latitude": -21.1775, "longitude": -47.8103},
    "Lençóis Paulista - SP": {"latitude": -22.59861, "longitude": -48.8003},
    "Rio de Janeiro - RJ": {"latitude": -22.9068, "longitude": -43.1729},
    "Nova Friburgo - RJ": {"latitude": -22.2871, "longitude": -42.5337},
    "Guarapari - ES": {"latitude": -20.6667, "longitude": -40.6333},
    "Belo Horizonte - MG": {"latitude": -19.8416, "longitude": -43.9865},
    "Ipatinga - MG": {"latitude": -19.4676, "longitude": -42.5484},
    "Salvador - BA": {"latitude": -12.9747, "longitude": -38.5016},
    "Delmiro Gouveia - AL": {"latitude": -9.3886, "longitude": -37.9992},
    "Cabedelo - PB": {"latitude": -6.9802, "longitude": -34.8304},
    "Natal - RN": {"latitude": -5.8128, "longitude": -35.2551},
    "Fortaleza - CE": {"latitude": -3.7333, "longitude": -38.5276},
    "Bequimão - MA": {"latitude": -2.4330, "longitude": -44.7830},
    "Salinópolis - PA": {"latitude": 0.6136, "longitude": -47.5967},
    "Brasília - DF": {"latitude": -15.7939, "longitude": -47.8828},
    "Goiânia - GO": {"latitude": -16.6799, "longitude": -49.2550},
    "Campo Grande - MS": {"latitude": -20.4428, "longitude": -54.6464},
    "Curitiba - PR": {"latitude": -25.4284, "longitude": -49.2731},
    "Londrina - PR": {"latitude": -23.3045, "longitude": -51.1775},
    "Florianópolis - SC": {"latitude": -27.5935, "longitude": -48.5585},
    "Gravataí - RS": {"latitude": -29.9167, "longitude": -51.0569},
    "Santa Maria - RS": {"latitude": -29.6914, "longitude": -53.8008},
    "São Paulo - SP": {"latitude": -23.5505, "longitude": -46.6333},
    "Guarulhos - SP": {"latitude": -23.4549, "longitude": -46.5333},
    "Mauá - SP": {"latitude": -23.6670, "longitude": -46.4610},
    "Santa Cruz da Conceição - SP": {"latitude": -22.1403, "longitude": -47.2740},
    "Recife - PE": {"latitude": -8.0539, "longitude": -34.8811},
    "Olinda - PE": {"latitude": -7.9990, "longitude": -34.8830},
    "Palmares - PE": {"latitude": -8.9930, "longitude": -35.4940},
    "São Luís - MA": {"latitude": -2.5297, "longitude": -44.3020},
    "Eldorado do Sul - RS": {"latitude": -30.0331, "longitude": -51.2300},
    "Sapucaia do Sul - RS": {"latitude": -29.9167, "longitude": -51.2740}
}


def Graficos():
    df_selecao = df.query("categoria in @categorias")

    # Gráfico de pizza (pie chart)
    fig_categorias = px.pie(
        df_selecao,
        names="categoria",
        values="quantidade total",
        title="Distribuição de Resíduos por Categoria"
    )
    st.plotly_chart(fig_categorias, use_container_width=True)

    # Gráfico de barras
    df_categoria = df.groupby("categoria")["quantidade total"].sum().reset_index()
    fig_barras = px.bar(
        df_categoria,
        x="categoria",
        y="quantidade total",
        title="Quantidade Total por Categoria",
        labels={"quantidade total": "Quantidade"},
        color="categoria"
    )

    fig_barras.update_layout(
        font_color="purple"  # Change y-axis label color
    )

    st.plotly_chart(fig_barras, use_container_width=True)

    # Mapa
    st.markdown("### Localização das coletas")

    # Convert the 'locais' dictionary to a DataFrame
    df_locais = pd.DataFrame.from_dict(locais, orient='index')
    df_locais['location_name'] = df_locais.index
    df_locais.rename(columns={'latitude': 'lat', 'longitude': 'lon'}, inplace=True)

    # Display the map using the DataFrame
    st.map(df_locais[['lat', 'lon']])

    # Stacked Bar Chart - Cities x Category
    st.markdown("### Geração de Resíduos por Categoria e Cidade")
    # Assuming your data is in 'df_location'
    # First, melt the dataframe to long format
    id_vars = ['tipo', 'categoria']
    value_vars = [col for col in df_location.columns if col not in id_vars]
    df_melted = pd.melt(df_location, id_vars=id_vars, value_vars=value_vars, var_name='Cidade', value_name='Quantidade')

    # Then, create the stacked bar chart
    fig_stacked_bar = px.bar(df_melted, x="Cidade", y="Quantidade", color="categoria",
                             title="Quantidade de Resíduos por Cidade e Categoria",
                             labels={"Quantidade": "Quantidade de Resíduos"},
                             )
    st.plotly_chart(fig_stacked_bar, use_container_width=True)



Graficos()
