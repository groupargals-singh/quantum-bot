class SystemState:
    """Global System State & Emergency Kill-Switch Manager"""
    def __init__(self):
        self.is_paused = False

system_state = SystemState()
