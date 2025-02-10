$(document).ready(function() {
    var timeout = null;
    var priceChart = null; // Stocke l'instance du graphique pour le détruire si besoin

    // Fonction pour afficher les détails du produit
    function showProductDetails(name, imageUrl, price, priceHistoryData) {
        console.log("showProductDetails appelé");

        // ✅ Fermer la popup précédente avant d'afficher la nouvelle avec un délai
        $('#product-popup').fadeOut(500, function() {  // Délai de 500ms pour fermer la popup
            // Supprimer l'ancien graphique s'il existe
            if (priceChart !== null) {
                console.log("Popup fermé");
                priceChart.destroy();
                priceChart = null;
                console.log("Graphique supprimé lors de la fermeture de la popup");
            }

            // Mettre à jour les informations de la popup
            $('#popup-name').text(name);
            $('#popup-image').attr('src', imageUrl);
            $('#price-large').text(price);
            $('#popup-price').text(price);

            console.log("priceHistoryData:", priceHistoryData);

            // ✅ Vérifier si priceHistoryData est valide
            if (priceHistoryData && Array.isArray(priceHistoryData) && priceHistoryData.length > 0) {
                console.log("Données de priceHistoryData valides");

                var timestamps = priceHistoryData.map(function(item) {
                    return new Date(item.timestamp).toLocaleString();
                });

                var prices = priceHistoryData.map(function(item) {
                    return item.price;
                });

                console.log("Timestamps:", timestamps);
                console.log("Prices:", prices);

                var ctx = document.getElementById('price-history-chart').getContext('2d');

                // ✅ Créer un nouveau graphique après suppression de l'ancien
                priceChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: timestamps,
                        datasets: [{
                            label: 'Historique des prix',
                            data: prices,
                            borderColor: 'rgba(255, 99, 132, 1)',
                            fill: false,
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: 'Date'
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Prix'
                                }
                            }
                        }
                    }
                });
            } else {
                console.log("Erreur : priceHistoryData est vide ou non valide.");
            }

            // Afficher la popup après un délai
            setTimeout(function() {
                $('#product-popup').fadeIn(500); // Délai de 500ms pour afficher la popup
            }, 300);  // Retard de 300ms avant d'afficher
        });
    }

    // ✅ Gestion de la recherche avec un délai pour éviter trop de requêtes
    $('#search-input').on('input', function() {
        var query = $(this).val();
        clearTimeout(timeout);

        console.log("Recherche en cours pour :", query);

        timeout = setTimeout(function() {
            if (query.length > 0) {
                console.log("Recherche lancée");
                $.get('/autocomplete', { q: query }, function(data) {
                    console.log("Données de la recherche:", data);

                    $('#results').empty();
                    if (data.length > 0) {
                        console.log("Produits trouvés :", data.length);
                        data.forEach(function(product) {
                            console.log("Produit:", product);

                            var priceHistoryData = [];

                            // ✅ Vérification de la structure de price_history
                            if (product.price_history) {
                                console.log("price_history trouvé:", product.price_history);
                                if (Array.isArray(product.price_history)) {
                                    priceHistoryData = product.price_history;
                                    console.log("price_history est un tableau avec les données suivantes :");
                                    console.log(priceHistoryData);
                                } else {
                                    console.log("price_history n'est pas un tableau :", product.price_history);
                                }
                            } else {
                                console.log("price_history non trouvé dans le produit.");
                            }

                            // ✅ Ajout des produits dans la liste des résultats
                            $('#results').append(`
                                <div class="product-item" 
                                    data-id="${product.asin}" 
                                    data-name="${product.name}" 
                                    data-image="${product.image_url}" 
                                    data-price="${product.price}" 
                                    data-price-history='${JSON.stringify(priceHistoryData)}'>
                                    <div class="product-info">
                                        <img src="${product.image_url}" alt="${product.name}">
                                        <span class="product-name">${product.name}</span>
                                    </div>
                                    <span class="product-price">${product.price}</span>
                                </div>
                            `);
                        });

                        // ✅ Gérer le clic sur un produit
                        $('.product-item').on('click', function() {
                            var name = $(this).data('name');
                            var imageUrl = $(this).data('image');
                            var price = $(this).data('price');
                            var priceHistoryData = $(this).data('price-history');

                            // ✅ Corriger le problème de conversion JSON
                            if (typeof priceHistoryData === "string") {
                                try {
                                    priceHistoryData = JSON.parse(priceHistoryData);
                                } catch (e) {
                                    console.log("Erreur de parsing JSON sur priceHistoryData:", e);
                                    priceHistoryData = [];
                                }
                            }

                            console.log("Produit sélectionné:", name);
                            showProductDetails(name, imageUrl, price, priceHistoryData);
                        });
                    } else {
                        console.log("Aucun produit trouvé");
                        $('#results').append('<div class="no-results">Aucun produit trouvé</div>');
                    }
                }).fail(function(jqXHR, textStatus, errorThrown) {
                    console.log("Erreur AJAX : ", textStatus, errorThrown);
                });
            } else {
                console.log("La recherche est vide");
                $('#results').empty();
            }
        }, 300);
    });

    // ✅ Fermeture de la popup et suppression du graphique avec un délai
    $('#popup-close').on('click', function() {
        console.log("Popup fermé");

        // Attendre 300ms avant de fermer la popup et supprimer le graphique
        setTimeout(function() {
            $('#product-popup').fadeOut(500);  // Délai de 500ms pour fermer la popup

            if (priceChart !== null) {
                priceChart.destroy();
                priceChart = null;
                console.log("Graphique supprimé lors de la fermeture de la popup");
            }
        }, 300);  // Retard de 300ms avant la fermeture
    });
});
