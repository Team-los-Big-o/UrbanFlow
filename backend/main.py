
import asyncio
import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.simulacion.red import crear_red, ejecutar_red

from backend.estadisticas.metricas import (
    crear_estadisticas,
    actualizar_estadisticas,
    obtener_estadisticas
)


# ==========================================
# CONFIGURACIÓN DE FASTAPI
# ==========================================

app = FastAPI(
    title="UrbanFlow API",
    description="API para el simulador de tráfico urbano",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==========================================
# ESTADO GLOBAL DE LA SIMULACIÓN
# ==========================================

simulacion = {
    "activa": False,
    "turno": 0,
    "red": crear_red(),
    "estadisticas": crear_estadisticas(),
    "ultimo_resultado": {}
}


# ==========================================
# GENERACIÓN AUTOMÁTICA DE VEHÍCULOS
# ==========================================

def generar_llegadas():
    llegadas = {}

    for nombre in simulacion["red"]:

        llegadas[nombre] = {
            "norte": random.randint(0, 1),
            "sur": random.randint(0, 1),
            "este": random.randint(0, 1),
            "oeste": random.randint(0, 1)
        }

    return llegadas


# ==========================================
# EJECUCIÓN DE UN TURNO
# ==========================================

def avanzar_simulacion():

    llegadas = generar_llegadas()

    resultados = ejecutar_red(
        simulacion["red"],
        llegadas
    )

    simulacion["turno"] += 1

    actualizar_estadisticas(
        simulacion["estadisticas"],
        resultados
    )

    simulacion["ultimo_resultado"] = resultados

    return resultados


# ==========================================
# CICLO AUTOMÁTICO DE SIMULACIÓN
# ==========================================

async def ciclo_simulacion():

    while True:

        if simulacion["activa"]:
            avanzar_simulacion()

        await asyncio.sleep(1)


@app.on_event("startup")
async def iniciar_ciclo():
    asyncio.create_task(ciclo_simulacion())


# ==========================================
# ENDPOINT: INICIAR SIMULACIÓN
# ==========================================

@app.post("/api/iniciar")
def iniciar():

    simulacion["activa"] = True

    return {
        "mensaje": "Simulación iniciada",
        "activa": simulacion["activa"],
        "turno": simulacion["turno"]
    }


# ==========================================
# ENDPOINT: PAUSAR SIMULACIÓN
# ==========================================

@app.post("/api/pausar")
def pausar():

    simulacion["activa"] = False

    return {
        "mensaje": "Simulación pausada",
        "activa": simulacion["activa"],
        "turno": simulacion["turno"]
    }


# ==========================================
# ENDPOINT: REINICIAR SIMULACIÓN
# ==========================================

@app.post("/api/reiniciar")
def reiniciar():

    simulacion["activa"] = False
    simulacion["turno"] = 0
    simulacion["red"] = crear_red()
    simulacion["estadisticas"] = crear_estadisticas()
    simulacion["ultimo_resultado"] = {}

    return {
        "mensaje": "Simulación reiniciada",
        "activa": simulacion["activa"],
        "turno": simulacion["turno"]
    }


# ==========================================
# ENDPOINT: CONSULTAR ESTADO
# ==========================================

@app.get("/api/estado")
def obtener_estado():

    return {
        "activa": simulacion["activa"],
        "turno": simulacion["turno"],
        "red": simulacion["red"],
        "resultados": simulacion["ultimo_resultado"],
        "estadisticas": obtener_estadisticas(
            simulacion["estadisticas"]
        )
    }


# ==========================================
# ENDPOINT PRINCIPAL
# ==========================================

@app.get("/")
def inicio():

    return {
        "mensaje": "UrbanFlow API funcionando",
        "documentacion": "/docs",
        "estado": "/api/estado"
    }
