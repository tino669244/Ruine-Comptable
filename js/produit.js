document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("produitForm");
  const tableBody = document.querySelector("#produitsTable tbody");

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const nom = document.getElementById("nomProduit").value;
    const prix = document.getElementById("prixProduit").value;

    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${nom}</td>
      <td>${prix} Ar</td>
      <td>
        <button class="edit">✏️</button>
        <button class="delete">🗑️</button>
      </td>
    `;
    tableBody.appendChild(row);
    form.reset();
  });

  tableBody.addEventListener("click", (e) => {
    if (e.target.classList.contains("delete")) {
      e.target.closest("tr").remove();
    }
    if (e.target.classList.contains("edit")) {
      const row = e.target.closest("tr");
      document.getElementById("nomProduit").value = row.children[0].textContent;
      document.getElementById("prixProduit").value = row.children[1].textContent.replace(" Ar", "");
      row.remove();
    }
  });
});
