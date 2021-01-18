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

# This class calculates a subset of properties on a CashFlowStep. In reality
# there would be multiple similar classes, all setting properties on CashFlowStep
class ConstructionMarginCashFlowCostCalculator:
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

# This test, and its name are bad, as it is testing everything. In reality there should be
# many tests, that all test a permutation of the input values, and the names
# would reflect the input values and expected output.
# The function has 3 if statements, which means that there are  2^3, or 8 different paths
# through the code. In reality the calculate_inflation function would need 4 paths through 
# it, which leads to 2^7 paths in total.
# There is also the for loop, which should probably be tested for at least 3 different 
# lengths of list, which is another 2 code paths, for 2^9 (512).
# It is obviously not feasible (or useful) to test this, hence the need to find ways to 
# make it easier
def test_calculate_steps_sets_correct_values():
    balance_of_plant_costs_at_financial_close = 10
    development_cost = 11
    turbine_costs = 12
    special_capital_costs = 13
    date_of_financial_close = datetime(2020, 1, 1)
    in_selling_mode = True
    epc_margin = 0.1
    inflation_rate = 1.1
    inflation_mode = 2
    fraction_of_spend = 0.3

    sut = ConstructionMarginCashFlowCostCalculator(
        balance_of_plant_costs_at_financial_close, 
        development_cost, 
        turbine_costs, 
        special_capital_costs, 
        date_of_financial_close, 
        in_selling_mode, 
        epc_margin, 
        inflation_rate, 
        inflation_mode
    )

    cash_flow_step = CashFlowStep(date_of_financial_close, None, None, None, None, None, None, None)

    sut.calculate_steps([cash_flow_step], fraction_of_spend)

    print(cash_flow_step)

    assert cash_flow_step.special_capital_costs == 13
    assert cash_flow_step.development_cost_if_owning == None
    assert cash_flow_step.development_cost == 11
    assert cash_flow_step.turbine_cost_including_margin == 3.96
    assert cash_flow_step.balance_of_plant_cost_including_margin == 3.3000000000000003
    assert cash_flow_step.construction_profit == -0.66

