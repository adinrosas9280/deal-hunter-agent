import os
from dotenv import load_dotenv
from tavily import TavilyClient
import anthropic

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def buscar_ofertas(producto):
    print(f"\n🔍 Buscando ofertas de: {producto}...\n")

    # 1. Buscar en la web con Tavily
    resultados = tavily.search(
        query=f"{producto} oferta descuento remate",
        search_depth="advanced",
        max_results=20,
    )

    # Armar texto con los resultados
    texto = ""
    for i, r in enumerate(resultados["results"], 1):
        texto += f"[{i}] {r['title']}\n{r['url']}\n{r['content'][:300]}\n\n"

    # 2. Pasarle los resultados a Claude para que los ordene y limpie
    respuesta = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""Tengo estos resultados de búsqueda para "{producto}".
Muéstrame las 20 mejores ofertas reales de forma clara.
Para cada una pon:
- Número, nombre del producto
- Precio (si aparece)
- Descuento (si aparece)
- Sitio web
- Link

Si no es una oferta real, ignórala.

RESULTADOS:
{texto}"""
        }]
    )

    print(respuesta.content[0].text)


# ── Programa principal ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print(" Deal Hunter — Buscador de ofertas con IA")
    print("Escribe 'salir' para terminar\n")

    while True:
        producto = input("¿Qué quieres buscar? → ").strip()
        if not producto or producto.lower() == "salir":
            print("¡Hasta luego!")
            break
        buscar_ofertas(producto)
