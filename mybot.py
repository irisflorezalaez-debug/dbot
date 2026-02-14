import discord
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Cliente de Groq (Gratuito y rápido)
client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Configuración de Discord
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# --- CONFIGURACIÓN DEL AGENTE CSVA ---
SYSTEM_PROMPT = """
Eres CSVA (Customer Smart View Agent), un agente especializado en Revenue Ops y Customer Success Enterprise SaaS.
Tu objetivo es unificar la visión 360° y ejecutar playbooks autónomos.

REGLAS DE OPERACIÓN:
1. Tono: Neutral, profesional, enfocado en datos y factual.
2. Si detectas Riesgo de Churn (Uso < 50% o NPS bajo): Sugiere el 'Recovery Plan'.
3. Si detectas Oportunidad de Expansión (Uso > 90%): Sugiere 'Upsell Opportunity'.
4. Si es una renovación próxima (120 días): Genera un 'ROI Report'.
5. Siempre menciona el impacto en el ROI (ej. 'Evita churn del 25%').
6. No eres un chatbot de ayuda, eres un analista interno para el CSM.
"""

@bot.event
async def on_ready():
    print(f'### CSVA ONLINE - Monitoreando Revenue Ops como {bot.user} ###')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # El comando para activar el análisis del agente
    if message.content.startswith('$analizar'):
        datos_cuenta = message.content.replace('$analizar', '').strip()
        
        try:
            # Llamada a Groq con el contexto de tu propuesta
            completion = client_groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Analiza esta situación de cuenta y ejecuta playbook: {datos_cuenta}"}
                ]
            )
            
            respuesta = completion.choices[0].message.content
            
            # Formato profesional para el Dashboard de Discord
            embed = discord.Embed(title="📊 CSVA - Alerta de Revenue Ops", color=0x00ff00)
            embed.description = respuesta
            embed.set_footer(text="Guardrails: Human-in-loop activo | ROI Proyectado +900%")
            
            await message.channel.send(embed=embed)
            
        except Exception as e:
            await message.channel.send(f"⚠️ Error en el motor CSVA: {e}")

bot.run(os.getenv("TOKEN"))