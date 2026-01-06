# app.py
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

# SETUP
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///heroes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

#HOME
@app.route("/")
def home():
    return {"message": "Superheroes API running"}

# GET ALL HEROES
@app.route("/heroes")
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([
        {
            "id": h.id,
            "name": h.name,
            "super_name": h.super_name
        } for h in heroes
    ])

#GET HERO BY ID
@app.route("/heroes/<int:id>")
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return {"error": "Hero not found"}, 404

    return {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": [
            {
                "id": hp.id,
                "hero_id": hp.hero_id,
                "power_id": hp.power_id,
                "strength": hp.strength,
                "power": {
                    "id": hp.power.id,
                    "name": hp.power.name,
                    "description": hp.power.description
                }
            } for hp in hero.hero_powers
        ]
    }

# GET ALL POWERS
@app.route("/powers")
def get_powers():
    powers = Power.query.all()
    return jsonify([
        {"id": p.id, "name": p.name, "description": p.description}
        for p in powers
    ])

# GET POWER BY ID 
@app.route("/powers/<int:id>")
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return {"error": "Power not found"}, 404

    return {"id": power.id, "name": power.name, "description": power.description}

#PATCH POWER 
@app.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return {"error": "Power not found"}, 404

    data = request.get_json()
    try:
        power.description = data["description"]
        db.session.commit()
        return {"id": power.id, "name": power.name, "description": power.description}
    except Exception as e:
        return {"errors": [str(e)]}, 400

# POST HERO_POWER
@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    data = request.get_json()
    try:
        hp = HeroPower(
            strength=data["strength"],
            hero_id=data["hero_id"],
            power_id=data["power_id"]
        )
        db.session.add(hp)
        db.session.commit()

        return {
            "id": hp.id,
            "hero_id": hp.hero_id,
            "power_id": hp.power_id,
            "strength": hp.strength,
            "hero": {
                "id": hp.hero.id,
                "name": hp.hero.name,
                "super_name": hp.hero.super_name
            },
            "power": {
                "id": hp.power.id,
                "name": hp.power.name,
                "description": hp.power.description
            }
        }, 201
    except Exception as e:
        return {"errors": [str(e)]}, 400


if __name__ == "__main__":
    app.run(debug=True)
