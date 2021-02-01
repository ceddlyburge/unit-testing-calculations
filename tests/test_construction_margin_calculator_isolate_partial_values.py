from datetime import datetime
from cash_flow_calculator.cash_flow_step import CashFlowStep
from cash_flow_calculator.construction_margin_calculator_mockable_abstraction import ConstructionMarginCalculatorMockableAbstraction
from tests.mock_inflation import MockInflation
from tests.cash_flow_step_builder import CashFlowStepBuilder

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
    turbine_costs = 10
    balance_of_plant_costs_at_financial_close = 0
    fraction_of_spend = 0.3
    epc_margin = 0.1
    inflation = 1.2

    sut = ConstructionMarginCashFlowCostCalculatorBuilder() \
        .with_balance_of_plant_costs_at_financial_close(balance_of_plant_costs_at_financial_close) \
        .with_turbine_costs(turbine_costs) \
        .with_inflation(inflation) \
        .with_epc_margin(epc_margin) \
        .in_selling_mode() \
        .build()

    cash_flow_step = CashFlowStepBuilder().build()

    sut.calculate_step(cash_flow_step, fraction_of_spend)

    assert cash_flow_step.construction_profit == -1 * turbine_costs * inflation * fraction_of_spend * epc_margin


any_double = 5.55555

class ConstructionMarginCashFlowCostCalculatorBuilder:

    def __init__(self): 
        self._sut = ConstructionMarginCalculatorMockableAbstraction(
        balance_of_plant_costs_at_financial_close=any_double, 
        development_cost=any_double, 
        turbine_costs=any_double, 
        special_capital_costs=any_double, 
        date_of_financial_close=None, 
        in_selling_mode=None, 
        epc_margin=any_double, 
        inflation_calculator=MockInflation(any_double)
    )

    def with_turbine_costs(self, turbine_costs: float): 
        self._sut.turbine_costs = turbine_costs
        return self

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


# The code and test for the CashFlowStepsCalculator is no longer shown