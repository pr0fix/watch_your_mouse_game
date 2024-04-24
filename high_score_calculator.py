def save_high_score(score):
    try:
        with open("high_scores.txt", "r") as file:
            highest_score = file.read().strip()
            if highest_score == "":
                with open("high_scores.txt", "w") as file:
                    file.write(str(score))
            elif score > int(highest_score):
                with open("high_scores.txt", "w") as file:
                    file.write(str(score))
    except FileNotFoundError:
        highest_score = 0

def get_high_score():
    try:
        with open("high_scores.txt", "r") as file:
            highest_score = file.read().strip()
            if highest_score:
                return int(highest_score)
            else:
                return 0
    except FileNotFoundError:
        return 0