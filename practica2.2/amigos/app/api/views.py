from flask import request, abort, jsonify
from .. import db, fcm
from . import api
from ..models import Amigo, get_all_devices

@api.route("/amigo/<int:id>")
def get_amigo(id):
    amigo = Amigo.query.get_or_404(id)
    return jsonify(amigo.to_json())

@api.route("/amigo/byName/<name>")
def get_amigo_by_name(name):
    amigo = Amigo.query.filter_by(name = name).first()
    if not amigo:
        abort(404, "No se encuentra ningún amigo con ese nombre")
    return jsonify(amigo.to_json())

@api.route("/amigos")
def list_amigos():
    amigos = Amigo.query.all()
    lista_amigos = [a.to_json() for a in amigos]
    return jsonify(lista_amigos)

@api.route("/amigo/<int:id>", methods=["PUT"])
def edit_amigo(id):
    amigo = Amigo.query.get_or_404(id)

    if not request.json:
        abort(422, "No se ha enviado JSON")

    name = request.json.get("name")
    lati = request.json.get("lati")
    longi = request.json.get("longi")
    device = request.json.get("device")

    if name:
        amigo.name = name
    if lati:
        amigo.lati = lati
    if longi:
        amigo.longi = longi
    if device:
        amigo.device = device

    if name or lati or longi or device:
        db.session.commit()
        try:
            tokens = get_all_devices()
            fcm.notificar_amigos(tokens, "Amigo actualizado")
        except Exception as e:
            print(e)

    return jsonify(amigo.to_json())

@api.route("/amigo/<int:id>", methods=["DELETE"])
def delete_amigo(id):
    amigo = Amigo.query.get_or_404(id)
    db.session.delete(amigo)
    db.session.commit()
    try:
        tokens = get_all_devices()
        fcm.notificar_amigos(tokens, "Amigo borrado")
    except Exception as e:
        print(e)
    return ('', 204)

@api.route("/amigos", methods=["POST"])
def new_amigo():
    if not request.json:
        abort(422, "No se ha enviado JSON")

    name = request.json.get("name")
    if not name:
        abort(422, "El JSON no incluye el campo 'name'")

    amigo = Amigo.query.filter_by(name = name).first()
    if amigo:
        abort(422, "Ya existe un amigo con ese nombre")

    lati = request.json.get("lati", "0")
    longi = request.json.get("longi", "0")
    device = request.json.get("device", "")

    amigo = Amigo(name=name, lati=lati, longi=longi, device=device)
    db.session.add(amigo)
    db.session.commit()

    try:
        tokens = get_all_devices()
        fcm.notificar_amigos(tokens, "Nuevo amigo registrado")
    except Exception as e:
        print(e)

    return jsonify(amigo.to_json()) 
