#!/bin/bash

# Lancer l'application Dash
python app.py &

# Lancer le script de scraping
python time_scraper.py &

# Attendre que tous les processus se terminent
wait
