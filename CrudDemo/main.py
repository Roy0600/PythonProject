import marshmallow_sqlalchemy
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Root@localhost:3306/scoreboard'

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Model
class Scoreboard(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    score = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self):
        return f"{self.id}"


db.create_all()


class ScoreboardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Scoreboard
        load_instance = True

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    score = fields.String(required=True)


# Get all users
@app.route('/api/v1/user', methods=['GET'])
def index():
    get_users = Scoreboard.query.all()
    user_schema = ScoreboardSchema(many=True)
    users = user_schema.dump(get_users)
    return make_response(jsonify({"users": users}))


# Get a specific user
@app.route('/api/v1/user/<id>', methods=['GET'])
def get_user_by_id(id):
    get_user = Scoreboard.query.get(id)
    user_schema = ScoreboardSchema()
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))


# Update a specific user
@app.route('/api/v1/user/<id>', methods=['PUT'])
def update_user_by_id(id):
    data = request.get_json()
    get_user = Scoreboard.query.get(id)
    if data.get('name'):
        get_user.name = data['name']
    if data.get('score'):
        get_user.score = data['score']
    db.session.add(get_user)
    db.session.commit()
    user_schema = ScoreboardSchema(only=['id', 'name', 'score'])
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))


# Delete a specific user
@app.route('/api/v1/user/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    get_user = Scoreboard.query.get(id)
    db.session.delete(get_user)
    db.session.commit()
    return make_response("", 204)


# Add a user to the DB
@app.route('/api/v1/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_schema = ScoreboardSchema()
    user = user_schema.load(data)
    result = user_schema.dump(user.create())
    return make_response(jsonify({"user": result}), 200)


# Get the scoreboard of all users
@app.route('/api/v1/scoreboard', methods=['GET'])
def scoreboard():
    get_users = Scoreboard.query.order_by(Scoreboard.score.desc()).all()
    user_schema = ScoreboardSchema(many=True)
    users = user_schema.dump(get_users)
    return make_response(jsonify({"users": users}))


# Get the top # of users
@app.route('/api/v1/scoreboard/<amount>', methods=['GET'])
def scoreboard_top_amount(amount):
    get_users = Scoreboard.query.order_by(Scoreboard.score.desc()).limit(amount).all()
    user_schema = ScoreboardSchema(many=True)
    users = user_schema.dump(get_users)
    return make_response(jsonify({"users": users}))


if __name__ == "__main__":
    app.run(debug=True)
