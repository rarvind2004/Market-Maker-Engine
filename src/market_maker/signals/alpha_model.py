from market_maker.common.types import SignalVector


class WeightedAlphaModel:
    def __init__(self, weights: dict[str, float] | None = None) -> None:
        self.weights = weights or {
            "imbalance": 0.45,
            "momentum": 0.25,
            "mean_reversion": 0.15,
            "volatility": -0.15,
        }

    def score(self, vector: SignalVector) -> SignalVector:
        alpha = (
            vector.imbalance * self.weights["imbalance"]
            + vector.momentum * self.weights["momentum"]
            + vector.mean_reversion * self.weights["mean_reversion"]
            + vector.volatility * self.weights["volatility"]
        )
        vector.alpha = alpha
        return vector
