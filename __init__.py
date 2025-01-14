from flask import Flask, render_template, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

# Clé de cryptage
key = Fernet.generate_key()
f = Fernet(key)

# Page d'accueil avec des catégories cliquables
@app.route('/')
def accueil():
    return render_template('hello.html')

# Routes pour chaque exercice
@app.route('/exercice1')
def exercice1():
    return render_template('page1.html')

@app.route('/exercice2')
def exercice2():
    return render_template('page2.html')

@app.route('/exercice3')
def exercice3():
    return render_template('page3.html')

@app.route('/exercice4')
def exercice4():
    return render_template('page4.html')

@app.route('/exercice5')
def exercice5():
    return render_template('page5.html')

@app.route('/Exemple_Base_SVG')
def Exemple_Base_SVG():
    return render_template('Exemple_Base_SVG.html')

@app.route('/Maison')
def Maison():
    return render_template('Maison.html')
@app.route('/jack')
def Maison():
    return render_template('jack.html')
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
        global f  # Modifier la variable globale f
        f = Fernet(user_key.encode())  # Créer un nouvel objet Fernet avec la clé de l'utilisateur
        return jsonify({"message": "Key set successfully"}), 200  # Réponse indiquant que la clé a été définie
    except Exception as e:
        return jsonify({"error": f"Invalid key: {str(e)}"}), 400  # Si la clé est invalide

if __name__ == "__main__":
    app.run(debug=True)
