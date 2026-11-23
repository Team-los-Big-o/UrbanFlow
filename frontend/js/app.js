//Estado de la aplicacion
let estadoActual = null;
let intervaloConsulta = null;
let interseccionSeleccionada = "I22";
let historialCongestion = [];
const MAX_MUESTRAS = 30;

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

function actualizarGraficaCongestion() {
    const grafica = document.getElementById("graficaCongestion");

    if (!estadoActual || !estadoActual.red) return;

    const intersecciones = Object.keys(estadoActual.red).sort();

    const datos = intersecciones.map(nombre => {
        const colas = estadoActual.red[nombre].colas ?? {};

        const totalVehiculos = Object.values(colas)
            .reduce((total, cantidad) => total + cantidad, 0);

        return {
            nombre,
            totalVehiculos
        };
    });

    const maximo = Math.max(...datos.map(d => d.totalVehiculos), 1);

    grafica.innerHTML = datos.map(dato => {
        const porcentaje = (dato.totalVehiculos / maximo) * 100;

        return `
            <div class="fila-grafica">
                <span class="nombre-interseccion">${dato.nombre}</span>

                <div class="fondo-barra">
                    <div
                        class="barra-congestion ${dato.totalVehiculos === maximo && dato.totalVehiculos > 0 ? 'mayor-congestion' : ''}"
                        style="width: ${porcentaje}%">
                    </div>
                </div>

                <span class="valor-congestion">
                    ${dato.totalVehiculos}
                </span>
            </div>
        `;
    }).join("");
}

function registrarHistorialCongestion() {
    if (!estadoActual || !estadoActual.red) return;

    const turno = estadoActual.turno;

    // Evitar registrar dos veces el mismo turno
    if (
        historialCongestion.length > 0 &&
        historialCongestion[historialCongestion.length - 1].turno === turno
    ) {
        return;
    }

    const muestra = {
        turno,
        intersecciones: {}
    };

    Object.keys(estadoActual.red).sort().forEach(nombre => {
        const colas = estadoActual.red[nombre].colas ?? {};

        muestra.intersecciones[nombre] = Object.values(colas)
            .reduce((total, cantidad) => total + Number(cantidad || 0), 0);
    });

    historialCongestion.push(muestra);

    if (historialCongestion.length > MAX_MUESTRAS) {
        historialCongestion.shift();
    }
}

function actualizarGraficaHistorial() {
    const contenedor = document.getElementById("graficaHistorial");

    if (historialCongestion.length === 0) {
        contenedor.innerHTML = "<p>Inicia la simulación para generar el historial.</p>";
        return;
    }

    const colores = [
        "#38bdf8", "#f59e0b", "#22c55e",
        "#a78bfa", "#f472b6", "#eab308",
        "#60a5fa", "#ef4444", "#2dd4bf"
    ];

    const intersecciones = Object.keys(
        historialCongestion[0].intersecciones
    ).sort();

    const ancho = 720;
    const alto = 260;
    const margenIzquierdo = 45;
    const margenDerecho = 15;
    const margenSuperior = 15;
    const margenInferior = 35;

    const anchoGrafica = ancho - margenIzquierdo - margenDerecho;
    const altoGrafica = alto - margenSuperior - margenInferior;

    const maximo = Math.max(
        ...historialCongestion.flatMap(muestra =>
            Object.values(muestra.intersecciones)
        ),
        1
    );

    let svg = `
        <svg viewBox="0 0 ${ancho} ${alto}" 
             xmlns="http://www.w3.org/2000/svg">
    `;

    // Líneas horizontales y valores del eje vertical
    for (let i = 0; i <= 4; i++) {
        const y = margenSuperior + (altoGrafica / 4) * i;
        const valor = Math.round(maximo * (1 - i / 4));

        svg += `
            <line x1="${margenIzquierdo}" y1="${y}"
                  x2="${ancho - margenDerecho}" y2="${y}"
                  stroke="#33445e" stroke-dasharray="4 4"/>

            <text x="${margenIzquierdo - 10}" y="${y + 4}"
                  fill="#8493aa" font-size="11" text-anchor="end">
                ${valor}
            </text>
        `;
    }

    // Dibujar una línea por cada intersección
    intersecciones.forEach((nombre, indice) => {
        const puntos = historialCongestion.map((muestra, posicion) => {
            const x = margenIzquierdo +
                (posicion / Math.max(historialCongestion.length - 1, 1)) *
                anchoGrafica;

            const valor = muestra.intersecciones[nombre];
            const y = margenSuperior +
                (1 - valor / maximo) * altoGrafica;

            return `${x},${y}`;
        });

        svg += `
            <polyline
                points="${puntos.join(" ")}"
                fill="none"
                stroke="${colores[indice % colores.length]}"
                stroke-width="2.5"
                stroke-linecap="round"
                stroke-linejoin="round"
            />
        `;

        // Mostrar un punto en cada medición
        historialCongestion.forEach((muestra, posicion) => {
            const x = margenIzquierdo +
                (posicion / Math.max(historialCongestion.length - 1, 1)) *
                anchoGrafica;

            const y = margenSuperior +
                (1 - muestra.intersecciones[nombre] / maximo) *
                altoGrafica;

            svg += `
                <circle cx="${x}" cy="${y}" r="3"
                        fill="${colores[indice % colores.length]}"/>
            `;
        });
    });

    svg += `
        <text x="${margenIzquierdo}" y="${alto - 8}"
              fill="#8493aa" font-size="11">
            Turno ${historialCongestion[0].turno}
        </text>

        <text x="${ancho - margenDerecho}" y="${alto - 8}"
              fill="#8493aa" font-size="11" text-anchor="end">
            Turno ${historialCongestion[historialCongestion.length - 1].turno}
        </text>
        </svg>
    `;

    const leyenda = intersecciones.map((nombre, indice) => `
        <div class="elemento-leyenda">
            <span class="punto-leyenda"
                  style="background:${colores[indice % colores.length]}">
            </span>
            ${nombre}
        </div>
    `).join("");

    contenedor.innerHTML = `
        ${svg}
        <div class="leyenda-historial">${leyenda}</div>
    `;
}

//Consultar Backend
async function actualizarEstado() {
    try {
        estadoActual = await obtenerEstadoAPI();

        if (estadoActual.activa) {
            registrarHistorialCongestion();
        }

        actualizarGraficaHistorial();
        actualizarIndicador(estadoActual.activa);
        actualizarInterseccion();
        actualizarEstadisticas();
        actualizarTablaCongestion();
        actualizarGraficaCongestion();
    

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
        historialCongestion = [];
        actualizarGraficaHistorial();

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