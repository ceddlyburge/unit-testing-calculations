from tests.construction_margin_calculator_mockable_abstraction_builder import ConstructionMarginCalculatorMockableAbstractionBuilder
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

    sut = ConstructionMarginCalculatorMockableAbstractionBuilder() \
        .with_balance_of_plant_costs_at_financial_close(balance_of_plant_costs_at_financial_close) \
        .with_turbine_costs(turbine_costs) \
        .with_inflation(inflation) \
        .with_epc_margin(epc_margin) \
        .in_selling_mode() \
        .build()

    cash_flow_step = CashFlowStepBuilder().build()

    sut.calculate_step(cash_flow_step, fraction_of_spend)

    assert cash_flow_step.construction_profit == -1 * turbine_costs * inflation * fraction_of_spend * epc_margin


# The test for the CashFlowStepsCalculator is no longer shown