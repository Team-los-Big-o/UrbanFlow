const valoresIniciales = {
    norte: 12,
    sur: 5,
    este: 18,
    oeste: 7
};

//Estado de la simulacion
let vehiculos = { ...valoresIniciales };
let simulacionActiva = false;
let intervalo = null;

//Elemento donde aparecerán las alertas
const listaAlertas = document.getElementById("listaAlertas");

//Elemento donde aparecerán los vehículos prioritarios
const listaPrioritarios = document.getElementById("listaPrioritarios");

//Registrar un vehículo prioritario en pantalla
function registrarPrioritario(tipo, direccion) {

    const elemento = document.createElement("p");

    elemento.className = "mensaje-prioritario";
    elemento.textContent =
        `${tipo} detectado en dirección ${direccion.toUpperCase()}`;

    //Eliminar el mensaje inicial
    const mensajeVacio = listaPrioritarios.querySelector(".mensaje-vacio");

    if (mensajeVacio) {
        mensajeVacio.remove();
    }

    //Mostrar el más reciente primero
    listaPrioritarios.prepend(elemento);
}

function limpiarEventos() {

    listaAlertas.innerHTML =
        '<p class="mensaje-vacio">No hay alertas registradas.</p>';

    listaPrioritarios.innerHTML =
        '<p class="mensaje-vacio">No hay vehículos prioritarios registrados.</p>';
}

function registrarAlerta(mensaje) {

    const alerta = document.createElement("p");

    alerta.className = "mensaje-alerta";
    alerta.textContent = mensaje;

    //Eliminar el mensaje inicial
    const mensajeVacio = listaAlertas.querySelector(".mensaje-vacio");

    if (mensajeVacio) {
        mensajeVacio.remove();
    }

    //Mostrar la alerta más reciente primero
    listaAlertas.prepend(alerta);
}

//Elementos de la página
const estadoSimulacion = document.getElementById("estadoSimulacion");
const indicador = document.querySelector(".indicador");

const btnIniciar = document.getElementById("btnIniciar");
const btnPausar = document.getElementById("btnPausar");
const btnReiniciar = document.getElementById("btnReiniciar");

function actualizarPantalla() {

    //Mostrar cantidades por dirección
    document.getElementById("vehiculosNorte").textContent = vehiculos.norte;
    document.getElementById("vehiculosSur").textContent = vehiculos.sur;
    document.getElementById("vehiculosEste").textContent = vehiculos.este;
    document.getElementById("vehiculosOeste").textContent = vehiculos.oeste;

    //Calcular total de vehículos
    const total =
        vehiculos.norte +
        vehiculos.sur +
        vehiculos.este +
        vehiculos.oeste;

    document.getElementById("totalVehiculos").textContent = total;

    document.getElementById("numeroInterseccion").textContent = "1";

    //Determinar la dirección con más vehículos
    const direccionVerde = Object.keys(vehiculos).reduce((mayor, direccion) => {
        return vehiculos[direccion] > vehiculos[mayor] ? direccion : mayor;
    });

    document.getElementById("direccionVerde").textContent =
        direccionVerde.toUpperCase();

    //Actualizar los semáforos
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

        if (direccion === direccionVerde) {
            luzVerde.classList.add("activa");
        } else {
            luzRoja.classList.add("activa");
        }
    });
}

function ejecutarTurno() {

    //Simular nuevas llegadas de vehículos
    Object.keys(vehiculos).forEach(direccion => {
        const llegadas = Math.floor(Math.random() * 3);
        vehiculos[direccion] += llegadas;
    });

    //Identificar la dirección con más vehículos
    const direccionVerde = Object.keys(vehiculos).reduce((mayor, direccion) => {
        return vehiculos[direccion] > vehiculos[mayor] ? direccion : mayor;
    });

    //Permitir el paso de hasta 3 vehículos
    const atendidos = Math.min(vehiculos[direccionVerde], 3);

    vehiculos[direccionVerde] -= atendidos;

    //Detectar un posible accidente (5% de probabilidad)
    if (Math.random() < 0.05) {

        const direcciones = ["norte", "sur", "este", "oeste"];

        const direccionAccidente =
            direcciones[Math.floor(Math.random() * direcciones.length)];

        registrarAlerta(
            `¡ACCIDENTE DETECTADO! Se reporta un incidente en dirección ${direccionAccidente.toUpperCase()}.`
        );
    }

    //Detectar un posible vehículo prioritario (8% de probabilidad)
    if (Math.random() < 0.08) {

        const tiposPrioritarios = [
            "Ambulancia",
            "Patrulla",
            "Camión de bomberos"
        ];

        const direcciones = ["norte", "sur", "este", "oeste"];

        const tipo =
            tiposPrioritarios[
                Math.floor(Math.random() * tiposPrioritarios.length)
            ];

        const direccion =
            direcciones[
                Math.floor(Math.random() * direcciones.length)
            ];

        registrarPrioritario(tipo, direccion);
    }

    //Actualizar la interfaz
    actualizarPantalla();
}

//Boton Iniciar
btnIniciar.addEventListener("click", () => {

    if (simulacionActiva) return;

    simulacionActiva = true;

    estadoSimulacion.textContent = "Simulación en ejecución";
    indicador.style.backgroundColor = "#22c55e";
    indicador.style.boxShadow = "0 0 10px #22c55e";

    ejecutarTurno();

    intervalo = setInterval(ejecutarTurno, 2500);
});

//Boton Pausar
btnPausar.addEventListener("click", () => {

    if (!simulacionActiva) return;

    simulacionActiva = false;

    clearInterval(intervalo);
    intervalo = null;

    estadoSimulacion.textContent = "Simulación pausada";
    indicador.style.backgroundColor = "#eab308";
    indicador.style.boxShadow = "0 0 10px #eab308";
});

//Boton Reiniciar
btnReiniciar.addEventListener("click", () => {

    simulacionActiva = false;

    clearInterval(intervalo);
    intervalo = null;

    vehiculos = { ...valoresIniciales };
    limpiarEventos();

    estadoSimulacion.textContent = "Simulación detenida";
    indicador.style.backgroundColor = "#ef4444";
    indicador.style.boxShadow = "0 0 10px #ef4444";

    actualizarPantalla();
});

//Estado Inicial
actualizarPantalla();