$(document).ready(function() {
    var timeout = null;

    // Fonction pour afficher les détails du produit
    function showProductDetails(name, imageUrl, price, priceHistoryData) {
        console.log("showProductDetails appelé");
        $('#popup-name').text(name);
        $('#popup-image').attr('src', imageUrl);
        $('#price-large').text(price);
        $('#popup-price').text(price);
        $('#product-popup').fadeIn();

        console.log("priceHistoryData:", priceHistoryData);

        // Si priceHistoryData existe et contient des données valides
        if (priceHistoryData && Array.isArray(priceHistoryData) && priceHistoryData.length > 0) {
            console.log("Données de priceHistoryData valides");
            var timestamps = priceHistoryData.map(function(item) {
                console.log("Item dans priceHistoryData:", item); // Log chaque élément
                return new Date(item.timestamp).toLocaleString();
            });

            var prices = priceHistoryData.map(function(item) {
                console.log("Prix de l'item:", item.price); // Log chaque prix
                return item.price;
            });

            console.log("Timestamps:", timestamps);
            console.log("Prices:", prices);

            var ctx = document.getElementById('price-history-chart').getContext('2d');
            var priceChart = new Chart(ctx, {
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
    }

    // Quand un produit est sélectionné dans la recherche
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

                            // Afficher toutes les propriétés du produit pour mieux comprendre sa structure
                            console.log("Propriétés du produit:", Object.keys(product));

                            var priceHistoryData = [];

                            // Vérification de la structure de l'objet
                            if (product.price_history) {
                                console.log("price_history trouvé:", product.price_history);
                                if (Array.isArray(product.price_history)) {
                                    priceHistoryData = product.price_history;
                                    console.log("price_history est un tableau avec les données suivantes :");
                                    console.log(priceHistoryData); // Log tout l'historique des prix
                                } else {
                                    console.log("price_history n'est pas un tableau :", product.price_history);
                                }
                            } else {
                                console.log("price_history non trouvé dans le produit.");
                            }

                            // Ajouter le produit à la liste
                            $('#results').append(`
                                <div class="product-item" data-id="${product.asin}" data-name="${product.name}" data-image="${product.image_url}" data-price="${product.price}" data-price-history='${JSON.stringify(priceHistoryData)}'>
                                    <div class="product-info">
                                        <img src="${product.image_url}" alt="${product.name}">
                                        <span class="product-name">${product.name}</span>
                                    </div>
                                    <span class="product-price">${product.price}</span>
                                </div>
                            `);
                        });

                        // Gérer le clic sur un produit
                        $('.product-item').on('click', function() {
                            var name = $(this).data('name');
                            var imageUrl = $(this).data('image');
                            var price = $(this).data('price');
                            var priceHistoryData = $(this).data('price-history');
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

    // Fermeture du popup
    $('#popup-close').on('click', function() {
        console.log("Popup fermé");
        $('#product-popup').fadeOut();
    });
});
