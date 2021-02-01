from datetime import datetime
from typing import List
from dataclasses import dataclass
from cash_flow_calculator.cash_flow_step import CashFlowStep

# This class calculates a subset of properties on CashFlowSteps. In reality
# there would be multiple similar classes, all setting properties on CashFlowStep
# This example demonstrates use of the "Blackboard Pattern", which breaks
# dependencies and creates more loosely couple code.
# In this case the CashFlowStep is the blackboard. 
# This class requires two properties to be available on the blackboard, and if
# they are not it simply returns False, and expects to be called again later
# when the values are available. This requires another class to calculate
# these properties, and a class to orchestrate the blackboard / calculators
class ConstructionMarginCalculatorBlackboardPattern:
    def __init__(
            self, 
            development_cost: float, 
            special_capital_costs: float, 
            date_of_financial_close: datetime, 
            in_selling_mode: bool, 
            epc_margin: float
        ):
        self.development_cost = development_cost
        self.special_capital_costs = special_capital_costs
        self.date_of_financial_close = date_of_financial_close
        self.in_selling_mode = in_selling_mode
        self.epc_margin = epc_margin

    def calculate_step(self, step: CashFlowStep, fraction_of_spend: float):

        if (step.turbine_cost_including_margin is None 
            or step.balance_of_plant_cost_including_margin is None) :
            return False

        if step.start_of_step == self.date_of_financial_close:
            step.special_capital_costs = self.special_capital_costs

            if self.in_selling_mode == False:
                step.development_cost_if_owning = self.development_cost

            step.development_cost = self.development_cost

        if self.in_selling_mode:
            step.construction_profit = \
                -1 * \
                (step.turbine_cost_including_margin + step.balance_of_plant_cost_including_margin) * \
                self.epc_margin

        return True


# Example calculators to add the required properties to the blackbloard / CashFlowStep
class TurbineCostCalculator:
    def calculate_step(self, step: CashFlowStep, fraction_of_spend: float):
        step.turbine_cost_including_margin = 1 


class BalanceOfPlantCalculator:
    def calculate_step(self, step: CashFlowStep, fraction_of_spend: float):
        step.balance_of_plant_cost_including_margin = 1 


# Example class to orchestrate the blackboard and calculators
class CashFlowStepCalculator:
    def __init__(self, calculators: List[object]):
        self.calculators = calculators

    def calculate_step(self, step: CashFlowStep, fraction_of_spend: float):
        temporary_calculators = self.calculators.copy()

        # Loop through calculators until they all indicate that they have 
        # calculated. This code is quite naive and doesn't check for 
        # cyclic dependencies.
        while len(temporary_calculators > 0):
            calculator = temporary_calculators.pop(0)

            if calculator.calculate_step(step, fraction_of_spend) == False:
                temporary_calculators.append(calculator)
        
        
