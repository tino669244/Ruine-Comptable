// Données factices
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("clients-count").textContent = 12;
  document.getElementById("produits-count").textContent = 45;
  document.getElementById("ventes-count").textContent = 23;
  document.getElementById("stocks-count").textContent = 78;

  // Chart.js demo
  const ctx = document.getElementById("salesChart");
  if (ctx) {
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"],
        datasets: [{
          label: "Ventes",
          data: [5, 12, 9, 15, 7, 20],
          backgroundColor: "#27ae60"
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } }
      }
    });
  }
});
