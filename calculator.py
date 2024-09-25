def arithmetic_calculator(formula):
    try:
        result = eval(formula)
        return result
    except Exception as e:
        return str(e)

# Final test cases to ensure robustness
final_test_cases = [
    "2 ** 3",                         # Exponentiation
    "4 % 2",                          # Modulus
    "2 + 3 * 4 ** 2 / (1 - 5) ** 2",  # Mixed operations with different precedence
    "10 // 3",                        # Floor division
    "0 * 1 / 2 + 3 - 4",               # Zero multiplication
    "1 + 2 - 3 * 4 / 3 + 8"           # user test
]

for formula in final_test_cases:
    print(f"{formula} = {arithmetic_calculator(formula)}")
