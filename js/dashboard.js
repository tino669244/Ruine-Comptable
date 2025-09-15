document.addEventListener("DOMContentLoaded", () => {
  // Exemple data (peut être remplacé par loadData de LocalStorage)
  const stats = {
    clients: 12,
    produits: 25,
    ventes: 48,
    stocks: 90,
    ventesMensuelles: [12, 19, 8, 15, 20, 25, 18, 22, 30, 28, 40, 35]
  };

  // Mise à jour des cards
  document.getElementById("totalClients").textContent = stats.clients;
  document.getElementById("totalProduits").textContent = stats.produits;
  document.getElementById("totalVentes").textContent = stats.ventes;
  document.getElementById("totalStocks").textContent = stats.stocks;

  // Création du graphique avec Chart.js
  const ctx = document.getElementById("salesChart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: [
        "Jan", "Fév", "Mar", "Avr", "Mai", "Juin",
        "Juil", "Août", "Sep", "Oct", "Nov", "Déc"
      ],
      datasets: [{
        label: "Ventes mensuelles",
        data: stats.ventesMensuelles,
        backgroundColor: "rgba(0, 170, 255, 0.2)",
        borderColor: "#00aaff",
        borderWidth: 2,
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: { color: "#333" }
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
});
