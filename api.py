from flask import Flask
from flask_restful import Resource, Api, reqparse
from find import partitions

app = Flask(__name__)
api = Api(app)


class FindApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        if args["name"]=="":
          return {'error': "Forneça um nome de arquivo."}, 400
        output = partitions(args["name"])
        return {'response': output}, 200


api.add_resource(FindApi, '/find')

if __name__ == '__main__':
    app.run()
