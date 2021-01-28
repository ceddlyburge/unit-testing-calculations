from datetime import datetime
from typing import List
from dataclasses import dataclass

@dataclass
# This class contains a fictional list of rows in a cash flow calculation 
# for a wind farm, only the properties used in the calculation below are 
# present, but in reality there would be many more
class CashFlowStep:
    start_of_step: datetime
    special_capital_costs: float
    development_cost_if_owning: float
    development_cost: float
    turbine_cost_including_margin: float
    balance_of_plant_costs_at_financial_close: float
    construction_profit: float
    balance_of_plant_cost_including_margin: float
    # and lots of other properties

