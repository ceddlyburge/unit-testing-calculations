from cash_flow_calculator.cash_flow_step import CashFlowStep

any_double = 5.55555

class CashFlowStepBuilder:

    def __init__(self): 
        self._sut = CashFlowStep(
            start_of_step=None,
            special_capital_costs=any_double,
            development_cost_if_owning=any_double,
            development_cost=any_double,
            turbine_cost_including_margin=any_double,
            balance_of_plant_costs_at_financial_close=any_double,
            construction_profit=any_double,
            balance_of_plant_cost_including_margin=any_double)

    def with_turbine_cost_including_margin(self, turbine_cost_including_margin: float): 
        self._sut.turbine_cost_including_margin = turbine_cost_including_margin
        return self
    
    def with_balance_of_plant_cost_including_margin(self, balance_of_plant_cost_including_margin: float): 
        self._sut.balance_of_plant_cost_including_margin = balance_of_plant_cost_including_margin
        return self

    def build(self):
        return self._sut