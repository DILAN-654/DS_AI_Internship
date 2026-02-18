# Probability of rolling a 4 on a fair die
favorable = 1
total_outcomes = 6
probability = favorable / total_outcomes
print(probability)

# Independent events example
p_rain = 0.3
p_traffic = 0.2
p_both = p_rain * p_traffic
print(p_both)

# Conditional probability example
p_A_and_B = 0.1
p_B = 0.4
p_A_given_B = p_A_and_B / p_B
print(p_A_given_B)

# Bayes' theorem example
p_disease = 0.01
p_positive_given_disease = 0.9
p_positive = 0.05

p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive
print(p_disease_given_positive)

#we have two boxes each comnatains 10 balls with random colors (blue and red)
#the probablity of picking 3 balls randomly from each box in round basis
#the probablity of picking red given at least one is blue from each box