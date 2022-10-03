# Intégrer votre service avec ma cantine

Ce repo est un exemple d'utilisation des API du service [ma cantine](https://github.com/betagouv/ma-cantine) avec [OAuth2](https://www.oauth.com/).

## Pourquoi intégrer votre logiciel avec ma cantine ?

Vous pouvez simplifier la déclaration des données concernant la [loi EGAlim](https://ma-cantine.agriculture.gouv.fr/mesures-phares/) de vos utilisateurs en interfaçant avec [**nos APIs**](https://ma-cantine.agriculture.gouv.fr/swagger-ui/).

## Demarrer l'application

Pour cet exemple on utilise Python3, [Flask](https://flask.palletsprojects.com/en/2.2.x/), et [Authlib](https://docs.authlib.org/en/latest/client/flask.html). Vous n'avez pas besoin d'être un expert en ces téchnologies pour démarrer cette application.

#### 1- Téléchargez ce repo

#### 2- Installez les dépendances 

Nous vous conseillons d'utiliser *venv*. Les commandes pour macOS/Linux :

```
cd ma-cantine-demo-integration
python3 -m venv venv (ou bien `virtualenv -p python3 venv)
. venv/bin/activate
pip install -r requirements.txt
```

#### 3- Créez un fichier `.env` avec :

```
SECRET_KEY= créez-le avec python -c 'import secrets; print(secrets.token_hex())'
CLIENT_ID= 
CLIENT_SECRET=
SERVICE_URL=https://ma-cantine-demo.cleverapps.io ou https://ma-cantine.agriculture.gouv.fr
```

Vous trouverez les valeurs de `CLIENT_ID` et `CLIENT_SECRET` lors de la création de votre application dans l'éspace dév sur notre site [démo](https://ma-cantine-demo.cleverapps.io/developpement-et-apis/). Enregistrez ces valeurs avant qu'ils soient sécurisés avec un hash.

![Screenshot from 2022-10-03 18-08-40](https://user-images.githubusercontent.com/9282816/193626101-160b50de-52ec-4738-becd-3832ca68644c.png)

#### 4- Démarrez l'application

Pour démarrer le serveur, utilisez la commande `flask run`.

## Bugs communs

Si vous rencontrez des difficultés avec votre integration, vous pouvez essayez les conseils ci-dessous. Vous pouvez aussi contacter l'équipe ma cantine.

- Vérifier que vous avez le bon CLIENT_ID et CLIENT_SECRET
- Vérifier que les URLs vers notre service terminent avec un `/`
