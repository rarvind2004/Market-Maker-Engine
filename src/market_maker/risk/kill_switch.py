class KillSwitch:
    def __init__(self) -> None:
        self.active = False
        self.reason = ""

    def trigger(self, reason: str) -> None:
        self.active = True
        self.reason = reason

    def reset(self) -> None:
        self.active = False
        self.reason = ""
