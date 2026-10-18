const pesos = new Intl.NumberFormat("es-MX", { style: "currency", currency: "MXN" });
const ESTADOS = { abierta: "abierta", en_proceso: "en proceso", cerrada: "cerrada" };
let clientes = [];
let equipos = [];
let ordenActual = null;

async function api(ruta, opciones = {}) {
  const resp = await fetch(ruta, {
    headers: { "Content-Type": "application/json" },
    ...opciones,
  });
  const cuerpo = await resp.json().catch(() => ({}));
  if (!resp.ok) throw new Error(cuerpo.detail || `Error ${resp.status}`);
  return cuerpo;
}

function mostrarVista(nombre) {
  document.querySelectorAll(".vista").forEach((v) => v.classList.toggle("activa", v.id === nombre));
  document.querySelectorAll("nav button").forEach((b) => b.classList.toggle("activa", b.dataset.vista === nombre));
  if (nombre === "ordenes") cargarOrdenes();
  if (nombre === "equipos") cargarEquipos();
  if (nombre === "refacciones") cargarRefacciones();
}

function texto(valor) {
  const span = document.createElement("span");
  span.textContent = valor ?? "";
  return span.innerHTML;
}

function avisar(id, ok, contenido) {
  const mensaje = document.getElementById(id);
  mensaje.className = `mensaje ${ok ? "ok" : "error"}`;
  mensaje.textContent = contenido;
}

// ---------- Órdenes ----------

async function cargarOrdenes() {
  const estado = document.getElementById("filtro-estado").value;
  const lista = await api(`/api/ordenes${estado ? `?estado=${estado}` : ""}`);
  document.getElementById("lista-ordenes").innerHTML = lista
    .map((o) => `
      <tr class="seleccionable" onclick="verOrden(${o.id})">
        <td>${o.id}</td><td>${texto(o.fecha_apertura)}</td><td>${texto(o.razon_social)}</td>
        <td>${texto(o.numero_serie)}<br><span class="nota">${texto(o.modelo)}</span></td>
        <td>${o.tipo}</td><td>${texto(o.tecnico) || "—"}</td>
        <td><span class="estado ${o.estado}">${ESTADOS[o.estado] || o.estado}</span></td>
        <td class="num">${o.estado === "cerrada" ? pesos.format(o.total) : "—"}</td>
      </tr>`)
    .join("");
}

async function verOrden(id) {
  ordenActual = await api(`/api/ordenes/${id}`);
  const o = ordenActual;
  document.getElementById("detalle").hidden = false;
  document.getElementById("detalle-titulo").textContent = `Orden ${o.id} · ${o.razon_social}`;
  document.getElementById("detalle-datos").textContent =
    `${o.numero_serie} (${o.tipo_equipo}, ${o.modelo}) en ${o.ubicacion}, ${o.planta} · ` +
    `${o.tipo} · ${ESTADOS[o.estado]} · Falla: ${o.falla_reportada}` +
    (o.diagnostico ? ` · Diagnóstico: ${o.diagnostico}` : "");
  document.getElementById("detalle-refacciones").innerHTML = o.refacciones.length
    ? o.refacciones
        .map((r) => `
          <tr><td>${texto(r.descripcion)}</td><td class="num">${r.cantidad}</td>
          <td class="num">${pesos.format(r.precio)}</td><td class="num">${pesos.format(r.importe)}</td></tr>`)
        .join("")
    : `<tr><td colspan="4" class="nota">Sin refacciones</td></tr>`;
  document.getElementById("acciones").hidden = o.estado === "cerrada";
  document.getElementById("costos").innerHTML = o.estado === "cerrada"
    ? `<dt>Mano de obra (${o.horas_mano_obra} h)</dt><dd>${pesos.format(o.costo_mano_obra)}</dd>
       <dt>Refacciones</dt><dd>${pesos.format(o.costo_refacciones)}</dd>
       <dt>IVA 16%</dt><dd>${pesos.format(o.iva)}</dd>
       <dt>Total</dt><dd>${pesos.format(o.total)}</dd>`
    : "";
  document.getElementById("mensaje-detalle").textContent = "";
}

async function accionSobreOrden(ruta, cuerpo, exito) {
  try {
    await api(`/api/ordenes/${ordenActual.id}/${ruta}`, { method: "POST", body: JSON.stringify(cuerpo) });
    await verOrden(ordenActual.id);
    avisar("mensaje-detalle", true, exito);
    cargarOrdenes();
  } catch (e) {
    avisar("mensaje-detalle", false, e.message);
  }
}

// ---------- Nueva orden ----------

function llenarEquiposDelCliente() {
  const clienteId = Number(document.getElementById("cliente").value);
  document.getElementById("equipo").innerHTML = equipos
    .filter((e) => e.cliente_id === clienteId)
    .map((e) => `<option value="${e.id}">${texto(e.numero_serie)} · ${texto(e.modelo)} · ${texto(e.ubicacion)}</option>`)
    .join("");
}

async function abrirOrden() {
  try {
    const r = await api("/api/ordenes", {
      method: "POST",
      body: JSON.stringify({
        equipo_id: Number(document.getElementById("equipo").value),
        tipo: document.getElementById("tipo-orden").value,
        falla_reportada: document.getElementById("falla").value.trim(),
      }),
    });
    avisar("mensaje-nueva", true, `Orden ${r.id} abierta`);
    document.getElementById("falla").value = "";
  } catch (e) {
    avisar("mensaje-nueva", false, e.message);
  }
}

// ---------- Catálogos ----------

async function cargarEquipos() {
  equipos = await api("/api/equipos");
  document.getElementById("lista-equipos").innerHTML = equipos
    .map((e) => `
      <tr><td>${texto(e.numero_serie)}</td><td>${e.tipo}</td><td>${texto(e.marca)} ${texto(e.modelo)}</td>
      <td>${texto(e.razon_social)}</td><td>${texto(e.ubicacion)}</td><td>${texto(e.fecha_instalacion)}</td></tr>`)
    .join("");
}

async function cargarRefacciones() {
  const lista = await api("/api/refacciones");
  document.getElementById("refaccion").innerHTML = lista
    .map((r) => `<option value="${r.clave}">${texto(r.descripcion)} (${r.existencias} en almacén)</option>`)
    .join("");
  document.getElementById("lista-refacciones").innerHTML = lista
    .map((r) => `
      <tr><td>${texto(r.clave)}</td><td>${texto(r.descripcion)}</td>
      <td class="num">${pesos.format(r.precio)}</td><td class="num">${r.existencias}</td></tr>`)
    .join("");
}

// ---------- Arranque ----------

document.querySelectorAll("nav button").forEach((b) => (b.onclick = () => mostrarVista(b.dataset.vista)));
document.getElementById("filtro-estado").onchange = cargarOrdenes;
document.getElementById("cliente").onchange = llenarEquiposDelCliente;
document.getElementById("abrir-orden").onclick = abrirOrden;
document.getElementById("asignar").onclick = () =>
  accionSobreOrden("asignar", { tecnico_id: Number(document.getElementById("tecnico").value) }, "Técnico asignado");
document.getElementById("agregar-refaccion").onclick = async () => {
  await accionSobreOrden(
    "refacciones",
    { clave: document.getElementById("refaccion").value, cantidad: Number(document.getElementById("cantidad-refaccion").value) },
    "Refacción agregada",
  );
  cargarRefacciones();
};
document.getElementById("cerrar").onclick = () =>
  accionSobreOrden(
    "cerrar",
    { diagnostico: document.getElementById("diagnostico").value.trim(), horas_mano_obra: Number(document.getElementById("horas").value) },
    "Orden cerrada",
  );

(async () => {
  clientes = await api("/api/clientes");
  document.getElementById("cliente").innerHTML = clientes
    .map((c) => `<option value="${c.id}">${texto(c.razon_social)} · ${texto(c.planta)}</option>`)
    .join("");
  const tecnicos = await api("/api/tecnicos");
  document.getElementById("tecnico").innerHTML = tecnicos
    .map((t) => `<option value="${t.id}">${texto(t.nombre)} · ${texto(t.especialidad)}</option>`)
    .join("");
  await cargarEquipos();
  llenarEquiposDelCliente();
  await cargarRefacciones();
  await cargarOrdenes();
})();
