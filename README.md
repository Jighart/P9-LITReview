# LIT Review

***MVP de LITReview, site communautaire de partage de critiques de livres.***

_Testé sous Windows 10 - Python 3.11 - Django 4.1.5_

## Initialisation du projet

### Windows :
Dans Windows Powershell, naviguer vers le dossier souhaité.
###### • Récupération du projet

```
git clone https://github.com/Jighart/P9-LITReview.git
```

###### • Activer l'environnement virtuel

```
cd P9-LITReview 
python -m venv venv 
venv\Scripts\activate.bat
```

###### • Installer les paquets requis

```
pip install -r requirements.txt
```


### MacOS et Linux :
Dans le terminal, naviguer vers le dossier souhaité.
###### • Récupération du projet
```
git clone https://github.com/Jighart/P9-LITReview.git
```

###### • Activer l'environnement virtuel
```
cd P9-LITReview 
python3 -m venv venv 
source venv/bin/activate
```

###### • Installer les paquets requis
```
pip install -r requirements.txt
```

## Utilisation

1. Lancer le serveur Django:

```
python manage.py runserver
```

2. Dans le navigateur de votre choix, se rendre à l'adresse http://127.0.0.1:8000/


## Infos

### Django administration

Identifiant : **Admin** | Mot de passe : **LITReview**

&rarr; http://127.0.0.1:8000/admin/

### Liste des utilisateurs existants

| *Identifiant* | *Mot de passe* |
|---------------|----------------|
| Admin         | LITReview    |
| Test_user_1   | LITReview    |
| Test_user_2   | LITReview    |
| Test_user_3   | LITReview    |


### Fonctionnalités

- Se connecter et s'inscrire ;
- Consulter son profil et le modifier, ajouter une image de profil ;
- Consulter un flux contenant les tickets et critiques des utilisateurs auxquels on est abonné ;
- Créer des tickets de demande de critique ;
- Créer des critiques, en réponse ou non à des tickets ;
- Voir ses propres posts, les modifier ou les supprimer ;
- Suivre d'autres utilisateurs, ou se désabonner.