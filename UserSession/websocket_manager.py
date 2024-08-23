# core/websocket_manager.py
import json
class WebSocketManager:
    def __init__(self):
        # Dictionary to store the mapping of tokens to WebSocket connections
        self.connections = {}

    def add_connection(self, token, connection):
        self.connections[token] = connection

    def remove_connection(self, token):
        if token in self.connections:
            del self.connections[token]

    async def notify_disconnect(self, token):
        connection = self.connections.get(token)
        if connection:
            await connection.send(text_data=json.dumps({
                'message': 'logout'
            }))
            # Optionally, close the connection
            await connection.close()
            # Remove the connection from the manager
            self.remove_connection(token)

# Instantiate a global WebSocketManager
websocket_manager = WebSocketManager()
