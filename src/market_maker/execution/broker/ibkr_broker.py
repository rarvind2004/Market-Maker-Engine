from market_maker.execution.broker.base import Broker

class IbkrBroker(Broker):
    def place(self, order):
        raise NotImplementedError("Live broker adapter not implemented in scaffold")
