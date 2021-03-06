const FIND_API_URL = "http://127.0.0.1:5000/find";
let passou = 0;

// Verificando se a api está online
setInterval(async() => {
    try {
        let online;
        if (passou == 0)
            online = await fetch("http://127.0.0.1:5000/inicio");
        if (online.status == 200) passou++;
    } catch (err) {
        if (passou == 0) alert("API offline.");
        else passou = 0;
    }
}, 2000);

// Montando a request com os campos informados no formulário.
function montarRequest() {
    let name = $("#inputName").val();
    let case_insensitive = $("#inputCaseInsensitive").is(":checked");
    let exact_name = $("#inputExactName").is(":checked");
    let all_extensions = $("#inputTodasExtensoes").is(":checked");
    let extensions = $("#selectExtensoes").val();
    if (all_extensions) {
        extensions = [];
    }
    if (extensions.indexOf("outras") > -1) {
        extensions.splice(extensions.indexOf("outras"), 1);
        let other_extensions = $("#inputOutrasExtensoes").val();
        other_extensions = other_extensions.replaceAll(/[.  ]/g, "");
        other_extensions = other_extensions.split(",");
        extensions = extensions.concat(other_extensions);
    }
    let modification_date = $("#inputData").val();
    let size = $("#inputTamanho").val();
    let dir = $("#inputDiretorio").is(":checked");

    let request = FIND_API_URL + "?name=" + name + "&case_insensitive=" + case_insensitive + "&exact_name=" + exact_name + "&dir=" + dir;

    if (extensions.length > 0) {
        request += "&extensions=" + extensions;
    }
    if (modification_date != "") {
        if ($("#inputPeriodo").is(":checked")) {
            request += `&modification_date=${modification_date}, ${ $("#inputDataFim").val() }`;
        } else {
            let md = modification_date.split("-")
            let date = new Date(md[0], md[1] - 1, md[2]);
            date.setDate(date.getDate() + 1)
            request += `&modification_date=${modification_date}, ${date.toISOString().split('T')[0]}`;
        }

    }
    if (size != "") {
        request += "&size=" + $("#selectOpcaoTamanho").val() + size;
    }

    return request;
}

// Realizando a pesquisa na API.
function find(request) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        // Verificando se a requisição está completa.
        if (this.readyState == 4) {
            // Se a requisição estiver completa e o status for 200, então ocorreu tudo certo.
            if (this.status == 200) {
                let response = JSON.parse(this.responseText);

                // Utilizadas para separar os arquivos e diretórios.
                let arquivos = "";
                let diretorios = "";

                let item;
                let itemHmtl;
                // Percorrendo os itens recebidos.
                for (let i = 0; i < response.response.length; i++) {
                    item = response.response[i];
                    itemHmtl = `
                            <button type="button" onclick="mostrarInfo('${item.path}', '${item.creation_date}', ${item.isFile}, '${item.size}', '${item.count_files}')" class="list-group-item list-group-item-action text-truncate">
                                ${item.isFile ? '<i class="bi bi-file-earmark me-3"></i>' : '<i class="bi bi-folder me-3"></i>'}
                                ${item.path.substring(item.path.lastIndexOf("/") + 1)}
                            </button>
                        `;

                    // Adicionando o item no html referente ao seu tipo.
                    if (item.isFile) {
                        arquivos += itemHmtl;
                    } else {
                        diretorios += itemHmtl;
                    }
                }

                // Caso tenha pesquisado, ou tenha recebido somente arquivos então os arquivos terão a largura total
                let col = diretorios == "" ? 12 : 5;

                // Montando o html com a resposta.
                let resultado = `
                        <div class="col-12 col-lg-${col}">
                            <h3>Arquivos</h3>
                            <div class="list-group fs-4 col-12">
                                ${arquivos}
                            </div>
                        </div>
                    `;

                if (diretorios != "") {
                    resultado += `
                        <div class="col-12 col-lg-${col}">
                            <h3>Diretórios</h3>
                            <div class="list-group fs-4 col-12">
                                ${diretorios}
                            </div>
                        </div>
                    `;
                }

                // Adicionando o resultado na página.
                $("#resultado").html(resultado);

            } else if (this.status == 404) { // Se a requisição estiver completa e o status for 404, então não foi encontrado nenhum arquivo/diretório.
                let response = JSON.parse(this.responseText);
                $("#resultado").html(`
                    <div class="alert alert-danger text-center col-12" role="alert">
                        ${response.error}
                    </div>
                `);
            } else { // Se a requisição estiver completa, mas o status não for 200 ou 404, então ocorreu algum erro.
                let response = JSON.parse(this.responseText);
                $("#resultado").html(`
                    <div class="alert alert-danger text-center col-12" role="alert">
                        Ocorreu um erro ao realizar a pesquisa.
                    </div>
                `);
            }

            // Ativando a aba de resultado.
            $("#resultado-tab").removeClass('disabled');
            // Alternando para a aba com o resultado.
            $("#resultado-tab").tab('show');

            $("#btnPesquisar").prop("disabled", false);
            $("#btnPesquisar").html("Pesquisar");
        }
    };
    xhttp.open("GET", request, true);
    xhttp.send();
}

// Montando a request e fazendo a pesquisa.
function pesquisar() {
    let request = montarRequest();
    console.log(request);
    find(request);
}

// Configura o modal com as informações do item e o exibe.
function mostrarInfo(path, creation_date, isFile, size, count_files) {
    // Convertendo a data que foi recebida em milisegundos.
    let dataMs = creation_date.toString().replaceAll(".", "");
    if (dataMs.length > 13) {
        dataMs = dataMs.substring(0, 13);
    } else if (dataMs.length < 13) {
        dataMs = dataMs.padEnd(13, '0');
    }
    let dataDeCriacao = new Date(parseInt(dataMs));
    let dd = String(dataDeCriacao.getDate()).padStart(2, '0');
    let mm = String(dataDeCriacao.getMonth() + 1).padStart(2, '0');
    let aaaa = dataDeCriacao.getFullYear();

    // Preenchendo as informações do item.
    let info = `
        <p><span class="fw-bold">Nome: </span>${path.substring(path.lastIndexOf("/") + 1)}</p>
        <p><span class="fw-bold">Caminho absoluto: </span> ${path}</p>`;
    if (isFile) {
        info += `<p><span class="fw-bold">Tamanho: </span> ${parseInt(size)} bytes</p>`;
    } else {
        info += `<p><span class="fw-bold">Quantidade de arquivos: </span> ${count_files}</p>`;
    }
    info += `<p><span class="fw-bold">Data de criação: </span>${dd}/${mm}/${aaaa}</p>
        <p><span class="fw-bold">Tipo: </span>${isFile ? "Arquivo" : "Diretório"}</p>`;

    // Adicionando as informações preenchidas e exibindo o modal.
    $("#informacoesModalBody").html(info);
    $("#informacoesModal").modal('show');
}

$(document).ready(function() {
    // Escondendo o input para extensões informadas pelo usuário.
    $("#inputOutrasExtensoes").closest('div').hide();
    $("#inputDataFim").closest('div').hide();

    // Exibindo o input para extensões informadas pelo usuário caso o usuário selecione para especificar outras extensões.
    $('#selectExtensoes, #inputTodasExtensoes').change(function() {
        let extensions = $("#selectExtensoes").val();
        if (extensions.indexOf("outras") > -1 && !$("#inputTodasExtensoes").is(":checked")) {
            $("#inputOutrasExtensoes").closest('div').fadeIn();
        } else {
            $("#inputOutrasExtensoes").closest('div').fadeOut();
        }
    });

    // Exibindo o select para as extensões caso o usuaário não queira pesquisar todas.
    $('#inputTodasExtensoes').change(function() {
        if ($("#inputTodasExtensoes").is(":checked")) {
            $("#selectExtensoes").closest('div').fadeOut();
        } else {
            $("#selectExtensoes").closest('div').fadeIn();
        }
    });

    // Exibindo o input para data final caso o usuário selecione para pesquisar em um período.
    $("#inputPeriodo").change(function() {
        if ($("#inputPeriodo").is(":checked")) {
            $("#inputDataFim").closest('div').fadeIn();

            $("#inputData").closest('div').addClass('col-lg-6 pe-lg-1');
            $('label[for="inputData"]').text("Data de Modificação (Início do período)");

            $("#inputData").attr("required", true);
            $("#inputDataFim").attr("required", true);
        } else {
            $("#inputDataFim").closest('div').hide();

            $("#inputData").closest('div').removeClass('col-lg-6 pe-lg-1');
            $('label[for="inputData"]').text("Data de Modificação");

            $("#inputData").attr("required", false);
            $("#inputDataFim").attr("required", false);
        }
    });

    // Alterando o minimo da data final para a data inicial.
    $("#inputData").change(function() {
        $("#inputDataFim").attr({ "min": $("#inputData").val() });
    });

    // Interceptando o evento de envio do formulário, fazendo a pesquisa e interrompendo o envio.
    $("#form").submit(function(event) {
        event.preventDefault();
        $("#btnPesquisar").prop("disabled", true);
        $("#btnPesquisar").html(`
            <div class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>`);
        pesquisar();
    });
});