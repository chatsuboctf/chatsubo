from app import socketio_server, server

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
socketio_server.run(server, debug=True, host="0.0.0.0", port=5000)
