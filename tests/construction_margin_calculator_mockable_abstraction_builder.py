from cash_flow_calculator.construction_margin_calculator_mockable_abstraction import ConstructionMarginCalculatorMockableAbstraction
from tests.mock_inflation import MockInflation

any_double = 5.55555

class ConstructionMarginCalculatorMockableAbstractionBuilder:

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

    def with_balance_of_plant_costs_at_financial_close(self, balance_of_plant_costs_at_financial_close: float): 
        self._sut.balance_of_plant_costs_at_financial_close = balance_of_plant_costs_at_financial_close
        return self

    def with_turbine_costs(self, turbine_costs: float): 
        self._sut.turbine_costs = turbine_costs
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