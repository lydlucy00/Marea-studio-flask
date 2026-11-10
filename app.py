from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones_marea' # Necesario para usar el carrito

PRODUCTOS = [
    {
        "id": 1,
        "nombre": "Expositor de joyas con conchas",
        "precio": 17.99,
        "imagen": "/static/img/producto1.jpg",
        "descripcion": "El mar a tus joyas. Una pieza organizadora y decorativa única, artesanal y eterna."
    },
    {
        "id": 2,
        "nombre": "Espejo artesanal marino",
        "precio": 18.99,
        "imagen": "/static/img/producto2.jpg",
        "descripcion": "Espejo decorativo con detalles de conchas naturales, aportando calidez y diseño moderno a tu hogar."
    },
    {
        "id": 3,
        "nombre": "Joyero de concha nacarada",
        "precio": 14.99,
        "imagen": "/static/img/producto3.jpg",
        "descripcion": "Pequeño joyero decorado a mano con texturas marinas y perlas, ideal para tus piezas más especiales."
    }
]

@app.route("/")
def home():
    return render_template("index.html", productos=PRODUCTOS)

@app.route("/producto/<int:producto_id>")
def producto(producto_id):
    prod = next((p for p in PRODUCTOS if p["id"] == producto_id), None)
    return render_template("producto.html", producto=prod)

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

# --- NUEVAS RUTAS DEL CARRITO ---

@app.route("/carrito")
def carrito():
    if 'carrito' not in session:
        session['carrito'] = []
    
    carrito_items = session['carrito']
    subtotal = sum(item['precio'] for item in carrito_items)
    
    # Calcular el total aplicando el descuento si está guardado en la sesión
    descuento = session.get('descuento', 0)
    total = subtotal * (1 - descuento)
    
    return render_template("carrito.html", 
                           carrito=carrito_items, 
                           subtotal=round(subtotal, 2), 
                           total=round(total, 2), 
                           descuento_aplicado=session.get('codigo_aplicado', None))

@app.route("/aplicar-cupon", methods=["POST"])
def aplicar_cupon():
    codigo = request.form.get("codigo", "").strip()
    
    if codigo == "Flask":
        session['descuento'] = 0.20 # 20% de descuento
        session['codigo_aplicado'] = "Flask (20% OFF)"
    else:
        # Si el código no es válido, podemos recargar o ignorar (o incluso mandar un aviso)
        session.pop('descuento', None)
        session.pop('codigo_aplicado', None)
        
    return redirect(url_for('carrito'))

@app.route("/quitar-cupon")
def quitar_cupon():
    session.pop('descuento', None)
    session.pop('codigo_aplicado', None)
    return redirect(url_for('carrito'))

@app.route("/agregar/<int:producto_id>")
def agregar_al_carrito(producto_id):
    prod = next((p for p in PRODUCTOS if p["id"] == producto_id), None)
    if prod:
        if 'carrito' not in session:
            session['carrito'] = []
        session['carrito'].append(prod)
        session.modified = True
    return redirect(url_for('carrito'))

@app.route("/vaciar")
def vaciar_carrito():
    session.pop('carrito', None)
    return redirect(url_for('carrito'))

@app.route("/procesar-pago", methods=["POST"])
def procesar_pago():
    # Aquí podríamos guardar los datos del formulario de pago si quisiéramos
    return redirect(url_for('pago_exitoso'))

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    pregunta = request.form.get("pregunta", "").lower()
    
    # Respuestas automáticas predefinidas para la tienda
    if "envio" in pregunta or "cuanto tarda" in pregunta or "llega" in pregunta:
         respuesta = "📦 Los envíos de nuestras piezas artesanales tardan entre 3 y 5 días laborables."
    elif "pago" in pregunta or "tarjeta" in pregunta or "pagar" in pregunta:
        respuesta = "💳 Aceptamos tarjetas de crédito/débito a través de nuestra pasarela segura simulada."
    elif "cupon" in pregunta or "descuento" in pregunta:
        respuesta = "✨ ¡Claro! Puedes usar el código de descuento 'Flask' en tu cesta para obtener un 20% de rebaja."
    elif "contacto" in pregunta or "hablar" in pregunta or "tienda" in pregunta:
        respuesta = "📞 Puedes escribirnos a hola@mareastudio.com o usar nuestro formulario de contacto en el menú superior."
    else:
        respuesta = "👋 ¡Hola! Soy el asistente virtual de Marea Studio. Pregúntame sobre envíos, métodos de pago o códigos de descuento."
        
    return respuesta

if __name__ == "__main__":
    app.run(debug=True)