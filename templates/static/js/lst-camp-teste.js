document.addEventListener("DOMContentLoaded", () => {
    const campanhasContainer = document.getElementById("campanhas");

    // Simulando dados do banco de dados
    let campanhas = [
        {
            id: 1,
            nome: "Nome da Campanha",
            dataCriacao: "12/02/2024",
            imagem: "icon/jujutsu.jpg"
        },
        {
            id: 2,
            nome: "Nome da Campanha",
            dataCriacao: "15/03/2024",
            imagem: "simbolo.jpg"
        },
        {
            id: 3,
            nome: "Nome da Campanha",
            dataCriacao: "20/01/2024",
            imagem: "rpg.jpg"
        }
    ];

    // Função para carregar campanhas
    function carregarCampanhas() {
        campanhasContainer.innerHTML = ""; // Limpa antes de adicionar

        campanhas.forEach(campanha => {
            const div = document.createElement("div");
            div.classList.add("campanha");

            // Criando a div da imagem
            const imgDiv = document.createElement("div");
            imgDiv.classList.add("campanha-imagem");

            const img = document.createElement("img");
            img.src = campanha.imagem;
            img.alt = campanha.imagem;

            imgDiv.appendChild(img);

            // Criando a div do conteúdo
            const contentDiv = document.createElement("div");
            contentDiv.classList.add("campanha-conteudo");

            const title = document.createElement("h3");
            title.textContent = campanha.nome;

            const date = document.createElement("p");
            date.textContent = `Data de criação: ${campanha.dataCriacao}`;

            const acessarBtn = document.createElement("button");
            acessarBtn.classList.add("btn-acessar");
            acessarBtn.textContent = "Acessar campanha";

            const deletarBtn = document.createElement("button");
            deletarBtn.classList.add("btn-deletar");
            deletarBtn.textContent = "🗑";
            deletarBtn.onclick = () => deletarCampanha(campanha.id);

            // Adicionando elementos à div de conteúdo
            contentDiv.appendChild(title);
            contentDiv.appendChild(date);
            contentDiv.appendChild(acessarBtn);
            contentDiv.appendChild(deletarBtn);

            // Adicionando tudo ao container da campanha
            div.appendChild(imgDiv);
            div.appendChild(contentDiv);
            campanhasContainer.appendChild(div);
        });
    }

    // Função para deletar campanha
    function deletarCampanha(id) {
        campanhas = campanhas.filter(campanha => campanha.id !== id);
        carregarCampanhas();
    }

    carregarCampanhas(); // Chama a função ao carregar a página
});
