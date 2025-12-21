from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------------------
# Hero Model
# ----------------------------
class Hero(db.Model):
    __tablename__ = "heroes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    # Relationship to HeroPower
    hero_powers = db.relationship("HeroPower", back_populates="hero", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
            "hero_powers": [hp.to_dict() for hp in self.hero_powers]
        }

# ----------------------------
# Power Model
# ----------------------------
class Power(db.Model):
    __tablename__ = "powers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    # Relationship to HeroPower
    hero_powers = db.relationship("HeroPower", back_populates="power", cascade="all, delete-orphan")

    # Validation method for description
    @staticmethod
    def validate_description(description):
        return description and len(description) >= 20

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

# ----------------------------
# HeroPower Model
# ----------------------------
class HeroPower(db.Model):
    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"), nullable=False)
    strength = db.Column(db.String, nullable=False)

    # Relationships
    hero = db.relationship("Hero", back_populates="hero_powers")
    power = db.relationship("Power", back_populates="hero_powers")

    # Allowed strength values
    VALID_STRENGTH = ["Strong", "Weak", "Average"]

    # Validation method
    def is_valid_strength(self):
        return self.strength in self.VALID_STRENGTH

    def to_dict(self):
        return {
            "id": self.id,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "strength": self.strength,
            "hero": {
                "id": self.hero.id,
                "name": self.hero.name,
                "super_name": self.hero.super_name
            },
            "power": {
                "id": self.power.id,
                "name": self.power.name,
                "description": self.power.description
            }
        }
