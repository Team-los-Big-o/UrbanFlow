const API_URL = "http://127.0.0.1:8000";

async function consultarAPI(ruta, metodo = "GET") {

    try {

        const respuesta = await fetch(`${API_URL}${ruta}`, {
            method: metodo,
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!respuesta.ok) {
            throw new Error(`Error HTTP: ${respuesta.status}`);
        }

        return await respuesta.json();

    } catch (error) {

        console.error("Error al comunicarse con UrbanFlow:", error);
        throw error;

    }
}

//Controles de la Simulación
async function iniciarSimulacionAPI() {
    return await consultarAPI("/api/iniciar", "POST");
}

async function pausarSimulacionAPI() {
    return await consultarAPI("/api/pausar", "POST");
}

async function reiniciarSimulacionAPI() {
    return await consultarAPI("/api/reiniciar", "POST");
}

//Obtener estado de la simulacion
async function obtenerEstadoAPI() {
    return await consultarAPI("/api/estado", "GET");
}