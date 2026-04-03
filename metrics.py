def calculate_metrics(money, product, team):
    health = money + product * 10 + team * 5

    if health > 150:
        status = "Excellent"
    elif health > 100:
        status = "Good"
    elif health > 50:
        status = "Average"
    else:
        status = "Bad"

    return health, status
