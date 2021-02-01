from datetime import datetime
from cash_flow_calculator.cash_flow_step import CashFlowStep
from cash_flow_calculator.construction_margin_calculator_without_loop import (
    ConstructionMarginCalculatorWithoutLoop, 
    CashFlowStepsCalculator)


# The function now has 2^7 (128) paths in total, much less that the initial 2^9 (512) paths, 
# as the loop is done elsewhere. The loop might still want testing, but it now
# probably only needs 3 or so tests, rather 
def test_calculate_step_sets_correct_values():
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

    sut = ConstructionMarginCalculatorWithoutLoop(
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

    sut.calculate_step(cash_flow_step, fraction_of_spend)

    assert cash_flow_step.special_capital_costs == 13
    assert cash_flow_step.development_cost_if_owning == None
    assert cash_flow_step.development_cost == 11
    assert cash_flow_step.turbine_cost_including_margin == 3.96
    assert cash_flow_step.balance_of_plant_cost_including_margin == 3.3000000000000003
    assert cash_flow_step.construction_profit == -0.66


# This code tests the CashFlowStepsCalculator, which is arguably unecessary, being as it
# is so simple. There is more code here than in the original solution, but it does remove
# ~400 potential paths through the code, so hopefully the benefit is clear.
class MockSpecialCapitalCostAsFractionOfSpendCalculator:
    def calculate_step(self, step: CashFlowStep, fraction_of_spend: float):
        step.special_capital_costs = fraction_of_spend


def test_calculate_steps_calculator_calculates_one_step():
    fraction_of_spend = 0.3
    date_of_financial_close = datetime(2020, 1, 1)
    cash_flow_step = CashFlowStep(date_of_financial_close, None, None, None, None, None, None, None)
    mock_calculator = MockSpecialCapitalCostAsFractionOfSpendCalculator()

    sut = CashFlowStepsCalculator([cash_flow_step])
    sut.calculate_step(mock_calculator, fraction_of_spend)

    assert cash_flow_step.special_capital_costs == fraction_of_spend
