const pesos = new Intl.NumberFormat("es-MX", { style: "currency", currency: "MXN" });
let productos = [];
let clientes = [];

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
  if (nombre === "pedidos") cargarPedidos();
  if (nombre === "facturas") cargarFacturas();
  if (nombre === "clientes") cargarClientes();
}

function texto(valor) {
  const span = document.createElement("span");
  span.textContent = valor ?? "";
  return span.innerHTML;
}

// ---------- Nuevo pedido ----------

function agregarRenglon() {
  const fila = document.createElement("tr");
  fila.innerHTML = `
    <td><select class="sku">${productos.map((p) => `<option value="${p.sku}">${texto(p.descripcion)}</option>`).join("")}</select></td>
    <td><input class="cantidad" type="number" min="1" value="1"></td>
    <td class="num precio"></td>
    <td class="num importe"></td>
    <td><button class="quitar secundario">Quitar</button></td>`;
  fila.querySelector(".quitar").onclick = () => { fila.remove(); recalcular(); };
  fila.querySelectorAll("select, input").forEach((el) => (el.oninput = recalcular));
  document.querySelector("#renglones tbody").appendChild(fila);
  recalcular();
}

function renglonesCapturados() {
  return [...document.querySelectorAll("#renglones tbody tr")].map((fila) => ({
    fila,
    sku: fila.querySelector(".sku").value,
    cantidad: parseInt(fila.querySelector(".cantidad").value, 10) || 0,
  }));
}

// Vista previa: el cálculo que cuenta es el del servidor al guardar.
function recalcular() {
  let subtotal = 0;
  for (const r of renglonesCapturados()) {
    const producto = productos.find((p) => p.sku === r.sku);
    const importe = Math.round(producto.precio * r.cantidad * 100) / 100;
    r.fila.querySelector(".precio").textContent = pesos.format(producto.precio);
    r.fila.querySelector(".importe").textContent = pesos.format(importe);
    subtotal += importe;
  }
  const iva = Math.round(subtotal * 0.16 * 100) / 100;
  document.getElementById("t-subtotal").textContent = pesos.format(subtotal);
  document.getElementById("t-iva").textContent = pesos.format(iva);
  document.getElementById("t-total").textContent = pesos.format(subtotal + iva);
}

function mostrarDatosCliente() {
  const c = clientes.find((x) => x.id == document.getElementById("cliente").value);
  document.getElementById("datos-cliente").textContent = c
    ? `RFC ${c.rfc} · C.P. ${c.codigo_postal} · Uso CFDI ${c.uso_cfdi} · Saldo ${pesos.format(c.saldo)}`
    : "";
}

async function guardarPedido() {
  const mensaje = document.getElementById("mensaje-pedido");
  const renglones = renglonesCapturados()
    .filter((r) => r.cantidad > 0)
    .map(({ sku, cantidad }) => ({ sku, cantidad }));
  try {
    const r = await api("/api/pedidos", {
      method: "POST",
      body: JSON.stringify({ cliente_id: Number(document.getElementById("cliente").value), renglones }),
    });
    mensaje.className = "mensaje ok";
    mensaje.textContent = `Pedido ${r.id} guardado por ${pesos.format(r.total)}`;
    document.querySelector("#renglones tbody").innerHTML = "";
    agregarRenglon();
    await cargarClientes();
  } catch (e) {
    mensaje.className = "mensaje error";
    mensaje.textContent = e.message;
  }
}

// ---------- Listados ----------

async function cargarPedidos() {
  const lista = await api("/api/pedidos");
  document.getElementById("lista-pedidos").innerHTML = lista
    .map((p) => `
      <tr>
        <td>${p.id}</td><td>${texto(p.fecha)}</td><td>${texto(p.razon_social)}</td>
        <td><span class="estado ${p.estado}">${p.estado}</span></td>
        <td class="num">${pesos.format(p.total)}</td>
        <td>${p.estado === "capturado" ? `<button onclick="facturar(${p.id}, this)">Facturar</button>` : ""}</td>
      </tr>`)
    .join("");
}

async function facturar(pedidoId, boton) {
  boton.disabled = true;
  boton.textContent = "Timbrando...";
  try {
    const r = await api(`/api/facturas/desde-pedido/${pedidoId}`, { method: "POST" });
    alert(`Factura timbrada\nUUID ${r.uuid}`);
  } catch (e) {
    alert(`No se pudo timbrar: ${e.message}`);
  }
  cargarPedidos();
}

async function reintentarTimbrado(facturaId, boton) {
  boton.disabled = true;
  boton.textContent = "Timbrando...";
  try {
    await api(`/api/facturas/${facturaId}/timbrar`, { method: "POST" });
  } catch (e) {
    alert(`No se pudo timbrar: ${e.message}`);
  }
  cargarFacturas();
}

async function cancelarFactura(facturaId, boton) {
  const motivo = prompt("Motivo de cancelación (01, 02, 03 o 04):", "02");
  if (motivo === null) return;
  boton.disabled = true;
  try {
    const r = await api(`/api/facturas/${facturaId}/cancelar`, { method: "POST", body: JSON.stringify({ motivo }) });
    alert(`Factura cancelada: ${r.motivo}`);
  } catch (e) {
    alert(`No se pudo cancelar: ${e.message}`);
  }
  cargarFacturas();
}

async function cargarFacturas() {
  const lista = await api("/api/facturas");
  document.getElementById("lista-facturas").innerHTML = lista
    .map((f) => `
      <tr>
        <td>${f.serie}-${f.folio}</td><td>${texto(f.razon_social)}</td><td>${texto(f.rfc)}</td>
        <td class="uuid">${f.uuid || "—"}</td>
        <td><span class="estado ${f.estado}">${f.estado}</span></td>
        <td class="num">${pesos.format(f.total)}</td>
        <td>${f.estado === "pendiente" ? `<button onclick="reintentarTimbrado(${f.id}, this)">Timbrar</button>` : ""}
            ${f.estado === "timbrada" ? `<button class="secundario" onclick="cancelarFactura(${f.id}, this)">Cancelar</button>` : ""}</td>
      </tr>`)
    .join("");
}

async function cargarClientes() {
  clientes = await api("/api/clientes");
  const select = document.getElementById("cliente");
  const elegido = select.value;
  select.innerHTML = clientes.map((c) => `<option value="${c.id}">${texto(c.razon_social)}</option>`).join("");
  if (elegido) select.value = elegido;
  mostrarDatosCliente();
  document.getElementById("lista-clientes").innerHTML = clientes
    .map((c) => `
      <tr><td>${texto(c.rfc)}</td><td>${texto(c.razon_social)}</td><td>${texto(c.codigo_postal)}</td>
      <td>${texto(c.uso_cfdi)}</td><td class="num">${pesos.format(c.saldo)}</td></tr>`)
    .join("");
}

async function guardarCliente(evento) {
  evento.preventDefault();
  const mensaje = document.getElementById("mensaje-cliente");
  const datos = Object.fromEntries(new FormData(evento.target));
  try {
    await api("/api/clientes", { method: "POST", body: JSON.stringify(datos) });
    mensaje.className = "mensaje ok";
    mensaje.textContent = "Cliente guardado";
    evento.target.reset();
    cargarClientes();
  } catch (e) {
    mensaje.className = "mensaje error";
    mensaje.textContent = e.message;
  }
}

// ---------- Arranque ----------

document.querySelectorAll("nav button").forEach((b) => (b.onclick = () => mostrarVista(b.dataset.vista)));
document.getElementById("agregar-renglon").onclick = agregarRenglon;
document.getElementById("guardar-pedido").onclick = guardarPedido;
document.getElementById("cliente").onchange = mostrarDatosCliente;
document.getElementById("form-cliente").onsubmit = guardarCliente;

(async () => {
  productos = await api("/api/productos");
  await cargarClientes();
  agregarRenglon();
})();
