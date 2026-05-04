import streamlit as st
import pandas as pd
import requests
import random
from geopy.geocoders import Nominatim

# 1. GLOBAL CONFIG
st.set_page_config(page_title="Pulse-Path Global", page_icon="🚑", layout="wide")

st.title("🚑 Pulse-Path: Universal Emergency Navigator")
st.markdown("### *Global Hospital Finder & Traffic Simulator*")
st.markdown("---")

# 2. ANY LOCATION INPUT
user_place = st.text_input("Search any City, Landmark, or Street in the World:", placeholder="e.g. Dubai, Tokyo, or Mumbai")

if st.button("🚨 SEARCH GLOBAL DATABASE"):
    geo = Nominatim(user_agent="PulsePath_Global_App")
    
    with st.spinner(f"Accessing global satellite data for {user_place}..."):
        location = geo.geocode(user_place)
        
        if location:
            # SEARCHING GLOBALLY
            search_url = f"https://nominatim.openstreetmap.org/search?q=hospital+in+{user_place}&format=json&limit=10"
            
            try:
                headers = {'User-Agent': 'GlobalPulseApp/2.0'}
                data = requests.get(search_url, headers=headers).json()

                if data:
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.subheader("🏥 Nearby Medical Facilities")
                        map_points = []
                        for i, place in enumerate(data):
                            name = place.get('display_name').split(',')[0]
                            # Simulate a travel time (Traffic Simulation)
                            traffic_time = random.randint(5, 30)
                            
                            if i == 0:
                                st.success(f"🏆 **RECOMMENDED: {name}**\n\nEstimated Arrival: {traffic_time} mins")
                            else:
                                with st.expander(f"📍 {name}"):
                                    st.write(f"**Full Info:** {place.get('display_name')}")
                                    st.write(f"**Travel Estimate:** {traffic_time} mins")
                            
                            map_points.append({"lat": float(place['lat']), "lon": float(place['lon'])})
                    
                    with col2:
                        st.subheader("📍 Satellite View")
                        st.map(pd.DataFrame(map_points))
                else:
                    st.warning("No hospitals found in this specific area. Try a broader city name.")
            except:
                st.error("Global server busy. Please wait a moment and try again.")
        else:
            st.error("Location not found on the global map. Please check spelling!")

st.markdown("---")
st.caption("System Status: Online | Coverage: 195 Countries | Data: OpenStreetMap")
