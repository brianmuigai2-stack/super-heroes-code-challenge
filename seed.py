from app import app, db
from models import Hero, Power, HeroPower


# Seed Function
def seed_data():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()

        # Create Heroes
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra"),
        ]
        db.session.add_all(heroes)

        # Create Powers
        powers = [
            Power(name="super strength", description="gives the wielder super-human strengths"),
            Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed"),
            Power(name="super human senses", description="allows the wielder to use her senses at a super-human level"),
            Power(name="elasticity", description="can stretch the human body to extreme lengths"),
        ]
        db.session.add_all(powers)
        db.session.commit()

        # Create HeroPowers
        hero_powers = [
            HeroPower(hero_id=1, power_id=2, strength="Strong"),
            HeroPower(hero_id=2, power_id=4, strength="Average"),
            HeroPower(hero_id=3, power_id=1, strength="Weak"),
            HeroPower(hero_id=5, power_id=1, strength="Strong"),
            HeroPower(hero_id=6, power_id=2, strength="Average"),
        ]
        db.session.add_all(hero_powers)
        db.session.commit()

        print("Database seeded successfully!")

# Run Seed
if __name__ == "__main__":
    seed_data()
