# Intégrer votre service avec ma cantine

Ce repo est un exemple de comment intégrer votre site web avec le service [ma cantine](https://github.com/betagouv/ma-cantine) en utilisant [OAuth2](https://www.oauth.com/).

## Pourquoi intégrer avec ma cantine ?

Vous pouvez aider vos utilisateurs en fournissant des données automatiquement en utilisant [**nos APIs**](https://ma-cantine.agriculture.gouv.fr/swagger-ui/).

En bref, vous pouvez nous envoyer des données sur les cantines gérées par l'utilisateur, et des données sur les pratiques de gestion liés aux [mesures EGAlim](https://ma-cantine.agriculture.gouv.fr/mesures-phares/), comme la partie des achats bio et durable.

## Demarrer l'application

Pour cet exemple on utilise Python3, [Flask](https://flask.palletsprojects.com/en/2.2.x/), et [Authlib](https://docs.authlib.org/en/latest/client/flask.html). Vous n'avez pas besoin de connaître ces téchnologies beaucoup pour démarrer cette application.

Téléchargez ce repo.

Les commandes pour macOS/Linux :

```
cd ma-cantine-demo-integration
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Créez un fichier `.env` avec :

```
SECRET_KEY= créez-le avec python -c 'import secrets; print(secrets.token_hex())'
CLIENT_ID= 
CLIENT_SECRET=
SERVICE_URL=https://ma-cantine-demo.cleverapps.io ou https://ma-cantine.agriculture.gouv.fr
```

Pour le `CLIENT_ID` et `CLIENT_SECRET` vous trouverez les valeurs au moment où vous créez l'application dans l'éspace dév sur notre site [démo](https://ma-cantine-demo.cleverapps.io/developpement-et-apis/). Enregistrez les valeurs avant qu'ils soient sécurisés avec un hash.

Démarrez l'application avec :

`flask run`

## Bugs communs

Si vous rencontrez des difficultés avec votre integration, vous pouvez essayez les conseils en-dessous. Vous pouvez aussi contacter l'équipe ma cantine.

- Vérifier que vous avez le bon CLIENT_ID et CLIENT_SECRET
- Vérifier que les URLs vers notre service termine avec un `/`
