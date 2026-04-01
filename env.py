from pydantic import BaseModel
import random

# --- DATA MODELS ---
class Observation(BaseModel):
    factory_Inven: int
    warehouse_Inven: int
    demand: int
    price: float
    shock_active: bool
    shock_type: str
    time: int

class Action(BaseModel):
    order_qty: int

# --- THE ENVIRONMENT ---
class SupplyChainEnv:
    def __init__(self):
        self.max_steps = 10
        self.reset()

    def reset(self):
        self.stateData = {
            "inventory": {
                "factory": 100,
                "warehouse": 0   
            },
            "demand": 50,
            "price": 10.0,
            "in_transit": [],
            "time": 0,
            "shock_active": False,
            "shock_type": "NONE",
            "shock_duration": 0
        }
        return self._get_obs() 

    def _get_obs(self):
        inv = self.stateData["inventory"]
        return Observation(
            factory_Inven=inv["factory"],
            warehouse_Inven=inv["warehouse"],
            demand=self.stateData["demand"],
            price=self.stateData["price"],
            shock_active=self.stateData["shock_active"],
            shock_type=str(self.stateData["shock_type"]),
            time=self.stateData["time"]
        )

    def apply_shock(self):
        # FIX: Handle active shocks first
        if self.stateData["shock_active"]:
            self.stateData["shock_duration"] -= 1
            if self.stateData["shock_duration"] <= 0:
                print("✨ Shock Cleared: Supply chain returning to normal.")
                self.stateData["shock_active"] = False
                self.stateData["shock_type"] = "NONE"
            return

        # FIX: Removed the 'return' that was blocking new shocks
        if random.random() < 0.20: # Increased probability for testing
            shock_type = random.choice(["PORT_STRIKE", "FUEL_HIKE"])
            self.stateData["shock_active"] = True
            self.stateData["shock_type"] = shock_type
            self.stateData["shock_duration"] = random.randint(2, 4)
            print(f"⚠️ NEW SHOCK: {shock_type} active for {self.stateData['shock_duration']} steps!")

    def process_shipments(self):
        new_shipments = []
        for shipment in self.stateData["in_transit"]:
            shipment["time_left"] -= 1
            if shipment["time_left"] <= 0:
                self.stateData["inventory"]["warehouse"] += shipment["quantity"]
            else:
                new_shipments.append(shipment)
        self.stateData["in_transit"] = new_shipments 

    def update_market(self):
        self.stateData["demand"] = max(0, self.stateData["demand"] + random.randint(-5, 5))
        self.stateData["price"] = max(1.0, self.stateData["price"] + random.uniform(-0.5, 0.5))

    def step(self, action: Action):
        # 1) logic updates
        self.apply_shock()
        self.process_shipments()

        # 2) Place order from Factory
        factory_stock = self.stateData["inventory"]["factory"]
        order_qty = min(action.order_qty, factory_stock)   
        self.stateData["inventory"]["factory"] -= order_qty

        # 3) Travel Time logic
        travel_time = 2
        if self.stateData["shock_active"]:
            if self.stateData["shock_type"] == "PORT_STRIKE":
                travel_time += 3
            elif self.stateData["shock_type"] == "FUEL_HIKE":
                 travel_time += 1    

        # 4) Log Shipment
        self.stateData["in_transit"].append({
            "quantity": order_qty,
            "time_left": travel_time
        })

        # 5) Fulfill Demand
        warehouse = self.stateData["inventory"]["warehouse"]
        demand = self.stateData["demand"]
        fulfilled = min(warehouse, demand)
        self.stateData["inventory"]["warehouse"] -= fulfilled
        
        # 6) Revenue Calculation
        reward = fulfilled * self.stateData["price"] 

        # 7) Updates
        self.update_market()
        self.stateData["time"] += 1
        done = (self.stateData["time"] >= self.max_steps)

        return self._get_obs(), reward, done, {}

# --- INTEGRATION TEST ---
if __name__ == "__main__":
    env = SupplyChainEnv()
    obs = env.reset()
    
    print(f"Initial State: {obs}\n")
    
    for i in range(5):
        # Fake an action: Ordering 20 units
        test_action = Action(order_qty=20)
        obs, reward, done, info = env.step(test_action)
        print(f"Step {i+1}: Action(20) | Reward: {reward:.2f} | Warehouse: {obs.warehouse_Inven} | Shock: {obs.shock_type}")
