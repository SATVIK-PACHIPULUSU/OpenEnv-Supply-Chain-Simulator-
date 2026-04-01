from env import SupplyChainEnv, Action
from agents.supply_chain_agent import SupplyChainBrain

def run_simulation():
    # 1. Initialize the World (Role A) and the Brain (Role B)
    env = SupplyChainEnv()
    brain = SupplyChainBrain(agent_name="Meta_AI_Manager", role_type="Retailer")
    
    # 2. Reset the environment to get the first observation
    obs = env.reset()
    total_reward = 0
    print(f"--- 🚀 Starting Supply Chain Simulation ---")

    # 3. Run for the max steps defined in the Env (10 steps)
    for step_num in range(1, env.max_steps + 1):
        print(f"\n--- 🕒 Step {step_num} ---")
        
        # BRAIN PHASE: The AI looks at the world and picks an action index (0-5)
        action_idx = brain.choose_action(obs)
        
        # TRANSLATION PHASE: 
        # If the brain picks 'SEND_PROPOSAL' (1), we calculate a quantity.
        # Otherwise, we order 0 for now to keep it simple.
        if action_idx == 1:
            qty = brain.generate_order_qty(obs.demand, obs.warehouse_Inven)
        else:
            qty = 0
            
        # WORLD PHASE: We send the translated Action back to the environment
        env_action = Action(order_qty=qty)
        obs, reward, done, info = env.step(env_action)
        
        total_reward += reward
        
        # REPORTING
        print(f"📦 Action: Ordered {qty} units")
        print(f"💰 Step Reward: {reward:.2f} | Current Warehouse Stock: {obs.warehouse_Inven}")
        print(f"🌍 World Status: {obs.shock_type}")

        if done:
            print(f"\n--- ✅ Simulation Finished ---")
            print(f"🏆 Total Cumulative Reward: {total_reward:.2f}")
            break

if __name__ == "__main__":
    run_simulation()
