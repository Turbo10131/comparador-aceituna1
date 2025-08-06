import requests
from bs4 import BeautifulSoup
from datetime import date
import json

def obtener_precio_desde_aove():
    url = "https://aove.net/precio-aceite-de-oliva-hoy-poolred/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Buscar el primer elemento <strong> que contenga €/kg
    texto = soup.find("strong", string=lambda t: t and "€/kg" in t)
    if texto:
        precio_str = texto.text.replace("€", "").replace(",", ".").replace("/kg", "").strip()
        return float(precio_str)
    else:
        raise ValueError("❌ No se pudo encontrar el precio en la página.")

# Ejecutar
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
    print(f"❌ Error: {e}")
