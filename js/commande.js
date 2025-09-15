document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("commandeForm");
  const tbody = document.getElementById("commandeItems");
  const addRowBtn = document.getElementById("addRowCommande");
  const grandTotalEl = document.getElementById("grandTotalCommande");

  function updateTotals() {
    let grandTotal = 0;
    tbody.querySelectorAll("tr").forEach(row => {
      const qty = row.querySelector('input[name="quantite[]"]').value || 0;
      const price = row.querySelector('input[name="prix[]"]').value || 0;
      const total = qty * price;
      row.querySelector(".total").textContent = total.toFixed(2);
      grandTotal += total;
    });
    grandTotalEl.textContent = grandTotal.toFixed(2);
  }

  addRowBtn.addEventListener("click", () => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><input type="text" name="produit[]" placeholder="Nom du produit"></td>
      <td><input type="number" name="quantite[]" min="1" value="1"></td>
      <td><input type="number" name="prix[]" step="0.01" value="0"></td>
      <td class="total">0.00</td>
    `;
    tbody.appendChild(row);
  });

  form.addEventListener("input", updateTotals);

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Commande enregistrée !");
  });
});
