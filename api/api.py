from flask import Flask
from flask_cors import CORS
from flask_restful import Api, reqparse
from find import check_arguments

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/')
def init():
    return {'response': 'Vá até /find?name=[insira um nome]'}


"""
Define a rota e os argumentos nescessários para a API.
"""


@app.route('/find')
def get():
    parser = reqparse.RequestParser()
    """
        Os argumentos abaixo onde o required estiver como "True" é obrigatório especifica-lo na url
        Exemplo de chamadas:
          1. http://127.0.0.1:5000/find?name=api&extensions=py,txt
          2. http://127.0.0.1:5000/find?name=api&extensions=py,txt&case_insensitive=true
          3. http://127.0.0.1:5000/find?name=api&modification_date=1637193600&dir=true
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
    output = check_arguments(args)
    if output != 404:
        return {'response': output}, 200
    else:
        return {'error': 'O arquivo/pasta não pode ser encontrado.'}, 404


"""
Expressão lambda que verifica se foi passado um valor booleano.
"""
def verific_arg(v): return v.lower() == 'true'


if __name__ == '__main__':
    app.run(debug=True)
