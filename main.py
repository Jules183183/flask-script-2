from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/find_player_server', methods=['POST'])
def find_player_server():
    data = request.json
    player_id = str(data.get('player_id'))
    game_id = str(data.get('game_id'))

    # Appeler l'API Roblox pour récupérer les serveurs publics
    url = f"https://games.roblox.com/v1/games/{game_id}/servers/Public?limit=100"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Impossible de récupérer les serveurs"}), 500

    servers = response.json().get('data', [])
    
    # Chercher le joueur dans les serveurs
    for server in servers:
        if "playerIds" in server:
            if player_id in [str(p) for p in server['playerIds']]:
                return jsonify({"server_id": server['id']})
    
    return jsonify({"error": "Joueur introuvable"}), 404

if __name__ == '__main__':
    app.run()
