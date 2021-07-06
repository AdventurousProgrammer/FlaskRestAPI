from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)

class NotesModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#db.create_all()

notes = {}

notes_put_args = reqparse.RequestParser()
notes_put_args.add_argument("name", required=True, type=str, help="Please enter the name of the note")
notes_put_args.add_argument("title", required=True, type=str, help="Please enter the title")
notes_put_args.add_argument("body", required=True, type=str, help="Please enter note body")
# handle put, get, delete request
def abort_exists(note_id):
    if note_id in notes:
        abort(409, message="Note already exists with that id")

def abort_dne(note_id):
    if note_id not in notes:
        abort(404, message='Could not find note')


class Notes(Resource):
    def get(self, note_id):
        abort_dne(note_id)
        return notes[note_id]             #notes.get(note_id, "Note Does Not Exist")

    def put(self, note_id):
        abort_exists(note_id)
        args = notes_put_args.parse_args()
        notes[note_id] = args
        return notes.get(note_id), 201

    def delete(self, note_id):
        abort_dne(note_id)
        del notes[note_id]
        return '', 204 # string is not json serializable


api.add_resource(Notes, "/note/<int:note_id>") # access point
if __name__ == '__main__':
    app.run(debug=True) # make changes live
