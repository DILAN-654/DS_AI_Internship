P_heads = 1/2
P_six = 1/6
P_heads_and_six = P_heads * P_six
print("Independent Event Probability (Heads AND 6):",P_heads_and_six)
red = 5
blue = 5
total = red + blue
P_first_red = red / total
P_second_red = (red - 1) / (total - 1)
P_both_red = P_first_red * P_second_red
print("Dependent Event Probability (Both Red):",P_both_red)
print("The denominator changes because after picking the first marble,")
print("The total number of marbles decreases from 10 to 9 (no replacement).")