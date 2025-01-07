from cryptography.fernet import Fernet
from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Route d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')

# Fonction générant une clé (uniquement une fois lors du démarrage)
key = Fernet.generate_key()
f = Fernet(key)

# Route pour crypter une valeur
@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion de la chaîne en bytes
    token = f.encrypt(valeur_bytes)  # Crypter la valeur
    return f"Valeur cryptée : {token.decode()}"  # Retourne le token crypté sous forme de chaîne

# Route pour décrypter une valeur
@app.route('/decrypt/<string:valeur>')
def decryptage(valeur):
    try:
        valeur_bytes = valeur.encode()  # Conversion de la chaîne en bytes
        decrypted_value = f.decrypt(valeur_bytes)  # Décrypter la valeur
        return f"Valeur décryptée : {decrypted_value.decode()}"  # Retourne la valeur décryptée sous forme de chaîne
    except Exception as e:
        return f"Erreur lors du décryptage : {str(e)}"  # En cas d'erreur, retourne un message d'erreur

# Route pour permettre à l'utilisateur de définir sa propre clé
@app.route('/set-key', methods=['POST'])
def set_key():
    user_key = request.json.get('key')  # Recevoir la clé via JSON
    if not user_key:
        return jsonify({"error": "No key provided"}), 400  # Si aucune clé n'est fournie
    try:
        f = Fernet(user_key.encode())  # Créer un nouvel objet Fernet avec la clé de l'utilisateur
        return jsonify({"message": "Key set successfully"}), 200  # Réponse indiquant que la clé a été définie
    except Exception as e:
        return jsonify({"error": f"Invalid key: {str(e)}"}), 400  # Si la clé est invalide

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True)
