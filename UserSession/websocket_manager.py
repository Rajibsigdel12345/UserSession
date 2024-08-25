# core/websocket_manager.py
import json
class WebSocketManager:
    def __init__(self):
        # Dictionary to store the mapping of tokens to WebSocket connections
        self.connections = {}

    def add_connection(self, token, connection):
        if not self.connections.get(token):
            self.connections[token] = []
        self.connections[token].append(connection)

    def remove_connection(self, token, connection):
        if token in self.connections:
            self.connections[token].pop(connection)
            connection.close()

    async def notify_disconnect(self, token):
        connections = self.connections.get(token)
        if connections:
            for connection in connections:
                await connection.send(text_data=json.dumps({
                'message': 'logout'
                }))
            # Optionally, close the connection
                await connection.close()
            # Remove the connection from the manager
            del self.connections[token]
    
    def __str__(self):
        return str(self.connections)

# Instantiate a global WebSocketManager
websocket_manager = WebSocketManager()
