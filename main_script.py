from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, JavascriptException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import requests
import os
import time
import re

def setup_driver():
    """Initialisiert den WebDriver und öffnet die Login-Seite."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(1920, 1080)
    driver.get('https://www.pinterest.de/login/')
    return driver

def login(driver, email, password):
    """Loggt einen Benutzer ein."""
    #driver.get('https://www.pinterest.de/login/')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "id")))
    email_input = driver.find_element(By.NAME, "id")
    password_input = driver.find_element(By.NAME, "password")
    email_input.send_keys(email)
    password_input.send_keys(password)
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()
    time.sleep(8)  # Warte bis der Login abgeschlossen ist

def navigate_to_url(driver, url, sleeptime):
    """Navigiert zu einer spezifischen URL."""
    driver.get(url)
    time.sleep(sleeptime)  
def download_image(image_url, folder):
    """Lädt ein Bild herunter und speichert es in einem angegebenen Verzeichnis."""
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        original_image_url = image_url_original(image_url)
        response = requests.get(original_image_url, stream=True)
        if response.status_code == 200:
            file_extension = original_image_url.rsplit('.', 1)[-1]
            file_path = os.path.join(folder, image_url.split('/')[-1].rsplit('.', 1)[0] + '.' + file_extension)
            with open(file_path, 'wb') as f:
                f.write(response.content)
    except Exception as e:
        print(f"Fehler beim Herunterladen von {image_url}: {e}")

def image_url_original(image_url):
    """Ändert die Bild-URL, um die Originalgröße zu erhalten."""
    base_url = re.sub(r'/\d+x/', '/originals/', image_url).rsplit('.', 1)[0]
    original_extension = image_url.rsplit('.', 1)[-1]
    possible_extensions = [original_extension] + [ext for ext in ['jpg', 'png'] if ext != original_extension]
    for extension in possible_extensions:
        modified_url = f"{base_url}.{extension}"
        if check_image_exists(modified_url):
            return modified_url
    return image_url
def check_image_exists(image_url):
    """Überprüft, ob eine Bild-URL eine gültige Antwort mit den Endungen PNG oder JPG liefert."""
    try:
        response = requests.head(image_url)
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            if 'image/png' in content_type or 'image/jpeg' in content_type:
                return True
    except Exception as e:
        print(f"Fehler beim Überprüfen des Bilds {image_url}: {e}")
    return False
def get_image_src(image_element):
    """Extrahiert die Bildquelle aus einem Bildelement."""
    try:
        return image_element.get_attribute('src')
    except StaleElementReferenceException:
        return None
def download_images_from_page(driver, scroll_pause_time, folder="downloaded_images"):
    """Scrollt schrittweise durch die Seite und lädt sichtbare Bilder herunter, wobei vor jedem Scroll sichergestellt wird, dass alle sichtbaren Bilder verarbeitet wurden."""
    initial_pause = 2       # Initiale Wartezeit vor dem ersten Scrollen
    scroll_length = 800     # Pixelanzahl, um die bei jedem Schritt gescrollt wird
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempt_count = 0       # Zählt, wie oft versucht wurde zu scrollen, ohne dass neue Inhalte geladen wurden
    downloaded_images = set()  # Zum Speichern bereits heruntergeladener Bild-URLs
    time.sleep(initial_pause)

    while True:
        images = driver.find_elements(By.CSS_SELECTOR, 'img:not(.hCL.kVc.L4E.MIw.N7A.XiG)')
        new_images_found = False
        for image in images:
            src = get_image_src(image)
            if src and src not in downloaded_images:
                # hier rausfiltern der richtige folder
                download_image(src, folder)
                downloaded_images.add(src)
                new_images_found = True
        
        driver.execute_script(f"window.scrollBy(0, {scroll_length});")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            attempt_count += 1
            if attempt_count >= 3:  # 3 mal versuchen
                break
        else:
            last_height = new_height
            attempt_count = 0  # Zurücksetzen, wenn neue Inhalte geladen wurden

def navigate_and_download_from_folders(driver, base_url, scroll_pause_time, folder_name):
    """Erkennt Ordner auf der Seite, navigiert hinein, lädt Bilder herunter und kehrt zurück."""
    time.sleep(scroll_pause_time)
    try:
        folders = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.Wk9.xQ4.CCY.S9z.eEj.kVc.Tbt.L4E.e8F.BG7"))
        )
        num_folders = len(folders)
        start_index = 1 if base_url.endswith('_saved/') else 0  # Überspringen des ersten Ordners, wenn die URL auf '_saved/' endet

        for i in range(start_index, num_folders):
            driver.get(base_url)
            time.sleep(scroll_pause_time)
            folders = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.Wk9.xQ4.CCY.S9z.eEj.kVc.Tbt.L4E.e8F.BG7"))
            )
            if i < len(folders):
                folder_link = folders[i]
                folder_url = folder_link.get_attribute('href')
                folder_name_pin = folder_url.split('/')[-2]
                driver.get(folder_url)
                time.sleep(scroll_pause_time)
                download_images_from_page(driver, scroll_pause_time, f"{folder_name}/{folder_name_pin}")
    except TimeoutException:
        print("Keine Ordner auf der Seite gefunden, fahre fort mit Bildern auf der Hauptseite.")

def main(email, password, sleeptime, url, no_folder_flag):
    driver = setup_driver()
    try:
        login(driver, email, password)
        folder_name_from_url = url.strip('/').split('/')[-1]
        navigate_to_url(driver, url, int(sleeptime))
        navigate_and_download_from_folders(driver, url, int(sleeptime), folder_name_from_url)
        navigate_to_url(driver, url, int(sleeptime))
        download_images_from_page(driver, int(sleeptime), folder_name_from_url)
    finally:
        driver.quit()
        print("Alle Schritte abgeschlossen und der Browser wurde geschlossen.")

if __name__ == "__main__":
    email = 'x'
    password = 'x'
    sleeptime = 2
    url = 'https://www.pinterest.de/x/x/'
    no_folder_flag = False
    main(email, password, sleeptime, url, no_folder_flag)
