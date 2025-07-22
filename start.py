import time
import sys
import func



welcome_art = r"""

  __  __         _    _             ______             
 |  \/  |       | |  | |           |  ____|            
 | \  / |  __ _ | |_ | |__  ______ | |__  _   _  _ __  
 | |\/| | / _` || __|| '_ \|______||  __|| | | || '_ \ 
 | |  | || (_| || |_ | | | |       | |   | |_| || | | |
 |_|  |_| \__,_| \__||_| |_|       |_|    \__,_||_| |_|
                                                       
                                                       
Welcome to Math-Fun, the terminal-based quiz game!
"""

print(welcome_art)

while True:

    #welcome interface
    name = func.get("name")
    if name:
        print(f"-------------------------\nHello, {name}! Let's get started.")
    else:
        name = input("Please enter your name: ")
        if name.strip() == "":
            print("Name cannot be empty. Please enter a valid name.")
            continue
        func.update("name", name)
        print(f"-------------------------\nHello, {name}! Let's get started.")


    cmd = input("Enter command or help to know more: ")
    
    cmd = cmd.strip().lower()
    cmd_1 = cmd.split(' ')[0]  # first word 
    if cmd_1 == 'exit':
        print("Goodbye!")
        sys.exit()

    
    elif cmd_1 == 'help':
        help = '''
Commands:
1. start : to start game. 
2. lvl : save your game level ( default: 1)
3. game : save your game type ( default: classic).
4. config : to see your current config.
5. reset: to reset profile and config.
6. time_limit : set your time limit for timed game (default: 3.5 seconds).
7. quiz_amount : set the amount of questions you want to answer (default: 10).
8. digit: set the number of max digits in the questions (default: 2 which means you get expressions in 1 to 99 range.)
9. exit : to exit the game. 

------------------------------------
            
'''
        print(help)
        
    elif cmd_1 == 'reset':
        print("Resetting profile and stats...")
        func.reset()
        print("Profile and stats reset successfully.")
        continue



    elif cmd_1 == 'lvl':  
        level = input('''We have 21 game levels. Where we have quiz types as follows:
                      
1. Even or Odd  
2. Addition  
3. Subtraction  
4. Multiplication  
5. Division  
6. Mixed Operations (+, -, ×, ÷)  
7. Sum of Digits : (Keep 2 digit minimum. [cmd: digit])
8. Reverse a Number : (Keep 2 digit minimum. [cmd: digit])
9. Place Value : (Keep 2 digit minimum. [cmd: digit])
10. Rounding (Nearest Ten/Hundred/Thousand): (Keep 2 digit minimum. [cmd: digit])
11. Greater or Less Than  
12. Ordering Numbers  
13. Fill in the Blank  
14. Simple Algebraic Expression 
15. Square and Square Root  
16. Factors : answer it by separating with ,
17. Prime Factorization  : answer it by separating with  ,
18. Adding/Subtracting Fractions  : Provide the simplified final answer.
19. Decimal Addition/Subtraction  
20. Percentage  
21. Word Problems

Enter your game level (default is 1): ''')
        
        if level.strip() == "":
            level = 1
        else:
            try:
                level = int(level)
                if level < 1 or level > 21:
                    raise ValueError("Level must be between 1 and 21.")
                else:
                    func.update("level", level)
                    print(f"Game level set to {level}.")
            except ValueError as e:
                print(f"Invalid input: {e}. Setting level to default (1).")
                level = 1
        
        
        
        
        
    elif cmd_1 == 'game':
        typ = input('''We have 3 game types.
1. classic: you solve 10 (or given) amount of questions. on finish you will get your accuracy and time taken.
2. check: you only move to next question if you answer correctly. you get your performance stats at the end.
3. timed: you have a limited time for each question, it moves to next question itself if you don't answer in time.

Enter your game type (default is classic):
''')
        if typ.strip() == "":
            typ = "classic"
        else:
            typ = typ.strip().lower()
            if typ not in ('classic', 'check', 'timed'):
                print("Invalid game type. Setting to default (classic).")
                typ = "classic"
        
        func.update("game", typ)
        print(f"Game type set to {typ}.")
        
    elif cmd_1 == 'config':
        stats = {
            "name": func.get("name"),
            "level": func.get("level"),
            "game_type": func.get("game"),
            "time_limit": func.get("time_limit"),
            "quiz_amount": func.get("quiz_amount"),
            "digit_number": func.get("digit_in_number")
        }
        
        print("\nYour config:")
        for key, value in stats.items():
            print(f"{key.capitalize()}: {value}")
        print()

    elif cmd_1 == 'time_limit':
        time_limit = input("Enter your time limit in seconds (default is 3.5): ")
        
        try:
            time_limit = float(time_limit)
            if time_limit <= 0:
                raise ValueError("Time limit must be a positive number.")
        except ValueError as e:
            print(f"Invalid input: Setting time limit to default (3.5 seconds).")
            time_limit = 3.5
            
            
        func.update("time_limit", time_limit)
        print(f"Time limit set to {time_limit} seconds.")
        
    elif cmd_1 == 'quiz_amount':
        quiz_amount = input("Enter the number of questions you want to answer (default is 10): ")
        
        try:
            quiz_amount = int(quiz_amount)
            if quiz_amount <= 0:
                raise ValueError("Quiz amount must be a positive integer.")
        except ValueError as e:
            print(f"Invalid input: Setting quiz amount to default (10).")
            quiz_amount = 10
            
        func.update("quiz_amount", quiz_amount)
        print(f"Quiz amount set to {quiz_amount}.")
        
        
    elif cmd_1 == 'digit':
        digit = input("The more digits you set, the greater the difficulty.\nFor example, if you choose 3 digits, you might get expressions like: 259 + 986.\nSo, set it carefully.\n\nEnter the number of digits in the questions (default is 2): ")
        
        try:
            digit = int(digit)
            if digit <= 0:
                raise ValueError("Digit must be a positive integer.")
        except ValueError as e:
            print(f"Invalid input: Setting digit to default (2).")
            digit = 2
            
        func.update("digit_in_number", digit)
        print(f"Digit set to {digit}.")
        
        
    elif cmd_1 == 'start':
        qn = func.generate_math_questions(func.get("quiz_amount"),func.get("digit_in_number"), func.get("level"))
   
        
        print("Let's go.. ")
        
        
        
       
        
        
        if(func.get("game") == "classic"):
            print("You will be asked 10 questions.. your time starts now!\n______________________________\n_______________________")
            start_time = time.time()
            
            answer_book = []
            
            for question in qn:
                q_sr = question['sr']
                q = question['question']
                crt_answer = question['answer']
                
                print(f"({q_sr}.)       {q}")
                input_answer = input("Your answer: ")
                answer_book.append({'sr': q_sr, 'question': q, 'your_answer': input_answer, 'correct_answer': crt_answer})
                
            end_time = time.time()
            elapsed_time = end_time - start_time
       
            res = func.analyse_list(answer_book)
            print(f"\nCorrect: {res[0]}, Incorrect: {res[1]}\nLvl:{func.get('level')}, Difficulty: {func.get('digit_in_number')}x \nTime taken: {elapsed_time:.2f} seconds")
    
        
            
        elif(func.get("game") == "check"):
            print("You will be asked 10 questions. You must answer each correctly to move on.\n______________________________\n_______________________")
            start_time = time.time()
       
            incorrect_attempts = 0
            for question in qn:
                q_sr = question['sr']
                q = question['question']
                crt_answer = question['answer']
                while True:
                    print(f"({q_sr}.)       {q}")
                    input_answer = input("Your answer: ")
                   
                    if func.check_answer(input_answer, crt_answer):
                        print("Correct!\n")
                        break
                    else:
                        print("Incorrect. Try again.\n")
                        incorrect_attempts += 1
                    
                        
                        
                        
                        
            # when for loop ends , we can safely assume all questions were answered correctly. 
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            print(f"\nDone. \nIncorrect attempts: {incorrect_attempts}\nLvl:{func.get('level')}, Difficulty: {func.get('digit_in_number')}x \nTime taken: {elapsed_time:.2f} seconds")
            
            
            
            
            
            
            
        elif(func.get("game") == "timed"):
            
            from inputimeout import inputimeout, TimeoutOccurred
            your_time = float(func.get("time_limit")) if func.get("time_limit") else 4
            print(f"You will be asked 10 questions. You have {your_time} seconds to answer each question.\n______________________________\n_______________________")
            
            
            answer_book = []
            
            for question in qn:
                q_sr = question['sr']
                q = question['question']
                crt_answer = question['answer']
                
                print(f"({q_sr}.)       {q}")
                
                try:
                    input_answer = inputimeout(prompt="Your answer:  ", timeout=your_time)
                    
                except TimeoutOccurred:
                    print(":( Time is up.")
                    input_answer=None
                
            
                answer_book.append({'sr': q_sr, 'question': q, 'your_answer': input_answer, 'correct_answer': crt_answer})
                
       
            res = func.analyse_list(answer_book)
            print(f"\nCorrect: {res[0]}, Incorrect: {res[1]}\nLvl:{func.get('level')}, Difficulty: {func.get('digit_in_number')}x\n")
            print(f"Accuracy: {res[0] / (res[0] + res[1]) * 100:.2f}% \nYou can raise or lower your time limit with time_limit command.")
        