from datetime import datetime
from cash_flow_calculator.cash_flow_step import CashFlowStep
from tests.construction_margin_calculator_mockable_abstraction_builder import ConstructionMarginCalculatorMockableAbstractionBuilder
from tests.cash_flow_step_builder import CashFlowStepBuilder

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

    sut = ConstructionMarginCalculatorMockableAbstractionBuilder() \
        .with_balance_of_plant_costs_at_financial_close(balance_of_plant_costs_at_financial_close) \
        .with_inflation(inflation) \
        .with_epc_margin(epc_margin) \
        .in_selling_mode() \
        .build()

    cash_flow_step = CashFlowStepBuilder().build()

    sut.calculate_step(cash_flow_step, fraction_of_spend)

    assert cash_flow_step.balance_of_plant_cost_including_margin == (balance_of_plant_costs_at_financial_close * inflation * fraction_of_spend) * (1 + epc_margin)


# The code and test for the CashFlowStepsCalculator is no longer shown