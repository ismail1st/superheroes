from app import app
from models import db, Hero, Power, HeroPower

with app.app_context():
    Hero.query.delete()
    Power.query.delete()
    HeroPower.query.delete()

    h1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
    h2 = Hero(name="Gwen Stacy", super_name="Spider-Gwen")

    p1 = Power(
        name="super strength",
        description="gives the wielder super-human strengths"
    )
    p2 = Power(
        name="flight",
        description="gives the wielder the ability to fly through the skies"
    )

    db.session.add_all([h1, h2, p1, p2])
    db.session.commit()

    hp1 = HeroPower(
        strength="Strong",
        hero_id=h1.id,
        power_id=p2.id
    )

    db.session.add(hp1)
    db.session.commit()
