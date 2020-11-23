class Server:
    """
    Represent server class where consecuive events are handled.
    """
    def __init__(self):
        self.all_clients = 0
        self.all_clients_in_queue = 0
        self.clients_number_in_server = 0
        self.clients_number_in_queue = 0
        self.clients_in_server = []
        self.clients_in_queue = []

    def get_server_stats(self):
        return self.clients_number_in_server, self.clients_number_in_queue

    def is_server_empty(self):
        return not self.clients_in_server

    def is_queue_empty(self):
        return not self.clients_in_queue

    def add_client(self, client_id, timestamp):
        self.all_clients += 1
        self.clients_number_in_server += 1
        self.clients_in_server.insert(0, (client_id, timestamp))

    def add_client_to_queue(self, client_id, timestamp):
        self.all_clients_in_queue += 1
        self.clients_number_in_queue += 1
        self.clients_in_queue.insert(0, (client_id, timestamp))

    def get_queue_first_client(self):
        return self.clients_in_queue[-1]

    def delete_client(self, client_id):
        self.clients_number_in_server -= 1
        self.clients_in_server = list(
            filter(
                lambda client: client[0] != client_id,
                self.clients_in_server))

    def delete_client_from_queue(self, client_id):
        self.clients_number_in_queue -= 1
        self.clients_in_queue = list(
            filter(
                lambda client: client[0] != client_id,
                self.clients_in_queue))

    def clear_server(self):
        self.all_clients = 0
        self.all_clients_in_queue = 0
        self.clients_number_in_server = 0
        self.clients_number_in_queue = 0
        self.clients_in_server = []
        self.clients_in_queue = []
