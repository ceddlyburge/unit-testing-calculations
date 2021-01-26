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

# Isolating the balance_of_plant_cost_including_margin value allows the test to 
# concentrate just on that one value / calculation, which means that a lot less
# setup data is required. The Test Data Builder pattern hides this Irrelevant 
# Information, and the test becomes more concise and more expressive.
# Including the calculation in the test continues to make the test more expressive
# and clearly communicates its intent. Interestingly the test code is no longer
# an exact copy of the system under test, as it already knows that it is 
# in_selling_mode, so doesn't need a conditional statement. This means that the
# test code is simpler than the system under test code, and the simpler a test is
# the easier it is find out what is wrong when it fails.
# There should obvioulsy be more tests like this, but only one is shown for 
# simplicity. For example testing the balance_of_plant_cost_including_margin
# when in_selling_mode is False.
def test_calculates_balance_of_plant_cost_including_margin_correctly_when_in_selling_mode():
    balance_of_plant_costs_at_financial_close = 10
    fraction_of_spend = 0.3
    epc_margin = 0.1
    inflation = 1.2

    sut = ConstructionMarginCashFlowCostCalculatorBuilder() \
        .with_balance_of_plant_costs_at_financial_close(balance_of_plant_costs_at_financial_close) \
        .with_inflation(inflation) \
        .with_epc_margin(epc_margin) \
        .in_selling_mode() \
        .build()

    cash_flow_step = CashFlowStepBuilder().build()

    sut.calculate_step(cash_flow_step, fraction_of_spend)

    assert cash_flow_step.balance_of_plant_cost_including_margin == (balance_of_plant_costs_at_financial_close * inflation * fraction_of_spend) * (1 + epc_margin)


class ConstructionMarginCashFlowCostCalculatorBuilder:

    def __init__(self): 
        self._sut = ConstructionMarginCashFlowCostCalculator(
        balance_of_plant_costs_at_financial_close=any_double, 
        development_cost=any_double, 
        turbine_costs=any_double, 
        special_capital_costs=any_double, 
        date_of_financial_close=None, 
        in_selling_mode=None, 
        epc_margin=any_double, 
        inflation_calculator=MockInflation(any_double)
    )

    def with_balance_of_plant_costs_at_financial_close(self, balance_of_plant_costs_at_financial_close: float): 
        self._sut.balance_of_plant_costs_at_financial_close = balance_of_plant_costs_at_financial_close
        return self

    def with_inflation(self, inflation: float): 
        self._sut.inflation_calculator = MockInflation(inflation)
        return self

    def with_epc_margin(self, epc_margin: float): 
        self._sut.epc_margin = epc_margin
        return self

    def in_selling_mode(self): 
        self._sut.in_selling_mode = True
        return self

    def build(self):
        return self._sut


class CashFlowStepBuilder:

    def __init__(self): 
        self._cash_flow_step = CashFlowStep(None, None, None, None, None, None, None, None)

    def build(self):
        return self._cash_flow_step


class MockInflation:
    def __init__(self, constant_inflation):
        self._constant_inflation = constant_inflation

    def inflation_to(self, when: datetime):
        return self._constant_inflation

# The code and test for the CashFlowStepsCalculator is no longer shown