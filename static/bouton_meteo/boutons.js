function showGraph(id) {
  // Masquer tous les graphiques
  const graphs = document.querySelectorAll('.graphique');
  graphs.forEach(graph => {
      graph.style.display = 'none';
  });

  // Afficher le graphique sélectionné
  const selectedGraph = document.getElementById(id);
  if (selectedGraph) {
      selectedGraph.style.display = 'block';
  }

  // Réinitialiser tous les boutons
  const buttons = document.querySelectorAll('#boutons .bouton');
  buttons.forEach(button => {
      button.classList.remove('bouton-actif'); // Supprimer la classe active
  });

  // Ajouter la classe active au bouton cliqué
  const activeButton = document.querySelector(`.bouton[onclick="showGraph('${id}')"]`);
  if (activeButton) {
      activeButton.classList.add('bouton-actif');
  }
}

function toggleMenu() {
  const navLinks = document.getElementById('nav-links');
  navLinks.style.display = (navLinks.style.display === 'flex' || navLinks.style.display === '') ? 'none' : 'flex';
}


