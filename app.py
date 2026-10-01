from flask import Flask, jsonify, request

app = Flask(__name__)

datos = [{'id': 1, 'nombre': 'Acetaminofén', 'stock': 120}, {'id': 2, 'nombre': 'Amoxicilina', 'stock': 45}, {'id': 3, 'nombre': 'Loratadina', 'stock': 70}]

@app.get("/")
def inicio():
    return jsonify({
        "servicio": "Farmacia",
        "estado": "activo",
        "recurso": "/medicamentos"
    })

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.get("/medicamentos")
def listar():
    return jsonify(datos), 200

@app.get("/medicamentos/<int:item_id>")
def obtener(item_id):
    item = next((x for x in datos if x["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Registro no encontrado"}), 404
    return jsonify(item), 200

@app.post("/medicamentos")
def crear():
    nuevo = request.get_json(silent=True)
    if not isinstance(nuevo, dict):
        return jsonify({"error": "Se requiere un cuerpo JSON válido"}), 400

    nuevo["id"] = max([x["id"] for x in datos], default=0) + 1
    datos.append(nuevo)
    return jsonify(nuevo), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
