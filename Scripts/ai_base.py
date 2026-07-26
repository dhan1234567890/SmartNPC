class AIBase:
    def __init__(self, npc):
        """
        Base class for all AI controllers.
        :param npc: The NPC instance this AI is controlling.
        """
        self.npc = npc
        self.current_state = "Idle"

    def update(self, dt, player, obstacles):
        """
        To be overridden by subclasses (RuleBased, FSM, FuzzyLogic).
        This method should determine the action and call the appropriate NPC methods.
        """
        pass
