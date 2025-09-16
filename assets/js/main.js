// Script de base pour affichage console + actions bouton
document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ Interface Ruine Comptable chargée avec succès !");

  // Gestion des boutons edit/delete
  document.querySelectorAll(".btn-edit").forEach(btn => {
    btn.addEventListener("click", () => {
      alert("✏️ Édition en cours...");
    });
  });

  document.querySelectorAll(".btn-delete").forEach(btn => {
    btn.addEventListener("click", () => {
      if(confirm("⚠️ Voulez-vous vraiment supprimer cet élément ?")) {
        btn.closest("tr").remove();
      }
    });
  });
});
