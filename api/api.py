from flask import Flask
from flask_restful import Api, reqparse
from find import check_arguments

app = Flask(__name__)
api = Api(app)

"""
Define a rota e os argumentos nescessários para a API.
"""
@app.route('/find')
def get():
    parser = reqparse.RequestParser()
    """
        Os argumentos abaixo onde o required estiver como "False" não é obrigatório especifica-lo na url
        Exemplo de chamadas:
          1. http://127.0.0.1:5000/find?name=api&extensions=py,txt
          2. http://127.0.0.1:5000/find?name=api&extensions=py,txt&case_insensitive=true
          3. http://127.0.0.1:5000/find?name=api&modification_date=1637193600&dir=false
          4. http://127.0.0.1:5000/find?name=api&size=100250
        """
    parser.add_argument('name', required=True)
    parser.add_argument('case_insensitive', type=verific_arg)
    parser.add_argument('exact_name', type=verific_arg)
    parser.add_argument('extensions')
    parser.add_argument('modification_date')
    parser.add_argument('size')
    parser.add_argument('dir', type=verific_arg)
    args = parser.parse_args()
    if args["name"] == "":
        return {'error': "Forneça um nome de arquivo."}, 400
    print(args["size"])
    output = check_arguments(args)
    return {'response': output}, 200

"""
Expressão lambda que verifica se foi passado um valor booleano.
"""
verific_arg = lambda v: v.lower() == 'true'

if __name__ == '__main__':
    app.run(debug=True)
