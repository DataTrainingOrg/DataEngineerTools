document.getElementById("searchForm").addEventListener("submit", function() {
    document.getElementById("searchButton").style.display = "none";  // Cacher le bouton
    document.getElementById("loading").style.display = "block";  // Afficher le loader
});

// Fonction pour supprimer un produit
function deleteProduct(element) {
    let productDiv = element.closest('.result');
    let asin = productDiv.getAttribute('data-asin');  

    if (productDiv) {
        fetch('/delete_product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ asin: asin })  
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                productDiv.remove();  
            }
        })
        .catch(error => console.error('Erreur de suppression:', error));
    }
}
