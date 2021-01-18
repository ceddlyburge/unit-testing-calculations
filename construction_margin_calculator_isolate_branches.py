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

# This class calculates a subset of properties on CashFlowSteps. In reality
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
            inflation_calculator
        ):
        self.balance_of_plant_costs_at_financial_close = balance_of_plant_costs_at_financial_close
        self.development_cost = development_cost
        self.turbine_costs = turbine_costs
        self.special_capital_costs = special_capital_costs
        self.date_of_financial_close = date_of_financial_close
        self.in_selling_mode = in_selling_mode
        self.epc_margin = epc_margin
        self.inflation_calculator = inflation_calculator

    def calculate_step(self, step: CashFlowStep, fraction_of_spend: float):
        inflation = self.inflation_calculator.inflation_to(step.start_of_step)

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

any_double = 5.55555

# Manipulating the conditionals so that most of them are false allows us to test
# small parts of the function in isolation, which makes the tests a lot simpler,
# and makes it feasible to include the calculation in the test, and to give the
# test a better name.
# There should obvioulsy be more tests like this, but only one is shown for 
# simplicity.
def test_calculates_turbine_cost_including_margin_correctly():
    not_in_selling_mode = False
    turbine_costs = 12
    fraction_of_spend = 0.3
    inflation = 2
    date_of_financial_close = datetime(2020, 1, 1)
    not_date_of_financial_close = datetime(2020, 1, 2)

    balance_of_plant_costs_at_financial_close = 10
    development_cost = 11
    special_capital_costs = 13
    epc_margin = 0.1
    inflation_rate = 1.1
    inflation_mode = 2

    sut = ConstructionMarginCashFlowCostCalculator(
        any_double, 
        any_double, 
        turbine_costs, 
        any_double, 
        date_of_financial_close, 
        not_in_selling_mode, 
        any_double, 
        MockInflation(inflation), 
    )

    cash_flow_step = CashFlowStep(not_date_of_financial_close, None, None, None, None, None, None, None)

    sut.calculate_step(cash_flow_step, fraction_of_spend)

    # It is now simple to include the calculation in the test, so no
    # the test clearly communicates that the turbine_cost_including_margin
    # should be the turbine_costs * fraction_of_spend * inflation
    assert cash_flow_step.turbine_cost_including_margin == turbine_costs * fraction_of_spend * inflation


class MockInflation:
    def __init__(self, constant_inflation):
        self._constant_inflation = constant_inflation

    def inflation_to(self, when: datetime):
        return self._constant_inflation

# The code and test for the CashFlowStepsCalculator is no longer shown