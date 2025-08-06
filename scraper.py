import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import json
import re

def obtener_precio_desde_aove():
    url = "https://aove.net/precio-aceite-de-oliva-hoy-poolred/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error al acceder a la página: {e}")
        exit(0)

    soup = BeautifulSoup(response.text, "html.parser")
    posibles_precios = soup.find_all("strong")

    print("🟨 DEBUG: Valores encontrados en <strong>:")
    for item in posibles_precios:
        texto = item.get_text(strip=True)
        print(" -", texto)
        match = re.search(r"(\d{1,2}[.,]\d{2})\s?€/kg", texto)
        if match:
            precio = match.group(1).replace(",", ".")
            print(f"🟩 Precio encontrado: {precio}")
            return float(precio)

    print("❌ No se encontró un precio válido en la página.")
    exit(0)

# Ejecutar el scraper
try:
    precio = obtener_precio_desde_aove()
    datos = {
        "precio": precio,
        "fecha": date.today().isoformat(),
        "actualizado": datetime.now().isoformat()
    }

    with open("precio-aceite.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

    print(f"✅ Precio guardado: {precio} €/kg")
    print(f"🕒 Fecha actual: {datos['fecha']}")
    print(f"🕓 Última modificación: {datos['actualizado']}")
except Exception as e:
    print(f"❌ Error general: {e}")
