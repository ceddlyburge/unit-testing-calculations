from datetime import datetime
from cash_flow_calculator.cash_flow_step import CashFlowStep
from cash_flow_calculator.construction_margin_calculator_blackboard_pattern import ConstructionMarginCalculatorBlackboardPattern
from tests.mock_inflation import MockInflation

# The full calculation for `construction_profit` is quite long and complicated,
# but we can simplify by setting some "additive" properties to 0, and some 
# "multiplicative" properties to 1, so that they don't effect the result.
# This test sets balance_of_plant_costs_at_financial_close to 0, so that we can
# concentrate on the turbine_costs. This again means that the test code is
# simpler than the system under test, which helps with "tests as documentation"
# and the "Obscure Test" smell.
# There should obvioulsy be more tests like this, but only one is shown for 
# simplicity. 
def test_construction_profit_includes_turbine_costs():
    turbine_cost_including_margin = 10
    balance_of_plant_cost_including_margin = 11
    fraction_of_spend = 0.3
    epc_margin = 0.1

    sut = ConstructionMarginCashFlowCostCalculatorBuilder() \
        .with_epc_margin(epc_margin) \
        .in_selling_mode() \
        .build()

    cash_flow_step = CashFlowStepBuilder() \
        .with_balance_of_plant_cost_including_margin(balance_of_plant_cost_including_margin) \
        .with_turbine_cost_including_margin(turbine_cost_including_margin) \
        .build()

    sut.calculate_step(cash_flow_step, fraction_of_spend)

    assert cash_flow_step.construction_profit == \
        -1 * \
        (turbine_cost_including_margin + balance_of_plant_cost_including_margin) * \
        epc_margin


any_double = 5.55555

class ConstructionMarginCashFlowCostCalculatorBuilder:

    def __init__(self): 
        self._sut = ConstructionMarginCalculatorBlackboardPattern(
            development_cost=any_double, 
            special_capital_costs=any_double, 
            date_of_financial_close=None, 
            in_selling_mode=None, 
            epc_margin=any_double
        )

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
        self._sut = CashFlowStep(None, None, None, None, None, None, None, None)

    def with_turbine_cost_including_margin(self, turbine_cost_including_margin: float): 
        self._sut.turbine_cost_including_margin = turbine_cost_including_margin
        return self
    
    def with_balance_of_plant_cost_including_margin(self, balance_of_plant_cost_including_margin: float): 
        self._sut.balance_of_plant_cost_including_margin = balance_of_plant_cost_including_margin
        return self

    def build(self):
        return self._sut


# The test for the CashFlowStepsCalculator is no longer shown

# The test for the blackboard / CashFlowStep orchestrator is
# (CashFlowStepCalculator) is also not shown. It's quite simple
# so hopefully its easy to imagine what the test would look like.
# It wouldn't really make sense if there were just one or two 
# calculators, but comes in to its own as the number of 
# calculators, and the dependencies between them increases.
# It is also relatively simple to create a generic blackboard
# orchestrator which only ever needs testing once, and if it
# arrives in a python package will already have been tested by
# its creator.