import requests
from bs4 import BeautifulSoup
from datetime import date
import json
import re

def obtener_precio_desde_aove():
    url = "https://aove.net/precio-aceite-de-oliva-hoy-poolred/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Buscar cualquier <strong> que contenga un número con formato €X,XXX o X,XX €/kg
    posibles_precios = soup.find_all("strong")
    for item in posibles_precios:
        texto = item.get_text(strip=True)
        match = re.search(r"(\d{1,2},\d{2})\s?€/kg", texto)
        if match:
            precio = match.group(1).replace(",", ".")
            return float(precio)

    raise ValueError("No se encontró un precio válido en el sitio AOVE.net")

# Ejecutar y guardar JSON
try:
    precio = obtener_precio_desde_aove()
    datos = {
        "precio": round(precio, 3),
        "fecha": date.today().isoformat()
    }

    with open("precio-aceite.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

    print(f"✔ Precio obtenido: {datos['precio']} €/kg - Fecha: {datos['fecha']}")
except Exception as e:
    print(f"❌ Error al obtener el precio: {e}")
