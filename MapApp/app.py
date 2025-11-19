import streamlit as st
import pandas as pd
import geopandas as gpd
from geo_utils import plot_disability_map  
from geo_utils import plot_disability_mapw
from streamlit.components.v1 import html

#Chatgpt assistance to build the streamlit app 

st.set_page_config(page_title="CPS Disability Maps", layout="wide")

#Runwith: python -m streamlit run app.py

# Load data once and cache 

@st.cache_data
def load_cps_data():
    df19 = pd.read_csv('CPSdata19w-API.csv')
    df21 = pd.read_csv('CPSdata21w-API.csv')
    df12 = pd.read_csv('CPSdata12w-API.csv')

    columns_to_str = ['GESTFIPS', 'GEREG', "GTCO"]
    for df in [df19, df12, df21]:
        df[columns_to_str] = df[columns_to_str].astype(str)
        df['GESTFIPS'] = df['GESTFIPS'].str.zfill(2)
        df['GTCO'] = df['GTCO'].str.zfill(3)
        df['GEDIV'] = df['GEDIV'].astype(str)

    return {
        2012: df12,
        2019: df19,
        2021: df21
    }

DATA_BY_YEAR = load_cps_data()

# Configuration Dictionaries 

DISABILITY_OPTIONS = {
    "Any disability (PRDISFLG)": "PRDISFLG",
    "Cognitive difficulty (PEDISREM)": "PEDISREM",
    "Hearing difficulty (PEDISEAR)": "PEDISEAR",
    "Mobility difficulty (PEDISPHY)": "PEDISPHY",
    "Vision difficulty (PEDISEYE)": "PEDISEYE",
    "Self-care difficulty (PEDISDRS)": "PEDISDRS",
    "Independent living difficulty (PEDISOUT)": "PEDISOUT",
}

GEO_OPTIONS = {
    "State (GESTFIPS)": {
        "geo_group_col": "GESTFIPS",
        "shapefile_path": "tl_2021_us_state",  # directory or .shp
        "shape_geo_id_col": "GEOID"           # FIPS in shapefile
    },
    "Region (GEREG)": {
        "geo_group_col": "GEREG",
        "shapefile_path": "cb_2018_us_region_5m", 
        "shape_geo_id_col": "GEOID"           
    },
    "Division (GEDIV)": {
        "geo_group_col": "GEDIV",
        "shapefile_path": "cb_2018_us_division_5m", 
        "shape_geo_id_col": "GEOID"               
    },
}

# Streamlit UI 

st.title("CPS Disability Prevalence Explorer")

with st.sidebar:
    st.header("Map Settings")

    year = st.selectbox("Year", options=[2012, 2019, 2021], index=2)
    geo_label = st.selectbox("Geography", options=list(GEO_OPTIONS.keys()), index=0)
    disability_label = st.selectbox("Disability Type", options=list(DISABILITY_OPTIONS.keys()), index=0)

    cmap = st.selectbox("Color map", options=["viridis", "plasma", "magma", "cividis"], index=0)

    show_raw_table = st.checkbox("Show aggregated data table", value=False)

# Get config for selections
df = DATA_BY_YEAR[year]

geo_cfg = GEO_OPTIONS[geo_label]
disability_col = DISABILITY_OPTIONS[disability_label]

geo_group_col = geo_cfg["geo_group_col"]
shapefile_path = geo_cfg["shapefile_path"]
shape_geo_id_col = geo_cfg["shape_geo_id_col"]

st.markdown(f"### {disability_label} in {year} by {geo_label}")

# Create GeoDataFrame 

try:
    dgdf = plot_disability_mapw(
        df=df,
        geo_group_col=geo_group_col,
        shapefile_path=shapefile_path,
        shape_geo_id_col=shape_geo_id_col,
        disability_flag_col=disability_col,
        disability_yes_value=1,  # assuming 1 = yes, 2 = no
        count_col_name="n_disabled",
        total_col_name="n_total",
        prev_col_name="prev_disabled"
    )

    # show table of prevalence
    if show_raw_table:
        st.subheader("Aggregated prevalence data")
        st.dataframe(
            dgdf[[geo_group_col, "n_disabled", "n_total", "prev_disabled"]]
            .sort_values("prev_disabled", ascending=False)
        )

    #Create Interactive Map 
    # GeoPandas .explore() returns a Folium map with _repr_html_().
    m = dgdf.explore(
        column="prev_disabled",
        cmap=cmap,
        legend=True,
        tooltip=[geo_group_col, "n_disabled", "n_total", "prev_disabled", "mean_income"],
    )

    # Render map in Streamlit
    html(m._repr_html_(), height=600)

except Exception as e:
    st.error(f"Error generating map: {e}")
