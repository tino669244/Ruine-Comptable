document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("clientForm");
  const tableBody = document.querySelector("#clientsTable tbody");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const nom = document.getElementById("nomClient").value;
    const email = document.getElementById("emailClient").value;
    const tel = document.getElementById("telClient").value;

    // Créer une nouvelle ligne
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${nom}</td>
      <td>${email}</td>
      <td>${tel}</td>
      <td>
        <button class="edit">✏️</button>
        <button class="delete">🗑️</button>
      </td>
    `;
    tableBody.appendChild(row);

    // Reset form
    form.reset();
  });

  // Gestion des actions Edit / Delete
  tableBody.addEventListener("click", (e) => {
    if (e.target.classList.contains("delete")) {
      e.target.closest("tr").remove();
    }
    if (e.target.classList.contains("edit")) {
      const row = e.target.closest("tr");
      const nom = row.children[0].textContent;
      const email = row.children[1].textContent;
      const tel = row.children[2].textContent;

      document.getElementById("nomClient").value = nom;
      document.getElementById("emailClient").value = email;
      document.getElementById("telClient").value = tel;

      row.remove(); // Supprime la ligne en attendant la mise à jour
    }
  });
});
