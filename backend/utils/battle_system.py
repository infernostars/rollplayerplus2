def betterchester(a_initial, a_surrender, a_strength, b_initial, b_surrender, b_strength, exponent): return [(a_initial ** exponent - (b_strength / a_strength * b_initial ** exponent) + (b_strength / a_strength * b_surrender ** exponent)) ** (1 / exponent), (b_initial ** exponent - (a_strength / b_strength * a_initial ** exponent) + (a_strength / b_strength * a_surrender ** exponent)) ** (1 / exponent)]