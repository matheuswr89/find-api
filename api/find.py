import os
import platform
from datetime import datetime
from stat import S_ISDIR

"""
Checa quais argumentos foram passados e monta o comando para pesquisar.
args -> argumentos fornecidos pelo usuário 
"""


def check_arguments(args):
    name = args['name']
    search_dir = args['dir']
    extensions = args['extensions']
    case_insensitive = args['case_insensitive']
    string = 'find ~'

    if search_dir == True:
        string += ' -type d,f'
    else:
        string += ' -type f'

    if args['size'] != None:
        string += ' -size {0}c'.format(args['size'])

    print(args['exact_name'])
    if args['exact_name'] == False or args['exact_name'] == None:
        name = '*{0}*'.format(name)

    if case_insensitive == True:
        if extensions == None:
            string += ' -iname "{0}"'.format(name)
        elif ',' not in extensions:
            string += ' -iname'
    else:
        if extensions == None:
            string += ' -name "{0}"'.format(name)
        elif ',' not in extensions:
            string += ' -name'

    if extensions != None:
        if ',' in extensions:
            split = extensions.split(',')
            case = ['-iname' if case_insensitive !=
                    None or case_insensitive == True else '-name']
            str_extension = ' \( {0} \{1}.{2}'.format(case[0], name, split[0])
            for i in split:
                if i != split[0]:
                    str_extension += ' -o {0} \{1}.{2}'.format(
                        case[0], name, i)
            string += str_extension + ' \)'
        else:
            string += ' "{0}.{1}"'.format(name, extensions)

    if args['modification_date'] != None:
        if ',' not in args['modification_date']:
            string += ' -newermt {0}'.format(args['modification_date'])
        else:
            split_date = args['modification_date'].split(',')
            string += ' -newermt {0} ! -newermt {1}'.format(
                split_date[0], split_date[1])

    return command_line(string.replace('\n', ''))


"""
Executa o comando.
command -> comando montado na função check_arguments 
"""


def command_line(command):
    json = []
    stream = os.popen(command)
    output = stream.read().split('\n')
    for path in output:
        if path != '':
            json.append({
                'path': path,
                'size' if is_file(path) == True else 'count_files': get_size(path) if is_file(path) == True else get_total_files(path),
                'creation_date': get_creation_date(path),
                'isFile': True if is_file(path) == True else False
            })
    if json == []:
        return 404
    return json


"""
Retorna a data de criação do arquivo ou diretório.
path -> caminho absoluto do arquivo ou diretório 
"""


def get_creation_date(path):
    creation = os.stat(path)
    try:
        return creation.st_birthtime
    except AttributeError:
        return creation.st_mtime


"""
Retorna o tamanho do arquivo.
path -> caminho absoluto do arquivo 
"""


def get_size(path):
    size = os.path.getsize(path)
    if size <= 1000:
        return str(size)+' BYTE'
    elif size <= 1000000:
        return str(size)+' KB'
    elif size <= 1000000000:
        return str(size)+' MB'
    elif size <= 1000000000000:
        return str(size)+' GB'


"""
Retorna a quantidade de arquivos de um diretório.
path -> caminho absoluto do diretório 
"""


def get_total_files(path):
    list = os.listdir(path)
    return len(list)


"""
Verifica se é um arquivo.
path -> caminho absoluto do diretório 
"""


def is_file(path):
    if(S_ISDIR(os.stat(path).st_mode)):
        return False
    return True
