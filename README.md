# Unit testing complicated calculations

[![Build status](https://ci.appveyor.com/api/projects/status/4k40ogfs5yv4rftf?svg=true)](https://ci.appveyor.com/project/ceddlyburge/unit-testing-calculations)

This repository contains the example code for a blog post on unit testing complicated calculations.

It is good to make tests as descriptive as possible, to achieve [Tests as Documentation](http://xunitpatterns.com/Goals%20of%20Test%20Automation.html#Tests%20as%20Documentation). Including the calculations in the test is a big part of this, and avoids the [Hard Coded Test Data](http://xunitpatterns.com/Obscure%20Test.html#Hard-Coded%20Test%20Data) smell.

This example code has an [initial naive test](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/tests/test_construction_margin_calculator.py#L17), which is around 30 lines long. It doesn't include the calculations, and introducing them would make the test even longer and more complicated, so would be hard to justify.

The blog describes a series of refactorings, which  build on the existing [test refactorings](http://xunitpatterns.com/Test%20Refactorings.html) from [XUnit Test Patterns](https://www.goodreads.com/review/show/2179089513).

The refactorings reduce the number of paths through the code and simplify the test. This means that less tests are needed, and that the tests become small and simple enough to include the calculations.

## Extract Calculation From Loop

- [Refactored Calculation](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/cash_flow_calculator/construction_margin_calculator_without_loop.py#L31)
- [Refactored Test](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/tests/test_construction_margin_calculator_remove_loop.py#L11)

## Introduce Mockable Abstractions

- [Refactored Calculation](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/cash_flow_calculator/construction_margin_calculator_mockable_abstraction.py#L29)
- [Refactored Test](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/tests/test_construction_margin_calculator_mockable_abstraction.py#L11)

## Test Conditional Branches In Isolation

- [No Change to Calculation](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/cash_flow_calculator/construction_margin_calculator_mockable_abstraction.py#L29)
- [Refactored Test](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/tests/test_construction_margin_calculator_isolate_branches.py#L16)

## Test Values In Isolation

- [No Change to Calculation](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/cash_flow_calculator/construction_margin_calculator_mockable_abstraction.py#L29)
- [Refactored Test](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/tests/test_construction_margin_calculator_isolate_values.py#L18)

## Test Partial Values in Isolation

- [No Change to Calculation](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/cash_flow_calculator/construction_margin_calculator_mockable_abstraction.py#L29)
- [Refactored Test](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/tests/test_construction_margin_calculator_isolate_partial_values.py#L14)

## Introduce Blackboard Pattern

- [Refactored Calculation](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/cash_flow_calculator/construction_margin_calculator_blackboard_pattern.py#L15)
- [Refactored Test](https://github.com/ceddlyburge/unit-testing-calculations/blob/main/tests/test_construction_margin_calculator_blackboard_pattern.py#L12)