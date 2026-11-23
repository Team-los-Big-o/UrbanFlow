//Estado de la aplicacion
let estadoActual = null;
let intervaloConsulta = null;
let interseccionSeleccionada = "I22";

//Elementos de la pagina
const estadoSimulacion = document.getElementById("estadoSimulacion");
const indicador = document.querySelector(".indicador");
const btnIniciar = document.getElementById("btnIniciar");
const btnPausar = document.getElementById("btnPausar");
const btnReiniciar = document.getElementById("btnReiniciar");

const selectorInterseccion = document.getElementById("seleccionarInterseccion");

const listaAlertas = document.getElementById("listaAlertas");
const listaPrioritarios = document.getElementById("listaPrioritarios");

//Actualizar estado visual
function actualizarIndicador(activa) {
    if (activa) {
        estadoSimulacion.textContent = "Simulación en ejecución";
        indicador.style.backgroundColor = "#22c55e";
        indicador.style.boxShadow = "0 0 10px #22c55e";
    } else {
        estadoSimulacion.textContent = "Simulación pausada";
        indicador.style.backgroundColor = "#eab308";
        indicador.style.boxShadow = "0 0 10px #eab308";
    }
}

//Actualizar interseccion
function actualizarInterseccion() {
    if (!estadoActual || !estadoActual.red) return;

    const interseccion = estadoActual.red[interseccionSeleccionada];

    if (!interseccion) return;

    const colas = interseccion.colas;

    // Conteo de vehículos por dirección
    document.getElementById("vehiculosNorte").textContent = colas.norte;
    document.getElementById("vehiculosSur").textContent = colas.sur;
    document.getElementById("vehiculosEste").textContent = colas.este;
    document.getElementById("vehiculosOeste").textContent = colas.oeste;

    // Identificador de la intersección
    document.getElementById("numeroInterseccion").textContent =
        interseccionSeleccionada;

    // Total de vehículos de toda la red
    let total = 0;

    Object.values(estadoActual.red).forEach(cruce => {
        Object.values(cruce.colas).forEach(cantidad => {
            total += cantidad;
        });
    });

    document.getElementById("totalVehiculos").textContent = total;

    //Dirección del semáforo en verde
    const direccionVerde = interseccion.estado_semaforo.direccion;

    document.getElementById("direccionVerde").textContent =
        direccionVerde ? direccionVerde.toUpperCase() : "--";

    //Actualizar luces de los semáforos
    const direcciones = ["norte", "sur", "este", "oeste"];

    direcciones.forEach(direccion => {
        const semaforo = document.getElementById(
            "semaforo" + direccion.charAt(0).toUpperCase() + direccion.slice(1)
        );

        const luzRoja = semaforo.querySelector(".roja");
        const luzAmarilla = semaforo.querySelector(".amarilla");
        const luzVerde = semaforo.querySelector(".verde");

        luzRoja.classList.remove("activa");
        luzAmarilla.classList.remove("activa");
        luzVerde.classList.remove("activa");

        if (direccionVerde === direccion) {
            luzVerde.classList.add("activa");
        } else {
            luzRoja.classList.add("activa");
        }
    });
}

//Actualizar estadísticas generales de la red
function actualizarEstadisticas() {
    if (!estadoActual || !estadoActual.estadisticas) return;

    const estadisticas = estadoActual.estadisticas;

    document.getElementById("totalTurnos").textContent =
        estadisticas.turnos;

    document.getElementById("vehiculosAtendidos").textContent =
        estadisticas.vehiculos_atendidos;

    document.getElementById("vehiculosTransferidos").textContent =
        estadisticas.vehiculos_transferidos;

    document.getElementById("vehiculosSalieron").textContent =
        estadisticas.vehiculos_salieron;

    document.getElementById("tiempoEspera").textContent =
        `${estadisticas.tiempo_espera_promedio} s`;

    document.getElementById("colaMaxima").textContent =
        estadisticas.cola_maxima;

    document.getElementById("mayorCongestion").textContent =
        estadisticas.interseccion_mayor_congestion ?? "--";
}

function actualizarTablaCongestion() {
    const tabla = document.getElementById("tablaCongestion");

    if (!estadoActual || !estadoActual.red) return;

    const congestion =
        estadoActual.estadisticas?.congestion_por_interseccion ?? {};

    const intersecciones = Object.keys(estadoActual.red).sort();

    tabla.innerHTML = intersecciones.map(nombre => {
        const datos = congestion[nombre] ?? {};

        return `
            <tr>
                <td>${nombre}</td>
                <td>${datos.cola_maxima ?? 0}</td>
                <td>${Number(datos.cola_promedio ?? 0).toFixed(2)}</td>
            </tr>
        `;
    }).join("");
}

//Consultar Backend
async function actualizarEstado() {
    try {
        estadoActual = await obtenerEstadoAPI();

        actualizarIndicador(estadoActual.activa);
        actualizarInterseccion();
        actualizarEstadisticas();
        actualizarTablaCongestion();

    } catch (error) {
        console.error("No se pudo actualizar el estado:", error);
        estadoSimulacion.textContent = "Error de conexión con el servidor";
        indicador.style.backgroundColor = "#ef4444";
        indicador.style.boxShadow = "0 0 10px #ef4444";
    }
}


function iniciarConsultaAutomatica() {
    if (intervaloConsulta !== null) return;

    actualizarEstado();

    intervaloConsulta = setInterval(actualizarEstado, 1000);
}

function detenerConsultaAutomatica() {
    if (intervaloConsulta !== null) {
        clearInterval(intervaloConsulta);
        intervaloConsulta = null;
    }
}

//Boton iniciar
btnIniciar.addEventListener("click", async () => {
    try {
        await iniciarSimulacionAPI();

        await actualizarEstado();

        iniciarConsultaAutomatica();

    } catch (error) {
        console.error("Error al iniciar la simulación:", error);
    }
});

//Boton pausar
btnPausar.addEventListener("click", async () => {
    try {
        await pausarSimulacionAPI();

        detenerConsultaAutomatica();

        await actualizarEstado();

    } catch (error) {
        console.error("Error al pausar la simulación:", error);
    }
});

//Boton reiniciar
btnReiniciar.addEventListener("click", async () => {
    try {
        detenerConsultaAutomatica();

        await reiniciarSimulacionAPI();

        limpiarEventos();

        await actualizarEstado();

    } catch (error) {
        console.error("Error al reiniciar la simulación:", error);
    }
});

//Kimpiar eventos
function limpiarEventos() {
    listaAlertas.innerHTML =
        '<p class="mensaje-vacio">No hay alertas registradas.</p>';

    listaPrioritarios.innerHTML =
        '<p class="mensaje-vacio">No hay vehículos prioritarios registrados.</p>';
}

//Cambiar interseccion
selectorInterseccion.addEventListener("change", () => {
    interseccionSeleccionada = selectorInterseccion.value;

    actualizarInterseccion();
});

//Inicializacion
actualizarEstado();