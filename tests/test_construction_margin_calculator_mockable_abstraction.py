from datetime import datetime
from cash_flow_calculator.cash_flow_step import CashFlowStep
from cash_flow_calculator.construction_margin_calculator_mockable_abstraction import ConstructionMarginCalculatorMockableAbstraction
from tests.mock_inflation import MockInflation

# Using a mock for the inflation removes the 4 code paths through the inflation code, 
# so with the removal of the loop, the function now has 2^3 (8) paths in total, much
# less that the initial 2^9 (512)!
# It is also easier to test everything, as the inflation is a separate and simple
# calculation
def test_calculate_step_sets_correct_values():
    balance_of_plant_costs_at_financial_close = 10
    development_cost = 11
    turbine_costs = 12
    special_capital_costs = 13
    date_of_financial_close = datetime(2020, 1, 1)
    in_selling_mode = True
    epc_margin = 0.1
    inflation = 1
    fraction_of_spend = 0.3

    sut = ConstructionMarginCalculatorMockableAbstraction(
        balance_of_plant_costs_at_financial_close, 
        development_cost, 
        turbine_costs, 
        special_capital_costs, 
        date_of_financial_close, 
        in_selling_mode, 
        epc_margin, 
        MockInflation(inflation)
    )

    cash_flow_step = CashFlowStep(date_of_financial_close, None, None, None, None, None, None, None)

    sut.calculate_step(cash_flow_step, fraction_of_spend)

    assert cash_flow_step.special_capital_costs == 13
    assert cash_flow_step.development_cost_if_owning == None
    assert cash_flow_step.development_cost == 11
    assert cash_flow_step.turbine_cost_including_margin == 3.96
    assert cash_flow_step.balance_of_plant_cost_including_margin == 3.3000000000000003
    assert cash_flow_step.construction_profit == -0.66

# The test for the CashFlowStepsCalculator is no longer shown