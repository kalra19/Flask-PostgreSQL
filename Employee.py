from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/mydatabase'

db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)

class Employee(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    first_name = db.Column(db.String(8))
    last_name = db.Column(db.String(8))

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

class CreateSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name')

result_new_schema = CreateSchema()
results_schema = CreateSchema(many=True)

class find(Resource):

#Below method fetches all the records from Employee table
    def get(self):
        stu_details = Employee.query.all()

        if stu_details:
            output = results_schema.dump(stu_details)
            return jsonify(output)
        else:
            return jsonify({"Message": "No Records Found"})

#Below method inserts a record in Employee table and display the inserted id for same
    def post(self):
        try:
            req_data = request.get_json()
            req_insert = Employee(first_name=req_data['first_name'], last_name=req_data['last_name'])
            db.session.add(req_insert)
            db.session.commit()
            inserted_id = req_insert.id
            return jsonify(
                {
                    "id": inserted_id,
                    "Message": "Record Inserted Successfully"
                }
            )
        except Exception as e:
            return str(e)

#Below method updates the record in Employee table by verifying "id" of Employee
    def put(self):
        req_data = request.get_json()
        searchbyid = req_data['id']
        query_by_id = Employee.query.filter_by(id=searchbyid).first()

        if query_by_id:
            query_by_id.first_name = req_data['first_name']
            query_by_id.last_name = req_data['last_name']
            db.session.commit()
            return jsonify({"Message": "Record Updated Successfully"})
        else:
            return jsonify({"Message": "Employee Doesnot Exist"})

#Below method deletes a record in Empployee table by verifying "id" of Employee
    def delete(self):
        req_data = request.get_json()
        query_by_id = Employee.query.filter_by(id=req_data['id']).first()

        if query_by_id:
            db.session.delete(query_by_id)
            db.session.commit()
            return jsonify({"Message": "Record Deleted Successfully"})
        else:
            return jsonify({"Message": "Employee Doesnot Exist"})

class GetById(Resource):

#Below method fetches the Employee by "id" field
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='args', required=True)
        args = parser.parse_args()

        query_by_id = Employee.query.filter_by(id=args['id']).all()

        if query_by_id:
            output = results_schema.dump(query_by_id)
            return jsonify(output)
        else:
            return jsonify({"Message": "Employee Doesnot Exist"})

api.add_resource(GetById, '/getall')
api.add_resource(find, '/getresult')

if __name__ == "__main__":
    app.run(debug=True)