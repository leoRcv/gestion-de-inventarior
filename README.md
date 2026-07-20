# Sistema de Gestión de Inventario

Backend REST construido con FastAPI y PostgreSQL para administrar un inventario de tienda de electrónica. La API cubre categorías, productos, ventas, movimientos de stock, usuarios, autenticación por JWT y un reporte de cierre de caja.

## Características

- Gestión de categorías y productos.
- Control de stock con movimientos de entrada y salida.
- Registro de ventas con detalle por producto.
- Autenticación con token JWT.
- Protección de rutas administrativas.
- Reporte de cierre de caja del día.

## Tecnologías

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT / OAuth2
- Bcrypt

## Estructura del proyecto

```text
backend/
├── main.py
├── database.py
├── security.py
├── dependencies.py
├── models/
├── repositories/
├── routers/
└── schemas/
```

## Requisitos

- Python 3.10 o superior.
- PostgreSQL.
- Un entorno virtual activo.

## Variables de entorno

El proyecto usa un archivo `.env` en la raíz con estas variables:

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost/inventario_db
SECRET_KEY=una_clave_secreta_larga
```

Si necesitas generar una clave nueva para JWT, puedes usar:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Instalación

1. Activa el entorno virtual.

```powershell
.\.venv\Scripts\Activate.ps1
```

2. Instala las dependencias.

```bash
pip install -r backend/requirements.txt
```

3. Configura la base de datos y ajusta `DATABASE_URL` en `.env`.

## Ejecución

La aplicación se ejecuta desde la carpeta `backend`.

```powershell
cd backend
uvicorn main:app --reload
```

Al iniciar, la app crea automáticamente las tablas definidas en los modelos.

## Módulos principales

- `main.py`: crea la app FastAPI, configura CORS e incluye todos los routers.
- `database.py`: configura la conexión a PostgreSQL.
- `models/`: define las tablas y relaciones.
- `schemas/`: valida entradas y salidas con Pydantic.
- `repositories/`: contiene la lógica de negocio y acceso a datos.
- `routers/`: expone los endpoints HTTP.
- `security.py`: genera y valida hashes de contraseña y tokens JWT.
- `dependencies.py`: protege rutas y valida roles.

## Endpoints

### Autenticación

- `POST /login`: inicia sesión con email y contraseña.

### Usuarios

- `POST /usuarios/`: registra un usuario nuevo.

### Categorías

- `POST /categorias/`: crea una categoría.
- `GET /categorias/`: lista categorías.

### Productos

- `POST /productos/`: crea un producto.
- `GET /productos/`: lista productos activos.
- `GET /productos/{codigo}`: busca un producto por código de barras.
- `GET /productos/buscar/nombre?nombre=...`: busca productos por nombre.
- `GET /productos/reporte/stock-bajo`: devuelve productos con stock bajo.
- `GET /productos/{producto_id}/movimientos`: historial de movimientos de un producto.
- `POST /productos/{producto_id}/ajustar`: ajusta stock manualmente.
- `PUT /productos/{producto_id}`: actualiza un producto.
- `DELETE /productos/{producto_id}`: desactiva un producto.

### Movimientos

- `GET /movimientos/{producto_id}`: historial de movimientos ordenado por fecha descendente.

### Ventas

- `POST /ventas/`: registra una venta con detalle de productos.
- `GET /ventas/`: lista ventas registradas.

### Reportes

- `GET /reportes/cierre-caja`: obtiene el cierre de caja del día.

## Autenticación y roles

El login usa OAuth2 con formulario. En este proyecto, el campo `username` del formulario se utiliza para enviar el correo electrónico.

La ruta `GET /reportes/cierre-caja` está protegida y solo permite usuarios con rol `admin`.

## Flujo de negocio

1. El router recibe la petición.
2. El schema valida los datos.
3. El repository ejecuta la lógica de negocio.
4. SQLAlchemy guarda o consulta la información en PostgreSQL.

## Notas

- Las ventas descuentan stock automáticamente.
- Cada alta o ajuste de stock crea un movimiento de inventario.
- El sistema marca productos como inactivos en lugar de eliminarlos físicamente.

## Sugerencia de uso

Primero crea una categoría, luego un usuario, después autentícate, crea productos y finalmente registra ventas para ver los reportes y movimientos.