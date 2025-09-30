import pandas as pd
import geojson

# 📂 Configuración
EXCEL_FILE = 'datos_200.xlsx'           # Nombre de tu archivo Excel
OUTPUT_FILE = 'datos_200.geojson'  # Nombre del archivo GeoJSON de salida

# 🏷️ Mapeo de identificadores a categorías
identifier_a_categoria = {
    "PD": "Personas desaparecidas",
    "EM": "Espacios de memoria",
    "MPM": "Madres / CDD",
    "CC": "Centros Clandestinos",
    "ODD": "Organismos de DDHH"
}

# 🔽 Lee el archivo Excel
df = pd.read_excel(EXCEL_FILE)

# ✅ Limpieza básica
df = df.dropna(subset=['Latitude', 'Longitude'])  # Elimina filas sin coordenadas
df = df.fillna('')  # Rellena celdas vacías

# 🌍 Crea la estructura GeoJSON
features = []

for _, row in df.iterrows():
    # Determinar categoría
    categoria = identifier_a_categoria.get(row['identifier'], "Personas desaparecidas")
    
    # Color según categoría
    color = {
        "Personas desaparecidas": "crimson",
        "Espacios de memoria": "blue",
        "Madres / CDD": "gold",
        "Centros Clandestinos": "gray",
        "Organismos de DDHH": "green"
    }.get(categoria, "gray")

    feature = geojson.Feature(
        type="Feature",
        geometry={
            "type": "Point",
            "coordinates": [float(row['Longitude']), float(row['Latitude'])]  # [lng, lat]
        },
        properties={
            "name": row['name'],
            "description": row['description'],  # ✅ Se deja TAL CUAL (incluye {{...}})
            "fecha": "",  # Puedes agregar una columna si tenés fechas
            "foto": "",   # O dejar vacío si usás {{url}} en description
            "categoria": categoria,
            "_umap_options": {
                "color": color,
                "iconClass": "Circle"
            }
        }
    )
    features.append(feature)

# 📦 Crea el FeatureCollection
feature_collection = geojson.FeatureCollection(features)

# 💾 Guarda el archivo
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    geojson.dump(feature_collection, f, ensure_ascii=False, indent=2)

print(f"✅ GeoJSON generado: {OUTPUT_FILE}")
print(f"📌 Cantidad de elementos: {len(features)}")