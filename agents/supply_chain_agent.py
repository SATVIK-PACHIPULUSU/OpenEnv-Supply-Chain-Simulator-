import random
import torch

class SupplyChainBrain:
    def __init__(self, agent_name, role_type="Retailer"):
        """
        Initializes the AI Brain for the Meta OpenEnv Hackathon.
        :param agent_name: Unique ID for the agent (e.g., 'Factory_1')
        :param role_type: The agent's position in the chain ('Supplier', 'Retailer', 'Logistics')
        """
        self.agent_name = agent_name
        self.role_type = role_type
        
        # ACTION SPACE: The 'Menu' of moves the AI can make
        self.action_space = {
            0: "WAIT",            # Observe and stay idle
            1: "SEND_PROPOSAL",   # Negotiate a price/quantity
            2: "ACCEPT_OFFER",    # Finalize a trade
            3: "REJECT_OFFER",    # End the current negotiation
            4: "REQUEST_INFO",    # MCP Protocol: Ask for inventory/lead times
            5: "REROUTE"          # Risk Management: Change paths due to shocks
        }

    def process_observation(self, obs):
        """
        Step 4: Interpreting World Shocks (Strikes, Holidays, War)
        """
        transport_status = obs.get("transport_status", 0)
        inventory = obs.get("inventory", 0)
        
        # Strategic awareness logic
        if transport_status == 1:
            print(f"[{self.agent_name}] Info: National Holiday. Expecting low demand.")
        elif transport_status == 2:
            print(f"[{self.agent_name}] Warning: Port Strike/Curfew. Logistics delayed.")
        elif transport_status == 3:
            print(f"[{self.agent_name}] ALERT: Wartime Scenario. High risk/High inflation.")
            
        return transport_status

    def calculate_reward(self, deal_made, profit, inventory_count, time_taken, transport_status):
        """
        Step 3: The 'Motivation' Math.
        This tells the AI if it is succeeding or failing.
        """
        reward = 0.0

        # 1. Economic Success: Profit is the primary driver
        reward += profit 

        # 2. Efficiency Penalty: Don't spend too many turns 'WAITING'
        reward -= (time_taken * 0.1)

        # 3. Reliability: Heavy penalty for 'Stockouts' (0 inventory)
        if inventory_count == 0:
            reward -= 10.0 

        # 4. Resilience Bonus: Reward the agent for surviving extreme shocks
        if transport_status == 3 and deal_made:
            reward += 5.0  # Extra points for a successful trade during 'War'

        # 5. Deal Completion: Incentive to close negotiations
        if deal_made:
            reward += 2.0

        return reward

    def choose_action(self, observation):
        """
        Step 2: Decision Making Logic.
        Currently using a random explorer. 
        TODO: Link to a PyTorch Neural Network for Round 2.
        """
        # First, we 'see' the world
        status = self.process_observation(observation)
        
        # The AI picks an action from the menu (0 to 5)
        action_idx = random.randint(0, 5)
        
        print(f"Decision: {self.agent_name} chose {self.action_space[action_idx]}")
        return action_idx

# Example of how this will be called by Teammate A (The World Architect)
if __name__ == "__main__":
    # Test Run
    my_brain = SupplyChainBrain("Agent_Alpha", "Retailer")
    sample_obs = {"transport_status": 3, "inventory": 5, "price": 150}
    
    action = my_brain.choose_action(sample_obs)
    print(f"Action Code to send back to Environment: {action}")
