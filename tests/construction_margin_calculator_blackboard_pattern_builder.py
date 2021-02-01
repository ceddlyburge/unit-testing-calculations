from cash_flow_calculator.construction_margin_calculator_blackboard_pattern import ConstructionMarginCalculatorBlackboardPattern
from tests.mock_inflation import MockInflation

any_double = 5.55555

class ConstructionMarginCalculatorBlackboardPatternBuilder:

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


