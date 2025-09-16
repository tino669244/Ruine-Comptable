document.addEventListener("DOMContentLoaded", () => {
  // Fake data (azo soloina API/database)
  const stats = {
    clients: 12,
    produits: 34,
    ventes: 18,
    stocks: 90
  };

  // Update cards
  document.getElementById("clientCount").textContent = stats.clients;
  document.getElementById("productCount").textContent = stats.produits;
  document.getElementById("venteCount").textContent = stats.ventes;
  document.getElementById("stockCount").textContent = stats.stocks;

  // Chart.js setup
  const ctx = document.getElementById("salesChart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"],
      datasets: [{
        label: "Ventes",
        data: [5, 9, 7, 12, 15, 20],
        borderColor: "#0d6efd",
        backgroundColor: "rgba(13, 110, 253, 0.2)",
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true }
      }
    }
  });
});
