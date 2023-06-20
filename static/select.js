// Função para obter a lista de usuários
function getUsers() {
    fetch('/get_users')
        .then(response => response.json())
        .then(data => {
            // Limpar a lista de contatos
            var contactsDiv = document.getElementById("contacts");
            contactsDiv.innerHTML = "";

            // Adicionar cada usuário como um contato
            data.users.forEach(function (user) {
                var newContactDiv = document.createElement("div");
                newContactDiv.classList.add("contact");
                newContactDiv.setAttribute("onclick", "selecionarContato('" + user.username + "')");

                var newContactImg = document.createElement("img");
                newContactImg.src = "/static/fotos/" + user.profile_pic;
                newContactImg.alt = user.username;

                var newContactSpan = document.createElement("span");
                newContactSpan.textContent = user.username;

                newContactDiv.appendChild(newContactImg);
                newContactDiv.appendChild(newContactSpan);

                contactsDiv.appendChild(newContactDiv);
            });
        });
}

// Função para redirecionar para a página do contato
function selecionarContato(contato) {
    // Redirecionar para a página do contato
    window.location.href = '/contact/' + encodeURIComponent(contato);
}


// Chamar a função para obter a lista de usuários ao carregar a página
window.addEventListener("load", getUsers);

