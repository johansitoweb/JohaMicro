
-----

# JohaMicro Un Microframework de Python Minimalista

-----

¡Bienvenido a **JohaMicro**\! Este es un microframework de desarrollo web en Python diseñado con la simplicidad y la comprensión en mente. Aunque no está destinado para aplicaciones de producción a gran escala, JohaMicro es una herramienta excelente para entender los principios fundamentales de cómo funcionan los frameworks web, incluyendo el enrutamiento, el manejo de solicitudes y respuestas, la integración de plantillas, la gestión de archivos estáticos y los middlewares.

-----

## 🚀 Características

  * **Enrutamiento Flexible:** Define rutas para tus URL con soporte para parámetros dinámicos (ej. `/users/<id>`).
  * **Manejo de Solicitudes y Respuestas:** Objetos `Request` y `Response` simples para una fácil interacción con los datos HTTP.
  * **Compatibilidad WSGI:** Diseñado para ejecutarse con cualquier servidor WSGI estándar (Gunicorn, Waitress, etc.).
  * **Servicio de Archivos Estáticos:** Configura directorios para servir archivos CSS, JavaScript, imágenes y más.
  * **Integración con Jinja2:** Soporte incorporado para el motor de plantillas Jinja2, permitiéndote generar HTML dinámico.
  * **Middlewares Básicos:** Implementa funciones que pueden procesar solicitudes antes de llegar a tus manejadores de ruta y después de que la respuesta sea generada.
  * **Manejo de Errores Personalizado:** Define tus propias páginas para errores HTTP comunes como 404 (No Encontrado) y 500 (Error Interno del Servidor).
  * **Funciones de Ayuda:** Atajos para respuestas comunes como JSON (`jsonify`) y redirecciones (`redirect`).

-----

## 🛠️ Instalación y Uso

### Prerrequisitos

Necesitarás Python 3.6 o superior.

### Dependencias

JohaMicro depende de `Jinja2` para el renderizado de plantillas.

```bash
pip install jinja2
```

Para ejecutar la aplicación, necesitarás un servidor WSGI. Recomendamos `waitress` para desarrollo:

```bash
pip install waitress
```

### Estructura del Proyecto

Crea la siguiente estructura de carpetas en tu proyecto:

```
your_project/
├── app.py              # Tu aplicación PicoWeb
├── picoweb.py          # El código fuente de PicoWeb
├── templates/          # Directorio para tus plantillas Jinja2
│   ├── index.html
│   ├── error_404.html
│   └── error_500.html
└── static/             # Directorio para tus archivos estáticos
    ├── css/
    │   └── style.css
    └── img/
        └── picoweb_logo.png
```

### Creando tu Aplicación (`app.py`)

```python
# app.py
from picoweb import PicoWeb, jsonify, redirect, Response, render_template

app = PicoWeb()

# --- Configuración Inicial ---
# Configura Jinja2 para cargar plantillas desde el directorio 'templates'
app.setup_templates("templates") 
# Sirve archivos desde la URL /static/ mapeados a la carpeta 'static'
app.static("/static/", "static") 

# --- Middlewares ---
def logger_middleware(request, next_handler, **kwargs):
    """
    Middleware simple para registrar la ruta y el método de cada solicitud.
    """
    print(f"[Middleware LOG] [{request.method}] {request.path}")
    response = next_handler(request, **kwargs) # Llama al siguiente manejador en la cadena
    print(f"[Middleware LOG] [{response.status}] {request.path}")
    return response

app.use_middleware(logger_middleware)

# --- Manejadores de Errores Personalizados ---
@app.errorhandler(404)
def page_not_found(exception=None):
    """
    Manejador para errores 404 (Página no encontrada).
    """
    return render_template("error_404.html", title="Página No Encontrada"), "404 Not Found"

@app.errorhandler(500)
def internal_server_error(exception=None):
    """
    Manejador para errores 500 (Error interno del servidor).
    """
    return render_template("error_500.html", title="Error Interno", exception=exception), "500 Internal Server Error"

# --- Rutas de la Aplicación ---
@app.route("/")
def index(request):
    return render_template("index.html", title="PicoWeb Inicio", heading="¡Bienvenido a PicoWeb!")

@app.route("/saludo/<name>")
def greet(request, name):
    return render_template("index.html", title=f"Hola, {name}", heading=f"¡Hola, {name.capitalize()}!", name=name)

@app.route("/info", methods=['GET'])
def info(request):
    output = f"<h1>Información de la Solicitud</h1>"
    output += f"<p>Método: {request.method}</p>"
    output += f"<p>Ruta: {request.path}</p>"
    output += f"<p>Query String: {request.query_string}</p>"
    return output

@app.route("/submit", methods=['POST'])
def handle_submit(request):
    if request.json:
        return jsonify({"message": "Datos JSON recibidos!", "data": request.json})
    elif request.form:
        return jsonify({"message": "Datos de formulario recibidos!", "data": request.form})
    else:
        return Response(status="400 Bad Request", body="No se encontraron datos en la solicitud.")

@app.route("/api/data", methods=['GET'])
def api_data(request):
    data = {
        "nombre": "PicoWeb API",
        "version": "0.1",
        "items": ["manzana", "banana", "cereza"]
    }
    return jsonify(data)

@app.route("/old-path")
def old_path(request):
    return redirect("/new-path")

@app.route("/new-path")
def new_path(request):
    return "<h1>¡Has sido redirigido a la nueva ruta!</h1>"

@app.route("/trigger-error")
def trigger_error(request):
    """
    Ruta para probar el manejador de error 500.
    """
    raise Exception("¡Este es un error intencional para probar el manejador 500!")

if __name__ == '__main__':
    print("Para ejecutar PicoWeb, usa un servidor WSGI como Waitress o Gunicorn.")
    print("Ejemplo: waitress-serve --listen=*:8000 app:app")
    print("\nLuego, abre tu navegador en http://127.0.0.1:8000/")

```

### Contenido de las Plantillas y Archivos Estáticos

**`templates/index.html`:**

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header>
        <h1>{{ heading }}</h1>
    </header>
    <main>
        <p>¡Bienvenido a nuestro microframework **PicoWeb**!</p>
        <p>Este es un ejemplo de cómo usar plantillas Jinja2 y servir archivos estáticos.</p>
        <p>Tu nombre es: **{{ name | default('Invitado') }}**</p>
        <img src="/static/img/picoweb_logo.png" alt="PicoWeb Logo" style="max-width: 150px; display: block; margin: 20px 0;">
        <p>Prueba las siguientes rutas:</p>
        <ul>
            <li><a href="/saludo/Mundo">/saludo/Mundo</a></li>
            <li><a href="/api/data">/api/data</a></li>
            <li><a href="/non-existent-page">/non-existent-page</a> (para ver el 404)</li>
            <li><a href="/trigger-error">/trigger-error</a> (para ver el 500)</li>
        </ul>
    </main>
    <footer>
        <p>&copy; 2025 PicoWeb</p>
    </footer>
</body>
</html>
```

**`templates/error_404.html`:**

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página No Encontrada</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header>
        <h1>404 - Página No Encontrada</h1>
    </header>
    <main>
        <p>Lo sentimos, la página que estás buscando no existe.</p>
        <p><a href="/">Volver al inicio</a></p>
    </main>
</body>
</html>
```

**`templates/error_500.html`:**

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error Interno del Servidor</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header>
        <h1>500 - Error Interno del Servidor</h1>
    </header>
    <main>
        <p>¡Ups! Algo salió mal de nuestro lado.</p>
        <p>Estamos trabajando para solucionarlo. Por favor, inténtalo de nuevo más tarde.</p>
        {% if exception %}
            <details>
                <summary>Detalles del Error (Solo para depuración)</summary>
                <pre>{{ exception }}</pre>
            </details>
        {% endif %}
        <p><a href="/">Volver al inicio</a></p>
    </main>
</body>
</html>
```

**`static/css/style.css`:**

```css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f4f4f4;
    color: #333;
    text-align: center;
}

header {
    background-color: #333;
    color: #fff;
    padding: 10px 0;
    margin-bottom: 20px;
}

main {
    background-color: #fff;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 800px;
    margin: 0 auto;
}

h1 {
    color: #333;
}

a {
    color: #007bff;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    margin-bottom: 5px;
}

footer {
    margin-top: 30px;
    color: #777;
    font-size: 0.9em;
}

details {
    margin-top: 20px;
    text-align: left;
    background-color: #eee;
    padding: 10px;
    border-radius: 5px;
}

pre {
    white-space: pre-wrap;
    word-wrap: break-word;
}
```

(Para `static/img/picoweb_logo.png`, puedes usar cualquier imagen PNG simple o crear una con un programa de edición de imágenes).

### Ejecutar la Aplicación

Desde el directorio raíz de tu proyecto (`your_project/`), ejecuta el servidor WSGI:

```bash
waitress-serve --listen=*:8000 app:app
```

Abre tu navegador y visita:

  * `http://127.0.0.1:8000/`
  * `http://127.0.0.1:8000/saludo/TuNombre`
  * `http://127.0.0.1:8000/api/data`
  * `http://127.0.0.1:8000/static/css/style.css`
  * `http://127.0.0.1:8000/pagina-que-no-existe` (para probar el 404)
  * `http://127.0.0.1:8000/trigger-error` (para probar el 500)

-----

## 💡 Cómo Funciona PicoWeb

PicoWeb opera como una aplicación **WSGI (Web Server Gateway Interface)**. Esto significa que es un objeto invocable que se comunica con el servidor web (como Waitress).

1.  **`PicoWeb.__call__(environ, start_response)`:** Este método es el punto de entrada principal para cada solicitud HTTP. El servidor WSGI le pasa el diccionario `environ` (con datos de la solicitud) y una función `start_response` (para enviar encabezados).
2.  **`Request` y `Response`:** Se crean objetos `Request` a partir de `environ` para encapsular los datos de la solicitud, y los manejadores de ruta devuelven objetos `Response` que luego se convierten a un formato compatible con WSGI.
3.  **Enrutamiento (`@app.route`)**: El decorador `app.route` registra tus funciones de vista, mapeándolas a patrones de URL. Utiliza **expresiones regulares** para manejar rutas dinámicas como `/users/<id>`.
4.  **Archivos Estáticos (`app.static`)**: Registra directorios que se servirán directamente. Cuando se recibe una solicitud, PicoWeb primero intenta hacer coincidir la URL con una ruta estática.
5.  **Middlewares (`app.use_middleware`)**: Son funciones que se ejecutan antes (y potencialmente después) de que el manejador de ruta principal sea invocado. Permiten añadir lógica transversal como logging, autenticación, etc.
6.  **Plantillas (`app.setup_templates`, `render_template`)**: Configura el entorno Jinja2. La función `render_template` carga y renderiza plantillas HTML, pasando datos para su visualización dinámica.
7.  **Manejo de Errores (`@app.errorhandler`)**: Permite definir funciones personalizadas que se ejecutarán cuando ocurra un error HTTP específico (ej., 404, 500), proporcionando una experiencia de usuario más amigable.

-----

## 🤝 Contribuciones y Mejoras

PicoWeb es un proyecto educativo. Siéntete libre de clonar, modificar y experimentar con él. Algunas ideas para mejorarlo:

  * **Validación de Formularios:** Una forma más robusta de validar datos enviados.
  * **Gestión de Sesiones:** Soporte para sesiones de usuario.
  * **Conexión a Base de Datos:** Integración con ORM como SQLAlchemy.
  * **Controladores de Archivos:** Mejor manejo para subida de archivos.
  * **Manejo de Contexto:** Un sistema de contexto de aplicación/solicitud más sofisticado (similar a Flask's `g` o `current_app`).
  * **Pruebas Unitarias:** Añadir un conjunto de pruebas para el framework.

-----

## 📜 Licencia

Este proyecto está bajo la licencia MIT.

-----