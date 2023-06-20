// Função para carregar os nomes dos arquivos do diretório do contato atual
function loadFiles() {
  var contact = window.location.pathname.split('/').pop();
  fetch('/get_files?contact=' + encodeURIComponent(contact))
    .then(response => response.json())
    .then(data => {
      // Adicionar os nomes dos arquivos como botões na página
      var chatDiv = document.getElementById("chat");
      chatDiv.innerHTML = "";

      data.files.forEach(function (file) {
        var button = document.createElement("button");
        button.textContent = file.replace(".txt", "");
        button.classList.add("button"); // Adiciona a classe "button" ao botão
        button.addEventListener("click", function () {
          // Chamar a rota '/view_file' para obter o conteúdo do arquivo selecionado
          fetch('/view_file?contact=' + encodeURIComponent(contact) + '&file=' + encodeURIComponent(file))
            .then(() => {
              // Redirecionar para outra página
              window.location.href = '/view_file?contact=' + encodeURIComponent(contact) + '&file=' + encodeURIComponent(file);
            });
        });

        chatDiv.appendChild(button);
      });
    });
}

// Chamar a função para carregar os nomes dos arquivos ao carregar a página
window.addEventListener("load", function () {
  loadFiles();
});

