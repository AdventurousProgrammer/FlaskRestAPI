from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
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

notes_update_args = reqparse.RequestParser()
notes_update_args.add_argument("name", required=False, type=str, help="Please enter the name of the note")
notes_update_args.add_argument("title", required=False, type=str, help="Please enter the title")
notes_update_args.add_argument("body", required=False, type=str, help="Please enter note body")
# handle put, get, delete request
def abort_exists(note_id):
    if note_id in notes:
        abort(409, message="Note already exists with that id")

def abort_dne(note_id):
    if note_id not in notes:
        abort(404, message='Could not find note')

# serialize fields into JSON format
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'title': fields.String,
    'body': fields.String
}

class Notes(Resource):
    @marshal_with(resource_fields)
    def get(self, note_id):
        print(f'Entering get')
        result = NotesModel.query.filter_by(id=note_id).first() # get one db
        if not result:
            abort(404, message="Could not find note with that id...")
        # instance that has that id
        # how to put json format
        return result

    @marshal_with(resource_fields)
    def put(self, note_id):
        print(f'Entering put')
        args = notes_put_args.parse_args() # getting form data
        print(f'Args = {args}')
        '''
        good way to check if note exists
        to avoid crashing program
        '''
        result = NotesModel.query.filter_by(id=note_id).first()
        print(type(result))
        if result:
            abort(409, 'Note id is already taken...')

        note = NotesModel(id=note_id, name=args['name'], title=args['title'], body=args['body'])
        db.session.add(note)
        db.session.commit() # make permanent additions to database
        return note, 201 # turn note into a dictionary, using

    def delete(self, note_id):
        abort_dne(note_id)
        del notes[note_id]
        return '', 204 # string is not json serializable

    @marshal_with(resource_fields)
    def patch(self, note_id):
        args = notes_update_args.parse_args()
        result = NotesModel.query.filter_by(id=note_id).first()
        if not result:
            abort(404, id='Note id is not found, cannot update')
        if args['name']:
            result.name = args['name']
        if args['title']:
            result.title = args['title']
        if args['body']:
            result.body = args['body']
        #db.session.add(result)
        db.session.commit()
        return result

api.add_resource(Notes, "/note/<int:note_id>") # access point
if __name__ == '__main__':
    app.run(debug=True) # make changes live
