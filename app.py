from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_mail import Mail, Message
from models import Hero, Power, HeroPower, db

# ----------------------
# App Setup
# ----------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///superheroes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

# ----------------------
# Routes
# ----------------------

# -------- GET /heroes --------
@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{"id": h.id, "name": h.name, "super_name": h.super_name} for h in heroes])

# -------- GET /heroes/<id> --------
@app.route("/heroes/<int:id>", methods=["GET"])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict())
    else:
        return jsonify({"error": "Hero not found"}), 404

# -------- POST /heroes --------
@app.route("/heroes", methods=["POST"])
def create_hero():
    data = request.get_json()
    name = data.get("name")
    super_name = data.get("super_name")
    
    if not name or not super_name:
        return jsonify({"errors": ["name and super_name are required"]}), 400
    
    hero = Hero(name=name, super_name=super_name)
    db.session.add(hero)
    db.session.commit()
    
    return jsonify({"id": hero.id, "name": hero.name, "super_name": hero.super_name}), 201

# -------- DELETE /heroes/<id> --------
@app.route("/heroes/<int:id>", methods=["DELETE"])
def delete_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    
    db.session.delete(hero)
    db.session.commit()
    
    return jsonify({"message": "Hero deleted successfully"}), 200

# -------- GET /powers --------
@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    return jsonify([p.to_dict() for p in powers])

# -------- GET /powers/<id> --------
@app.route("/powers/<int:id>", methods=["GET"])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict())
    else:
        return jsonify({"error": "Power not found"}), 404

# -------- PATCH /powers/<id> --------
@app.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    description = data.get("description")

    # Validation
    if not Power.validate_description(description):
        return jsonify({"errors": ["description must be at least 20 characters"]}), 400

    power.description = description
    db.session.commit()
    return jsonify(power.to_dict())

# -------- POST /hero_powers --------
@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get("hero_id")
    power_id = data.get("power_id")
    strength = data.get("strength")

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    errors = []

    if not hero:
        errors.append(f"Hero with id {hero_id} not found")
    if not power:
        errors.append(f"Power with id {power_id} not found")
    if strength not in HeroPower.VALID_STRENGTH:
        errors.append(f"Strength must be one of {HeroPower.VALID_STRENGTH}")

    if errors:
        return jsonify({"errors": errors}), 400

    hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify(hero_power.to_dict()), 201


# Run the App
# ----------------------
if __name__ == "__main__":
    app.run(port=5555, debug=True)
