from datetime import datetime
from typing import List
from dataclasses import dataclass
from cash_flow_calculator.cash_flow_step import CashFlowStep

# This class calculates a subset of properties on a CashFlowStep. In reality
# there would be multiple similar classes, all setting properties on CashFlowStep
class ConstructionMarginCalculator:
    def __init__(
            self, 
            balance_of_plant_costs_at_financial_close: float, 
            development_cost: float, 
            turbine_costs: float, 
            special_capital_costs: float, 
            date_of_financial_close: datetime, 
            in_selling_mode: bool, 
            epc_margin: float, 
            inflation_rate: float, 
            inflation_mode: int
        ):
        self.balance_of_plant_costs_at_financial_close = balance_of_plant_costs_at_financial_close
        self.development_cost = development_cost
        self.turbine_costs = turbine_costs
        self.special_capital_costs = special_capital_costs
        self.date_of_financial_close = date_of_financial_close
        self.in_selling_mode = in_selling_mode
        self.epc_margin = epc_margin
        self.inflation_rate = inflation_rate
        self.inflation_mode = inflation_mode

    def calculate_steps(
            self,
            steps: List[CashFlowStep], 
            fraction_of_spend: float
            ):
        for step in steps:
            inflation = self.calculate_inflation(step.start_of_step)
    
            if step.start_of_step == self.date_of_financial_close:
                step.special_capital_costs = self.special_capital_costs

                if self.in_selling_mode == False:
                    step.development_cost_if_owning = self.development_cost

                step.development_cost = self.development_cost

            step.turbine_cost_including_margin = \
                self.turbine_costs * inflation * fraction_of_spend
            
            step.balance_of_plant_cost_including_margin = \
                self.balance_of_plant_costs_at_financial_close * inflation * fraction_of_spend

            if self.in_selling_mode:
                step.construction_profit = \
                    -1 * \
                    (step.turbine_cost_including_margin + step.balance_of_plant_cost_including_margin) * \
                    self.epc_margin
                
                step.turbine_cost_including_margin *= (1 + self.epc_margin)
                
                step.balance_of_plant_cost_including_margin *= (1 + self.epc_margin)

    def calculate_inflation(self, start_of_step: datetime) -> float:
        # return 1 for the sake of the example, but in reality the calculation would need
        # self.date_of_financial_close, self.inflation_rate and self.inflation_mode
        return 1
