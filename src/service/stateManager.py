class StateManager:
    instance = None
    
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(StateManager, cls).__new__(cls)
        return cls.instance

    def setAttr(self, name, value):
        super().__setattr__(name, value)
    
    def getAttr(self, name):
        return getattr(self, name, '')

