class Mempool:

    def __init__(self):

        self.transactions = []

    def add_transaction(self, tx):

        self.transactions.append(tx)

    def get_transactions(self, limit=10):

        txs = self.transactions[:limit]

        self.transactions = self.transactions[limit:]

        return txs