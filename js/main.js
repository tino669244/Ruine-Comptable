// ========== MAIN.JS GLOBAL SCRIPT ==========

// Highlight active link in navbar
document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll("header nav a");
  const current = window.location.pathname.split("/").pop();

  links.forEach(link => {
    if (link.getAttribute("href") === current) {
      link.classList.add("active");
    }
  });
});

// Simple notification system
function showNotification(message, type = "info") {
  const notif = document.createElement("div");
  notif.className = `notification ${type}`;
  notif.textContent = message;

  document.body.appendChild(notif);

  setTimeout(() => {
    notif.remove();
  }, 3000);
}

// Save & Load Data from LocalStorage
function saveData(key, data) {
  localStorage.setItem(key, JSON.stringify(data));
}

function loadData(key) {
  const data = localStorage.getItem(key);
  return data ? JSON.parse(data) : [];
}

// Example: affichage de la date/heure actuelle
function updateClock() {
  const clock = document.getElementById("clock");
  if (clock) {
    const now = new Date();
    clock.textContent = now.toLocaleString("fr-FR");
  }
}

setInterval(updateClock, 1000);

// ========== UTILISATION ==========
// showNotification("Bienvenue sur Ruine Comptable", "success");
// saveData("clients", [{ nom: "Tino", email: "tino@test.com" }]);
// const clients = loadData("clients");
