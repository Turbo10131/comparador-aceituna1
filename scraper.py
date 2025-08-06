import json
from datetime import date

# Precio simulado por ahora (luego podemos automatizarlo con scraping real)
precio = 3.687

# Crear archivo JSON con fecha actual
data = {
    "precio": precio,
    "fecha": date.today().isoformat()
}

# Guardar como 'precio-aceite.json'
with open("precio-aceite.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
