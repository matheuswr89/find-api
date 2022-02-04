# Find API

API RESTful JSON para capturar e retornar a saída do comando Linux find . O programa find possibilita realizar 1 buscas por arquivos e diretórios por meio de diversos filtros, como nome, extensão, tipo e tamanho.

Site online: https://matheuswr89.github.io/find-api/index.html

<p>A api tem os seguintes recursos:</p>
    <ul>
      <li>Buscar arquivos por nome:
        <ul>
          <li>Case sensitive</li>
          <li>Case insensitive</li>
          <li>Nome exato</li>
          <li>Parte do nome</li>
        </ul>
      </li>
      <li>Buscar arquivos por extensão:
        <ul>
          <li>Lista de principais extensões para o usuário selecionar</li>
          <li>Possibilidade do usuário informar uma extensão que não faz parte da lista</li>
        </ul>
      </li>
      <li>Buscar arquivos por data de modificação</li>
      <li>Buscar arquivos por tamanho</li>
      <li>Buscar diretório</li>
      <li>Em relação à listagem dos resultados encontrados pela busca, quando o usuário clicar
        em um arquivo ou diretório, é ser exibido:
        <ul>
          <li>Nome, caminho absoluto, tamanho e data de criação do arquivo</li>
          <li>Nome, caminho absoluto, quantidade de arquivos e data de criação do diretório</li>
        </ul>
      </li>
    </ul>

# Como usar

1. Baixe o repositório.

2. Descompacte o arquivo e vá na pasta `api` e execute o comando para instalar as dependências: `pip3 install -r requeriments.txt`

3. Ainda na pasta `api` execute o comando para iniciar a api: `python3 api.py`

4. Vá até `http://127.0.0.1:5000/find?name=` e teste a API.

5. Entre na pasta `docs` e abra o arquivo `index.html` no navegador ou acesse a url https://matheuswr89.github.io/find-api/index.html para ver o frontend online.

# Video execução da API e frontend

[![Apresentacao](/docs/dist/apresentacao.png)](https://drive.google.com/file/d/11HuDbc-o6bzyJk3XQ5lNteiP6AzFsPgV/view?usp=sharing)

# Video Ailton

[![Video Ailton](/docs/dist/ailton.png)](https://drive.google.com/file/d/1FIhcUWdCSQlAhMVj3WW_LhCaEXbewdkQ/view?usp=sharing)

# Video Giovanne

[![Video Giovanne](/docs/dist/giovanne.png)](https://www.youtube.com/watch?v=DNNQv9u-lh4)

# Video Matheus

[![Video Matheus](/docs/dist/matheus.png)](https://drive.google.com/file/d/10JEw_1De8tBFpoxIvCwX1bficEukBChj/view?usp=sharing)
