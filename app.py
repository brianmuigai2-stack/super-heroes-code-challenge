import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_mail import Mail, Message
from models import Hero, Power, HeroPower, db

# App Setup
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///superheroes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'brian11613bmw@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'demo-password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME', 'brian11613bmw@gmail.com')

db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)


# Routes

@app.route("/", methods=["GET"])
def index():
    return """
    <h1>Super Heroes API</h1>
    <p>Created by Brian Muigai</p>
    <h2>Available Routes:</h2>
    <ul>
        <li><strong>GET /</strong> - API information and available routes</li>
        <li><strong>GET /heroes</strong> - List all heroes</li>
        <li><strong>GET /heroes/&lt;id&gt;</strong> - Get specific hero with powers</li>
        <li><strong>POST /heroes</strong> - Create a new hero</li>
        <li><strong>DELETE /heroes/&lt;id&gt;</strong> - Delete a hero</li>
        <li><strong>GET /powers</strong> - List all powers</li>
        <li><strong>GET /powers/&lt;id&gt;</strong> - Get specific power</li>
        <li><strong>PATCH /powers/&lt;id&gt;</strong> - Update power description</li>
        <li><strong>POST /hero_powers</strong> - Create hero-power relationship</li>
        <li><strong>POST /send-email</strong> - Send notification email</li>
    </ul>
    """

@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{"id": h.id, "name": h.name, "super_name": h.super_name} for h in heroes])

#GET /heroes/<id>
@app.route("/heroes/<int:id>", methods=["GET"])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict())
    else:
        return jsonify({"error": "Hero not found"}), 404

# POST /heroes
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

#  DELETE /heroes/<id>
@app.route("/heroes/<int:id>", methods=["DELETE"])
def delete_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    
    db.session.delete(hero)
    db.session.commit()
    
    return jsonify({"message": "Hero deleted successfully"}), 200

# GET /powers
@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    return jsonify([p.to_dict() for p in powers])

#  GET /powers/<id>
@app.route("/powers/<int:id>", methods=["GET"])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict())
    else:
        return jsonify({"error": "Power not found"}), 404

# PATCH /powers/<id>
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

# POST /hero_powers
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

# POST /send-email
@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()
    recipient = data.get("recipient")
    subject = data.get("subject", "Super Heroes API Notification")
    body = data.get("body", "Hello from Super Heroes API created by Brian Muigai!")
    
    if not recipient:
        return jsonify({"error": "Recipient email is required"}), 400
    
    # Demo mode - simulate email sending
    if app.config['MAIL_PASSWORD'] == 'demo-password':
        return jsonify({
            "message": "Email sent successfully (demo mode)",
            "details": {
                "to": recipient,
                "subject": subject,
                "body": body
            }
        }), 200
    
    try:
        msg = Message(
            subject=subject,
            recipients=[recipient],
            body=body
        )
        mail.send(msg)
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to send email: {str(e)}"}), 500



if __name__ == "__main__":
    app.run(port=5555, debug=True)
