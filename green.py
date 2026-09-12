import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import dual_annealing
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Quantum Green Fleet", layout="wide")
st.title("🌱 Quantum-Inspired Fuel & Green Fleet Optimization")
st.write("ഇന്ധനച്ചിലവും കാർബൺ എമിഷനും കുറയ്ക്കാനുള്ള ക്വാണ്ടം ബേസ്ഡ് ആപ്പ്")

st.sidebar.header("🚛 ഫ്ലീറ്റ് വിവരങ്ങൾ")
distance = st.sidebar.slider("യാത്രയുടെ ദൂരം (km)", 10, 500, 150)
cargo_weight = st.sidebar.slider("സാധനങ്ങളുടെ ഭാരം (kg)", 100, 5000, 2000)

base_fuel = (distance * 0.28) + (cargo_weight * 0.0004 * distance)

def fuel_objective(x):
    speed = x[0]
    penalty = 0.00012 * ((speed - 58) ** 2)
    return base_fuel * (1 + penalty)

res = dual_annealing(fuel_objective, bounds=[(40, 90)])
optimal_speed = res.x[0]
optimized_fuel = res.fun

normal_co2 = base_fuel * 2.68
optimized_co2 = optimized_fuel * 2.68
co2_saved = normal_co2 - optimized_co2

st.subheader("📊 കണ്ടെത്തലുകൾ (Results)")
col1, col2, col3 = st.columns(3)
col1.metric("സാധാരണ വേണ്ട ഇന്ധനം", f"{base_fuel:.2f} L")
col2.metric("ക്വാണ്ടം ഒപ്റ്റിമൈസ് ചെയ്ത ഇന്ധനം", f"{optimized_fuel:.2f} L", delta=f"-{(base_fuel - optimized_fuel):.2f} L")
col3.metric("ലാഭിച്ച CO2 എമിഷൻ", f"{co2_saved:.2f} kg")

st.success(f"⚡ **മികച്ച ഡ്രൈവിംഗ് സ്പീഡ്:** വാഹനം **{optimal_speed:.1f} km/h** വേഗതയിൽ ഓടിച്ചാൽ ഏറ്റവും കൂടുതൽ ഇന്ധനം ലാഭിക്കാം!")

st.subheader("🗺️ ഇക്കോ റൂട്ട് മാപ്പ്")
m = folium.Map(location=[10.0, 76.3], zoom_start=9)
folium.PolyLine([[9.9312, 76.2673], [10.1000, 76.3500], [10.5276, 76.2144]], color="green", weight=5).add_to(m)
folium.Marker([9.9312, 76.2673], popup="Start Point").add_to(m)
folium.Marker([10.5276, 76.2144], popup="Destination").add_to(m)
st_folium(m, width=700, height=350)
