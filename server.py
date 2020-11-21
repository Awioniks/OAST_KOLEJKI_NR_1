class Server:
    """
    Represent server class where consecuive events are handled.
    """
    def __init__(self):
        self.clients_in_server = []

    def add_client(self, client_id, timestamp):
        self.clients_in_server.insert(0, (client_id, timestamp))

    def get_queue_first_client(self):
        return self.clients_in_server[-1]

    def delete_client(self, client_id):
        self.clients_in_server = list(
            filter(lambda client: client[0] != client_id),
            self.clients_in_server)
