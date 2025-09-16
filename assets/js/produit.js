document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("productForm");
  const table = document.getElementById("productTable");

  let products = [];

  function renderProducts() {
    table.innerHTML = "";
    products.forEach((p, index) => {
      const row = `
        <tr>
          <td>${index + 1}</td>
          <td>${p.name}</td>
          <td>${p.price} Ar</td>
          <td>${p.stock}</td>
          <td>${p.category}</td>
          <td>
            <button class="btn btn-sm btn-warning me-1">✏️</button>
            <button class="btn btn-sm btn-danger">🗑️</button>
          </td>
        </tr>
      `;
      table.innerHTML += row;
    });
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const newProduct = {
      name: document.getElementById("productName").value,
      price: document.getElementById("productPrice").value,
      stock: document.getElementById("productStock").value,
      category: document.getElementById("productCategory").value,
    };
    products.push(newProduct);
    renderProducts();
    form.reset();
    bootstrap.Modal.getInstance(document.getElementById("addProductModal")).hide();
  });
});
