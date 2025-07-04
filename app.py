from picoweb import PicoWeb, jsonify, redirect, Response, render_template

app = PicoWeb()


app.setup_templates("templates") 
app.static("/static/", "static") 


def logger_middleware(request, next_handler, **kwargs):
    """
    Middleware simple para registrar la ruta y el método de cada solicitud.
    """
    print(f"[{request.method}] {request.path}")
    response = next_handler(request, **kwargs) 
    print(f"[{response.status}] {request.path}")
    return response

app.use_middleware(logger_middleware)


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



@app.route("/")
def index(request):
    """
    Maneja la solicitud para la ruta raíz, usando una plantilla.
    """
    return render_template("index.html", title="PicoWeb Inicio", heading="¡Bienvenido a PicoWeb!")

@app.route("/saludo/<name>")
def greet(request, name):
    """
    Maneja una ruta dinámica con un parámetro 'name', usando una plantilla.
    """
    return render_template("index.html", title=f"Hola, {name}", heading=f"¡Hola, {name.capitalize()}!", name=name)

@app.route("/info", methods=['GET'])
def info(request):
    """
    Muestra información básica de la solicitud.
    """
    output = f"<h1>Información de la Solicitud</h1>"
    output += f"<p>Método: {request.method}</p>"
    output += f"<p>Ruta: {request.path}</p>"
    output += f"<p>Query String: {request.query_string}</p>"
    return output

@app.route("/submit", methods=['POST'])
def handle_submit(request):
    """
    Maneja solicitudes POST y procesa datos de formulario o JSON.
    """
    if request.json:
        return jsonify({"message": "Datos JSON recibidos!", "data": request.json})
    elif request.form:
        return jsonify({"message": "Datos de formulario recibidos!", "data": request.form})
    else:
        return Response(status="400 Bad Request", body="No se encontraron datos en la solicitud.")

@app.route("/api/data", methods=['GET'])
def api_data(request):
    """
    Devuelve datos en formato JSON.
    """
    data = {
        "nombre": "PicoWeb API",
        "version": "0.1",
        "items": ["manzana", "banana", "cereza"]
    }
    return jsonify(data)

@app.route("/old-path")
def old_path(request):
    """
    Ejemplo de redirección.
    """
    return redirect("/new-path")

@app.route("/new-path")
def new_path(request):
    """
    Ruta a la que se redirige.
    """
    return "<h1>¡Has sido redirigido a la nueva ruta!</h1>"

@app.route("/trigger-error")
def trigger_error(request):
    """
    Ruta para probar el manejador de error 500.
    """
    raise Exception("¡Este es un error intencional para probar el manejador 500!")


if __name__ == '__main__':
    print("Para ejecutar PicoWeb, usa un servidor WSGI como Waitress o Gunicorn.")
    print("Asegúrate de haber instalado 'jinja2': pip install jinja2")
    print("Por ejemplo:")
    print("waitress-serve --listen=*:8000 app:app")
    print("\nLuego, abre tu navegador en http://127.0.0.1:8000/")