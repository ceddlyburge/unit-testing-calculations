from datetime import datetime
from cash_flow_calculator.cash_flow_step import CashFlowStep
from cash_flow_calculator.construction_margin_calculator_mockable_abstraction import ConstructionMarginCalculatorMockableAbstraction
from tests.mock_inflation import MockInflation

any_double = 5.55555

# Manipulating the conditionals so that most of them are false allows us to test
# small parts of the function in isolation, which makes the tests a lot simpler,
# and makes it feasible to include the calculation in the test, and to give the
# test a better name.
# The test is now more expressive and  clearly communicates how the calculations 
# should be performed (for example, that the turbine_cost_including_margin should
# be the turbine_costs * fraction_of_spend * inflation)
# There should obvioulsy be more tests like this, but only one is shown for 
# simplicity.
def test_calculates_turbine_cost_including_margin_correctly():
    not_in_selling_mode = False
    turbine_costs = 12
    balance_of_plant_costs_at_financial_close = 10
    fraction_of_spend = 0.3
    inflation = 2
    date_of_financial_close = datetime(2020, 1, 1)
    not_date_of_financial_close = datetime(2020, 1, 2)

    sut = ConstructionMarginCalculatorMockableAbstraction(
        balance_of_plant_costs_at_financial_close, 
        any_double, 
        turbine_costs, 
        any_double, 
        date_of_financial_close, 
        not_in_selling_mode, 
        any_double, 
        MockInflation(inflation), 
    )

    cash_flow_step = CashFlowStep(not_date_of_financial_close, any_double, any_double, any_double, any_double, any_double, any_double, any_double)

    sut.calculate_step(cash_flow_step, fraction_of_spend)

    assert cash_flow_step.turbine_cost_including_margin == turbine_costs * fraction_of_spend * inflation
    assert cash_flow_step.balance_of_plant_cost_including_margin == balance_of_plant_costs_at_financial_close * inflation * fraction_of_spend


# The code and test for the CashFlowStepsCalculator is no longer shown