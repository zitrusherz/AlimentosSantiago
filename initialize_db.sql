-- Proveedores
CREATE TABLE Proveedores (
    ProveedorID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Contacto TEXT NOT NULL,
    Telefono TEXT NOT NULL
);

-- Platos
CREATE TABLE Platos (
    PlatoID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Precio REAL NOT NULL,
    ProveedorID INTEGER,
    FOREIGN KEY (ProveedorID) REFERENCES Proveedores(ProveedorID) ON DELETE CASCADE
);

-- Clientes
CREATE TABLE Clientes (
    ClienteID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Saldo REAL DEFAULT 0.0
);

-- Pedidos
CREATE TABLE Pedidos (
    PedidoID INTEGER PRIMARY KEY AUTOINCREMENT,
    ClienteID INTEGER,
    PlatoID INTEGER,
    FechaHoraEntrega TEXT NOT NULL,
    Estado TEXT CHECK (Estado IN ('pendiente', 'entregado')) NOT NULL,
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID) ON DELETE CASCADE,
    FOREIGN KEY (PlatoID) REFERENCES Platos(PlatoID) ON DELETE SET NULL
);

-- Repartidores
CREATE TABLE Repartidores (
    RepartidorID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
    Telefono TEXT NOT NULL,
    Rutas TEXT
);

-- Menús
CREATE TABLE Menus (
    MenuID INTEGER PRIMARY KEY AUTOINCREMENT,
    ClienteID INTEGER,
    Fecha TEXT NOT NULL,
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID) ON DELETE CASCADE
);

CREATE TABLE MenuPlatos (
    MenuID INTEGER,
    PlatoID INTEGER,
    PRIMARY KEY (MenuID, PlatoID),
    FOREIGN KEY (MenuID) REFERENCES Menus(MenuID) ON DELETE CASCADE,
    FOREIGN KEY (PlatoID) REFERENCES Platos(PlatoID) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_plato_nombre ON Platos(Nombre);
CREATE INDEX idx_cliente_nombre ON Clientes(Nombre);
CREATE INDEX idx_pedido_fecha ON Pedidos(FechaHoraEntrega);

-- Vistas
CREATE VIEW ResumenPedidos AS
SELECT
    p.PedidoID,
    c.Nombre AS Cliente,
    pl.Nombre AS Plato,
    p.FechaHoraEntrega,
    p.Estado
FROM
    Pedidos p
JOIN
    Clientes c ON p.ClienteID = c.ClienteID
JOIN
    Platos pl ON p.PlatoID = pl.PlatoID;
