from tests.construction_margin_calculator_blackboard_pattern_builder import ConstructionMarginCalculatorBlackboardPatternBuilder
from tests.cash_flow_step_builder import CashFlowStepBuilder

# Now that we are using the blackboard pattern, the entire calculation for 
# construction_profit can be included in the test quite easily, and without
# making it too complicated.
# This is because we have broken the dependency between the construction_profit
# calculation and the balance_of_plant_cost_including_margin and 
# turbine_cost_including_margin calculations (by using the blackboard pattern)
# There should obvioulsy be more tests like this, but only one is shown for 
# simplicity. 
def test_construction_profit_calculated_correctly():
    turbine_cost_including_margin = 10
    balance_of_plant_cost_including_margin = 11
    fraction_of_spend = 0.3
    epc_margin = 0.1

    sut = ConstructionMarginCalculatorBlackboardPatternBuilder() \
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

# The test for the CashFlowStepsCalculator is no longer shown