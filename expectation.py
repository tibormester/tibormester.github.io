def calculate_expectation(n, m = 100):
    expectation = 0
    for i in range(1, m + 1):
        expectation += (-1) ** (i - 1) * combination(m, i) * ((1 - i / m) ** n)
    return expectation

def find_max_m(target_expectation, n):
    low, high = 1, 1000  # Set an initial range for binary search
    epsilon = 0.001  # Tolerance for precision

    while high - low > epsilon:
        mid = (low + high) / 2
        expectation = calculate_expectation(int(mid))

        if expectation < target_expectation:
            high = mid
        else:
            low = mid

    return int(low)

def factorial(x):
    if x > 0:
        return x * factorial(x-1)
    else:
        return 1
    
def combination(n, r):
    return factorial(n) / (factorial(n - r)* factorial(r))
        
# Example usage for m = 100 and target expectation = 50.0
max_m = find_max_m(50.0, 100)
print("The largest n for which the expectation is at least 50.0:", max_m)