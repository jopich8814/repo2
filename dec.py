import random
def print_scores(name,*scores, match):
    print(f'student name : {name}')
    for score in scores:
        print(score)
        print(match)

print_scores("egor", 15, 40, 40, 70)
