import os
import platform
import psutil


"""Pesquisa as partições NTFS quem o computador tem"""
def partitions(name):
    result = []
    drps = psutil.disk_partitions()
    drives = [dp.device for dp in drps if dp.fstype == 'NTFS']
    for i in drives:
        result.append(findFile(name, i))
        result.append(findDir(name, i))
    return result


"""
Pesquisa pelo arquivo.
term -> termo a ser pesquisado
partition -> partição aonde será pesquisado
"""
def findFile(term, partition):
    search = []
    for root, dirs, files in os.walk(partition):
        for name in files:
            if term in name:
                try:
                    absolute_path = os.path.join(root, name)
                    search.append({
                        'path': absolute_path,
                        'datacriacao': creation_date(absolute_path),
                        'tamanho': get_size(absolute_path),
                        'isFile': True
                    })
                except PermissionError as e:
                    print('Sem permissão neste arquivo!')
                except FileNotFoundError as e:
                    print('Arquivo não encontrado')
                except Exception as e:
                    print('Error desconhecido: ', e)
    if len(search)==0:
        search.append({'error': "Nenhum arquivo encontrado."})
    return search


"""
Pesquisa pelo diretório.
term -> termo a ser pesquisado
partition -> partição aonde será pesquisado
"""
def findDir(term, partition):
    search = []
    for root, dirs, files in os.walk(partition):
        for d in dirs:
            if term in d:
                try:
                    absolute_path = os.path.join(root, d)
                    search.append({
                        'path': absolute_path,
                        'datacriacao': creation_date(absolute_path),
                        'totalarquivos': get_total_arquivos(absolute_path),
                        'isFile': False
                    })
                except PermissionError as e:
                    print("Sem permissão neste arquivo!")
                except FileNotFoundError as e:
                    print("Arquivo não encontrado")
                except Exception as e:
                    print("Error desconhecido: ", e)
    if len(search)==0:
        search.append({'error': "Nenhuma pasta encontrada."})
    return search


"""
Retorna a data de criação do arquivo ou diretório.
path -> caminho absoluto do arquivo ou diretório 
"""
def creation_date(path):
    if platform.system() == 'Windows':
        return os.path.getctime(path)
    else:
        stat = os.stat(path)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime


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
def get_total_arquivos(path):
    list = os.listdir(path)
    return len(list)
