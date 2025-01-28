from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def switch_to_iframe_containing_element(driver, xpath):
    """Basculer vers l'iframe qui contient un élément correspondant à l'XPath."""
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for iframe in iframes:
        driver.switch_to.frame(iframe)
        try:
            # Vérifiez si l'élément existe dans l'iframe actuelle
            driver.find_element(By.XPATH, xpath)
            return True
        except Exception:
            driver.switch_to.default_content()  # Revenir au contexte principal si non trouvé
    return False

# Configuration des options pour Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--ignore-certificate-errors')  # Ignorer les erreurs SSL
chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")

# Initialisation du driver Chrome
driver = webdriver.Chrome(options=chrome_options)

try:
    print("Ouverture du site...")
    driver.get("https://www.transfermarkt.fr/ousmane-dembele/profil/spieler/288230")
    print("Site ouvert avec succès.")

    # XPath du bouton à cliquer
    accept_button_xpath = "//button[contains(@aria-label, 'Accepter et continuer') or contains(text(), 'Accepter')]"

    # Basculer dans l'iframe contenant le bouton si nécessaire
    if switch_to_iframe_containing_element(driver, accept_button_xpath):
        print("Bouton détecté dans une iframe.")
    else:
        print("Bouton non détecté dans une iframe. Continuons.")

    # Attente et clic sur le bouton
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, accept_button_xpath))
    )
    print("Bouton trouvé. Clic en cours...")
    accept_button.click()
    print("Clic effectué avec succès.")

    # Revenir au contexte principal après avoir cliqué
    driver.switch_to.default_content()

    # XPath du lien à cliquer
    link_xpath = "/html/body/div/main/div[2]/div[1]/tm-transfer-history/div/div[2]/a"

    # Attente et clic sur le lien
    try:
        # Vérifier si l'élément est dans une iframe avant de cliquer
        if switch_to_iframe_containing_element(driver, link_xpath):
            print("Le lien est dans une iframe, basculement effectué.")
        
        # Attendre que le lien soit cliquable
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, link_xpath))
        )
        print("Lien trouvé. Clic en cours...")
        link.click()  # Effectuer le clic
        print("Clic effectué avec succès.")
    except Exception as e:
        print(f"Erreur lors du clic sur le lien : {e}")

    # Attente de 10 secondes avant de fermer
    print("Attente de 10 secondes avant de fermer le navigateur...")
    time.sleep(10)

except Exception as e:
    print(f"Erreur rencontrée : {e}")
    driver.save_screenshot("debug_screenshot_error.png")

finally:
    driver.quit()
