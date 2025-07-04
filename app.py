from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'clave-secreta-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///producto.db'
db = SQLAlchemy(app)

class Contacto(db.Model):
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(50), nullable=True)
    estado = db.Column(db.String(50), nullable=True)
    clasificacion = db.Column(db.String(50), nullable=True)
    precio = db.Column(db.String(50), nullable=True)

    def serialize(self):
        return {
            'id_producto': self.id_producto,
            'nombre_producto': self.nombre_producto,
            'estado': self.estado,
            'clasificacion': self.clasificacion,
            'precio': self.precio,
        }

with app.app_context():
    db.create_all()

# Rutas existentes para API ...

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Crear nuevo producto
        nombre_producto = request.form.get("nombre_producto")
        estado = request.form.get("estado")
        clasificacion = request.form.get("clasificacion")
        precio = request.form.get("precio")

        nuevo_producto = Contacto(
            nombre_producto=nombre_producto,
            estado=estado,
            clasificacion=clasificacion,
            precio=precio
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        flash("Producto creado correctamente!")
        return redirect(url_for("home"))

    productos = Contacto.query.all()
    return render_template("index.html", productos=productos)


# Ruta para editar producto (desde modal)
@app.route("/editar/<int:id_producto>", methods=["POST"])
def editar_producto(id_producto):
    producto = Contacto.query.get_or_404(id_producto)

    producto.nombre_producto = request.form.get("nombre_producto")
    producto.estado = request.form.get("estado")
    producto.clasificacion = request.form.get("clasificacion")
    producto.precio = request.form.get("precio")

    db.session.commit()
    flash("Producto actualizado correctamente!")
    return redirect(url_for("home"))


# Ruta para eliminar producto
@app.route("/eliminar/<int:id_producto>", methods=["POST"])
def eliminar_producto(id_producto):
    producto = Contacto.query.get_or_404(id_producto)
    db.session.delete(producto)
    db.session.commit()
    flash("Producto eliminado correctamente!")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=False)
