function genererPrenoms() {
  const genre = document.getElementById('genre').value;
  const nombre = document.getElementById('nombre').value;
  window.location.href = `/generer_prenoms?nombre=${nombre}&genre=${genre}`;
}

function genererNoms() {
  const genre = document.getElementById('genre').value;
  const nombre = document.getElementById('nombre').value;
  window.location.href = `/generer_noms?nombre=${nombre}&genre=${genre}`;
}

function genererTout() {
  window.location.href = "/generer_tout";
}