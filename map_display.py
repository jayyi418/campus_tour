# map_display.py
import folium
from streamlit_folium import st_folium
from place_data import place_database 

def render_map(place_list):
    # 기본 지도 중심은 정문
    default = place_database.get("백양누리", {"lat": 37.56039, "lon": 126.93675})
    m = folium.Map(location=[default["lat"], default["lon"]], zoom_start=16)

    for name in place_list:
        place = place_database.get(name)
        if place:
            folium.Marker(
                location=[place["lat"], place["lon"]],
                popup=f"{name}: {place['desc']}",
                tooltip=name,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

    st_folium(m, width=700, height=500)
