document.addEventListener("DOMContentLoaded", () => {
    const notesContainer = document.getElementById("notes-container");
    const addNoteBtn = document.getElementById("add-note-btn");

    let noteCount = 0;

    addNoteBtn.addEventListener("click", () => {
        noteCount++;

        // Criar uma nova nota
        const note = document.createElement("div");
        note.classList.add("note");
        note.innerHTML = `
            <h3>Título da Nota</h3>
            <p>Data de criação: dd/mm/aaaa</p>
            <button class="view-btn">Visualizar Nota</button>
            <button class="edit-btn">Editar Nota</button>
        `;

        notesContainer.appendChild(note);

        // Mover botão de adicionar nota para o lado
        if (noteCount > 0) {
            addNoteBtn.classList.add("move-right");
        }
    });
});
