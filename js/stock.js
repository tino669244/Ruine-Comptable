document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("stockForm");
  const tableBody = document.querySelector("#stocksTable tbody");

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const produit = document.getElementById("produitStock").value;
    const quantite = document.getElementById("quantiteStock").value;

    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${produit}</td>
      <td>${quantite}</td>
      <td><button class="delete">🗑️</button></td>
    `;
    tableBody.appendChild(row);
    form.reset();
  });

  tableBody.addEventListener("click", (e) => {
    if (e.target.classList.contains("delete")) {
      e.target.closest("tr").remove();
    }
  });
});
