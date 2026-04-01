import random

class SupplyChainBrain:
    def __init__(self, agent_name, role):
        self.agent_name = agent_name
        self.role = role  # examples are "Supplier", "Retailer", or "Logistics"
        
        # This is the Action Menu
        self.action_space = {
            0: "WAIT",
            1: "SEND_PROPOSAL",
            2: "ACCEPT_OFFER",
            3: "REJECT_OFFER",
            4: "REQUEST_INFO",
            5: "REROUTE"
        }

    def choose_action(self, observation):
      
        print(f"Agent {self.agent_name} decided to: {self.action_space[action_idx]}")
        return action_idx
