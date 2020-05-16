from generate_quotes import get_quote

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ds23-hw2.firebaseio.com/'
})


response = get_quote()
quote = response.body['quote']
author = response.body['author']


ref = db.reference('/')
ref.set(response.body)

print(f'"{quote}" \n\t- {author}\nQuote successfully written to the db.')
