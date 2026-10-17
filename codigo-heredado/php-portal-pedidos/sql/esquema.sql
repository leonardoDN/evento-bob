-- esquema portal_pedidos (MySQL 5.0)

CREATE TABLE clientes (
  id_cliente INT NOT NULL AUTO_INCREMENT,
  razon_social VARCHAR(120),
  rfc VARCHAR(13),
  tipo CHAR(3),          -- DIS distribuidor, MOS mostrador, EMP empresa
  nivel TINYINT DEFAULT 0,
  lista TINYINT DEFAULT 1,
  cp VARCHAR(5),
  estado CHAR(2),
  limite_credito DECIMAL(12,2) DEFAULT 0,
  saldo DECIMAL(12,2) DEFAULT 0,
  PRIMARY KEY (id_cliente)
) ENGINE=MyISAM;

CREATE TABLE productos (
  sku VARCHAR(12) NOT NULL,
  descripcion VARCHAR(100),
  categoria CHAR(3),     -- FER ferreteria, ELE electrico, PLO plomeria
  precio_lista DECIMAL(10,2),
  precio_mayoreo DECIMAL(10,2),
  activo TINYINT DEFAULT 1,
  PRIMARY KEY (sku)
) ENGINE=MyISAM;

CREATE TABLE usuarios (
  usuario VARCHAR(20) NOT NULL,
  clave VARCHAR(32),
  id_cliente INT,
  vendedor TINYINT DEFAULT 0,
  PRIMARY KEY (usuario)
) ENGINE=MyISAM;

CREATE TABLE folios (
  serie CHAR(1) NOT NULL,
  ultimo INT DEFAULT 0,
  PRIMARY KEY (serie)
) ENGINE=MyISAM;

CREATE TABLE pedidos (
  folio INT NOT NULL,
  id_cliente INT,
  fecha DATETIME,
  fecha_entrega VARCHAR(10),
  forma_pago CHAR(3),
  subtotal DECIMAL(12,2),
  envio DECIMAL(10,2),
  iva DECIMAL(12,2),
  total DECIMAL(12,2),
  estatus TINYINT DEFAULT 0,
  usuario VARCHAR(20),
  puntos INT DEFAULT 0,
  PRIMARY KEY (folio)
) ENGINE=MyISAM;

CREATE TABLE pedidos_det (
  folio INT NOT NULL,
  sku VARCHAR(12) NOT NULL,
  cantidad INT,
  precio DECIMAL(10,2),
  pct_desc DECIMAL(5,2),
  importe DECIMAL(12,2)
) ENGINE=MyISAM;

INSERT INTO folios VALUES ('P', 10000);
