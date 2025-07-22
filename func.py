import random
import math
from fractions import Fraction
from decimal import Decimal, getcontext
import json
import os


def generate_number(digits):
    if digits == 1:
        return random.randint(1, 9)
    else:
        return random.randint(10**(digits-1), 10**digits-1)

def factors(n):
    return sorted(set(f for i in range(1, int(n**0.5)+1) if n % i == 0 for f in (i, n//i)))

def prime_factors(n):
    i, result = 2, []
    while i*i <= n:
        if n % i == 0:
            result.append(i)
            n //= i
        else:
            i += 1
    if n > 1: result.append(n)
    return result

def gen_fraction(digits):
    denom = random.randint(2, 9)
    numer = random.randint(1, denom-1)
    return Fraction(numer, denom)

WORD_PROBLEM_CATEGORIES = {
    "multiplication": {
        "templates": [
            "If you buy {n1} {item1} and each costs {n2} {currency}, what's the total?",
            "{n1} {item1} cost {n2} {currency} each. How much for all?",
            "Each {item2} holds {n1} {item3}. How many {item3} in {n2} {item2}?",
            "You need {n1} {item3} per {item2}. How many for {n2} {item2}?"
        ],
        "answer": lambda n1, n2: n1 * n2,
        "items": {
            "item1": ["apples", "books", "pens", "toys", "chairs"],
            "item2": ["boxes", "bags", "crates", "containers"],
            "item3": ["cookies", "marbles", "stickers", "cards"],
            "currency": ["dollars", "points", "coins"]
        }
    },
    "addition": {
        "templates": [
            "You have {n1} {item1} and get {n2} more. How many total?",
            "In one {item2} there are {n1} {item3}, in another {n2}. Total?",
            "First day you collect {n1} {item1}, second day {n2}. How many altogether?"
        ],
        "answer": lambda n1, n2: n1 + n2,
        "items": {
            "item1": ["stickers", "coins", "stamps", "cards"],
            "item2": ["box", "jar", "bag", "container"],
            "item3": ["toys", "books", "pencils", "erasers"]
        }
    },
    "subtraction": {
        "templates": [
            "You had {n1} {item1} and gave away {n2}. How many left?",
            "A {item2} contained {n1} {item3}. You removed {n2}. What remains?",
            "Starting with {n1} {item1}, you used {n2}. How many unused?"
        ],
        "answer": lambda n1, n2: n1 - n2,
        "items": {
            "item1": ["candies", "marbles", "stickers", "coins"],
            "item2": ["box", "bag", "jar", "basket"],
            "item3": ["toys", "books", "balls", "cards"]
        }
    }
}

def generate_word_problem(digits, category=None):
    if not category:
        category = random.choice(list(WORD_PROBLEM_CATEGORIES.keys()))
    
    cat_data = WORD_PROBLEM_CATEGORIES[category]
    template = random.choice(cat_data["templates"])
    
    # Generate numbers ensuring valid results
    n1 = generate_number(digits)
    n2 = generate_number(digits)
    
    # Fix numbers based on operation
    if category == "subtraction" and n2 > n1:
        n1, n2 = n2, n1
    
    # Random word substitutions
    placeholders = {}
    for key, options in cat_data["items"].items():
        placeholders[key] = random.choice(options)
    
    question = template.format(n1=n1, n2=n2, **placeholders)
    answer = cat_data["answer"](n1, n2)
    
    return {'question': question, 'answer': answer}





def generate_math_questions(num_questions, digits, level):
    questions = []
    for sr in range(1, num_questions+1):
        if level == 1:  # Even or Odd
            n = generate_number(digits)
            q = f"Is {n} even or odd?"
            a = "even" if n % 2 == 0 else "odd"
            
            
        elif level == 2:  # Addition
            a1, a2 = generate_number(digits), generate_number(digits)
            q = f"{a1} + {a2}"
            a = a1 + a2
            
            
        elif level == 3:  # Subtraction
            a1, a2 = generate_number(digits), generate_number(digits)
            a1, a2 = max(a1, a2), min(a1, a2)
            q = f"{a1} - {a2}"
            a = a1 - a2
            
            
        elif level == 4:  # Multiplication
            a1, a2 = generate_number(digits), generate_number(digits)
            q = f"{a1} × {a2}"
            a = a1 * a2
            
        elif level == 5:  # Division
            b = generate_number(digits)
            a = b * generate_number(digits)
            q = f"{a} ÷ {b}"
            ans = a // b
            a = ans
            
        elif level == 6:  # Mixed (+, -, ×, ÷)
            # For each question, pick a random operation (2: add, 3: sub, 4: mul, 5: div)
            op = random.choice([2, 3, 4, 5])
            # Generate a single question of the chosen type
            mixed_q = generate_math_questions(1, digits, op)[0]
            q = mixed_q['question']
            a = mixed_q['answer']
            
            
        elif level == 7:  # Sum of digits
            n = generate_number(digits)
            q = f"Sum the digits of {n}"
            a = sum(map(int, str(n)))
            
            
        elif level == 8:  # Reverse a number
            n = generate_number(digits)
            q = f"Reverse the number {n}"
            a = int(str(n)[::-1])
            
            
        elif level == 9:  # Place value
            n = generate_number(digits)
            n_str = str(n)
            places = ["ones", "tens", "hundreds", "thousands", "ten thousands", "hundred thousands", "millions"]
            if len(n_str) > len(places):
                place_names = ["digit"] * len(n_str)
            else:
                place_names = places[:len(n_str)][::-1]
            pos = random.randint(0, len(n_str)-1)
            place = place_names[pos]
            q = f"What digit is at the {place} place in {n}?"
            a = n_str[pos]
            
            
        elif level == 10:  # Rounding
            n = generate_number(digits)
            round_to = random.choice([10, 100, 1000][:digits])
            q = f"Round {n} to the nearest {round_to}"
            a = round(n, -int(math.log10(round_to)))
            
            
        elif level == 11:  # Greater or Less Than
            a1, a2 = generate_number(digits), generate_number(digits)
            comp = random.choice(["greater", "less"])
            if comp == "greater":
                q = f"Which is greater: {a1} or {a2}?"
                a = a1 if a1 > a2 else a2
            else:
                q = f"Which is less: {a1} or {a2}?"
                a = a1 if a1 < a2 else a2

        elif level == 12:  # Ordering Numbers
            items = [generate_number(digits) for _ in range(random.choice([3,4,5]))]
            order_type = random.choice(["ascending", "descending"])
            q = f"Arrange in {order_type} order: {', '.join(map(str, items))}"
            if order_type == "ascending":
                a = ', '.join(map(str, sorted(items)))
            else:
                a = ', '.join(map(str, sorted(items, reverse=True)))
            
            
        elif level == 13:  # Fill in the Blank
            a1 = generate_number(digits)
            a2 = generate_number(digits)
            if random.choice(['+', '-']) == '+':
                total = a1 + a2
                if random.choice([True, False]):
                    q = f"{a1} + ___ = {total}"
                    a = a2
                else:
                    q = f"___ + {a2} = {total}"
                    a = a1
            else:
                total = a1 - a2
                if random.choice([True, False]):
                    q = f"{a1} - ___ = {total}"
                    a = a2
                else:
                    q = f"___ - {a2} = {total}"
                    a = a1
                
        elif level == 14:  # Algebraic Equations
            op = random.choice(['+', '-', '*', '/'])
            x = generate_number(digits)
            if op == '+':
                addend = random.randint(1, 10)
                r = x + addend
                q = f"If x + {addend} = {r}, what is x?"
                a = x
            elif op == '-':
                subtrahend = random.randint(1, x)
                r = x - subtrahend
                q = f"If x - {subtrahend} = {r}, what is x?"
                a = x
            elif op == '*':
                multiplier = random.randint(2, 10)
                r = x * multiplier
                q = f"If x × {multiplier} = {r}, what is x?"
                a = x
            elif op == '/':
                divisor = random.randint(2, 10)
                r = x
                x_times_divisor = x * divisor
                q = f"If x ÷ {divisor} = {r}, what is x?"
                a = x_times_divisor
            
        elif level == 15:  # Square and Square Root
            if random.choice([True, False]):
                a1 = generate_number(digits)
                q = f"What is {a1}²?"
                a = a1**2
            else:
                a1 = generate_number(digits)
                q = f"√{a1*a1}"
                a = a1
                
                
        elif level == 16:  # Factors 
            n = generate_number(digits)
            q = f"List all factors of {n}"
            a = ', '.join(map(str, factors(n)))
            
            
        elif level == 17:  # Prime Factorization
            n = generate_number(digits)
            while n < 2:
                n = generate_number(digits)
            q = f"What are the prime factorization  of {n}?"
            pf = prime_factors(n)
            a = ','.join(map(str, pf))
            
            
        elif level == 18:  # Adding/Subtracting Fractions
            f1, f2 = gen_fraction(digits), gen_fraction(digits)
            if random.choice([True, False]):
                q = f"{f1} + {f2}"
                a = f1 + f2
            else:
                q = f"{f1} - {f2}"
                a = f1 - f2
                
                
        elif level == 19:  # Decimal Addition/Subtraction
            a1 = round(random.uniform(1, 10**digits), digits)
            a2 = round(random.uniform(1, 10**digits), digits)
            
            a1 = Decimal(str(a1))
            a2 = Decimal(str(a2))
            
            if random.choice([True, False]):
                q = f"{a1} + {a2}"
                a = a1 + a2
            else:
                q = f"{a1} - {a2}"
                a = a1 - a2
                
        elif level == 20:  # Percentage
         
            multiples = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
            a1 = random.choice(multiples) * (10 ** (digits-3)) if digits > 2 else random.choice([100, 200, 300, 400, 500])
            percent_choices = [5, 10, 20, 25, 50, 100]
            percent = random.choice(percent_choices)
            q = f"What is {percent}% of {a1}?"
            a = a1 * percent // 100
            
            
        elif level == 21:
            res = generate_word_problem(digits)
            q = res['question']
            a = res['answer']
            
            
            
            
            
            
        else:
            q, a = "Invalid level selected", None

        questions.append({'sr': sr, 'question': q, 'answer': str(a)})
    return questions









def check_answer(user_ans, correct_ans,question_type=0):
    # Skip if no answer provided
    if user_ans is None or user_ans == "":
        return False

    user_str = str(user_ans).strip().lower()
    correct_str = str(correct_ans).strip().lower()

    # Direct string comparison first
    if user_str == correct_str:
        return True

    # Handle 'factors and other answer with comma' 
    if ',' in user_str or ',' in correct_str:
        try:
            user_factors = [int(x.strip()) for x in user_str.split(',') if x.strip()]
            correct_factors = [int(x.strip()) for x in correct_str.split(',') if x.strip()]
            return user_factors == correct_factors
        except ValueError:
            return False
    else:
        # Try float comparison
        try:
            return float(user_str) == float(correct_str)
        except ValueError:
            return False
        
        

def analyse_list(answer_book):
    correct = 0
    incorrect = 0
    for answer in answer_book:
        try:
            user_ans = answer['your_answer']
            correct_ans = answer['correct_answer']
            if check_answer(user_ans, correct_ans):
                correct += 1
            else:
                incorrect += 1
        except Exception:
            incorrect += 1
    return correct, incorrect









user_file = "user.json"


def update(key, value):

    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    #update or add 
    data[key] = value

    # Save
    with open(user_file, "w") as f:
        json.dump(data, f, indent=4)

def get(key):
    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    return data.get(key)

def reset():
    default_values = {
        "level": 1,
        "name": 0,
        "game": "classic",
        "time_limit": 3.5,
        "quiz_amount": 10,
        "digit_in_number": 2
    }
    with open(user_file, "w") as f:
        json.dump(default_values, f, indent=4)



