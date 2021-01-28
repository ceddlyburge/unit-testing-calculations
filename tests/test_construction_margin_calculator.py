from datetime import datetime
from typing import List
from dataclasses import dataclass
from cash_flow_calculator.cash_flow_step import CashFlowStep
from cash_flow_calculator.construction_margin_calculator import ConstructionMarginCalculator

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

    sut = ConstructionMarginCalculator(
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

    assert cash_flow_step.special_capital_costs == 13
    assert cash_flow_step.development_cost_if_owning == None
    assert cash_flow_step.development_cost == 11
    assert cash_flow_step.turbine_cost_including_margin == 3.96
    assert cash_flow_step.balance_of_plant_cost_including_margin == 3.3000000000000003
    assert cash_flow_step.construction_profit == -0.66

