#!/usr/bin/python3

import itertools
import zxcvbn
import os
import datetime
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from termcolor import colored

file_lock = multiprocessing.Lock()

def calculate_password_strength(password):
    result = zxcvbn.zxcvbn(password)
    return result['score']

def append_password_to_file(password, strength):
    file_name = ""
    if strength == 0:
        file_name = "weak.txt"
    elif strength == 1:
        file_name = "average.txt"
    elif strength == 2 or strength == 3:
        file_name = "strong.txt"
    else:
        file_name = "verystrong.txt"

    with file_lock:
        with open(file_name, "a") as file:
            file.write(password + "\n")
            
def delete_files(password_files):
    for password_file in password_files:
        if os.path.exists(password_file):
            os.remove(password_file)

def process_combination(combination):

    password_results = set()
    password = ''.join(combination)
    password_results.add(password)

    for num in range(0, 100):
        generated_passwords = [
            password + str(num),
            password.capitalize() + str(num),
            password + "_" + str(num),
            password.capitalize() + "_" + str(num),
            password + str(num) + "!",
            password.capitalize() + str(num) + "!"
        ]
        password_results.update(generated_passwords)

    special_chars = ["!", "@", "#", "$", "%", "&", "*", "(", ")", "-", "_", "=", "+", ",", ".", "?", "1!", "!@#", "123!@#"]
    generated_passwords = [
        password + char
        for char in special_chars
    ] + [
        password.capitalize() + char
        for char in special_chars
    ]
    password_results.update(generated_passwords)

    capitalized_password = password.capitalize()
    password_results.add(capitalized_password)

    replacements = {'s': '$', 'o': '0', 'a': '@'}
    replaced_password = ''.join(replacements.get(char.lower(), char) for char in password)
    password_results.add(replaced_password)

    reversed_password = ''.join(reversed(combination))
    password_results.add(reversed_password)

    repeated_password = ''.join(combination) * 2
    password_results.add(repeated_password)

    for num in range(1800, 2030):
        generated_passwords = [
            password + str(num),
            password.capitalize() + str(num),
            password + "_" + str(num),
            password.capitalize() + "_" + str(num),
            password + str(num) + "!",
            password.capitalize() + str(num) + "!"
        ]
        password_results.update(generated_passwords)
 
    return password_results

def generate_passwords(words):
    filtered_words = [word for word in words if word != ""]
    count = 0
    if not filtered_words:
        return 0

    def generate_password_combinations():
        password_combinations = []
        for r in range(1, len(filtered_words) + 1):
            word_combinations = itertools.permutations(filtered_words, r)
            password_combinations.extend(word_combinations)
        return password_combinations

    password_combinations = generate_password_combinations()
    num_processors = multiprocessing.cpu_count()

    pool = multiprocessing.Pool(processes=num_processors)
    passwords = pool.map(process_combination, password_combinations)

    pool.close()
    pool.join()

    unique_passwords = set()
    for password_set in passwords:
        unique_passwords.update(password_set)

    unique_passwords_list = list(unique_passwords)

    for password in unique_passwords_list:
        strength = calculate_password_strength(password)
        append_password_to_file(password, strength)
        count += 1

    return count
    
def get_user_info():
    info = {}
    print(colored("\nTarget Information Input:", "green"))
    print(colored("-------------------------", "green"))
    info['name'] = input(colored("Enter name: ", "cyan"))
    info['surname'] = input(colored("Enter surname: ", "cyan"))

    while True:
        birthday = input(colored("Enter birthday (DDMMYYYY): ", "cyan"))
        if len(birthday) == 0:
            break
        elif len(birthday) != 8 or not birthday.isdigit():
            print(colored("Invalid date format. Please enter the date as DDMMYYYY.", "red"))
        else:
            day = int(birthday[:2])
            month = int(birthday[2:4])
            year = int(birthday[4:])
            try:
                birthday = datetime.datetime(year, month, day).strftime("%d%m%Y")
                break
            except ValueError:
                print(colored("Invalid date. Please enter a valid date.", "red"))

    info['birthday'] = birthday
    info['nickname'] = input(colored("Enter nickname: ", "cyan"))

    info['father_name'] = input(colored("Enter father's name: ", "cyan"))
    info['mother_name'] = input(colored("Enter mother's name: ", "cyan"))
    while True:
        num_children_input = input(colored("Enter the number of children: ", "cyan"))
        if len(num_children_input) == 0:
            num_children = 0
            break
        elif not num_children_input.isdigit():
            print(colored("Invalid input. Please enter a valid number.", "red"))
        else:
            num_children = int(num_children_input)
            break

    info['children'] = []

    for i in range(num_children):
        child_info = {}
        print(colored(f"\nChild {i+1}", "blue"))
        child_info['name'] = input(colored("Enter child's name: ", "cyan"))
        child_info['nickname'] = input(colored("Enter child's nickname: ", "cyan"))

        while True:
            child_birthday = input(colored("Enter child's birthday (DDMMYYYY): ", "cyan"))
            if len(child_birthday) == 0:
                break
            elif len(child_birthday) != 8 or not child_birthday.isdigit():
                print(colored("Invalid date format. Please enter the date as DDMMYYYY.", "red"))
            else:
                day = int(child_birthday[:2])
                month = int(child_birthday[2:4])
                year = int(child_birthday[4:])
                try:
                    child_birthday = datetime.datetime(year, month, day).strftime("%d%m%Y")
                    break
                except ValueError:
                    print(colored("Invalid date. Please enter a valid date.", "red"))
        child_info['birthday'] = child_birthday
        info['children'].append(child_info)

    info['favorite_club'] = input(colored("Enter favorite football club: ", "cyan"))
    info['hobby'] = input(colored("Enter hobby: ", "cyan"))
    info['pet_name'] = input(colored("Enter pet's name: ", "cyan"))
    info['favorite_color'] = input(colored("Enter favorite color: ", "cyan"))
    info['extra_info'] = input(colored("Enter any extra information: ", "cyan"))

    return info


def print_user_info(info):
    print(colored("\nTarget Information Output:", "green"))
    print(colored("--------------------------", "green"))
 
    primary_fields = ['name', 'surname', 'birthday', 'nickname']
    print(colored("\nPersonal Details:", "blue"))
    print(colored("-----------------", "blue"))
    for field in primary_fields:
        if info[field]:
            print(colored(f"{field.capitalize()}: ", "cyan") + colored(info[field], "white"))

    family_fields = ['children', 'father_name', 'mother_name']
    print(colored("\nFamily Information:", "blue"))
    print(colored("-------------------", "blue"))
    for field in family_fields:
        if field == 'children':
            print(colored("Children:", "cyan"), len(info['children']))
            for i, child in enumerate(info['children']):
                print(colored(f"\nChild {i+1}:", "magenta"))
                for child_field, value in child.items():
                    if value:
                        print(colored(f"{child_field.capitalize()}: ", "cyan") + colored(value, "white"))
        elif info[field]:
            print(colored(f"{field.replace('_', ' ').capitalize()}: ", "cyan") + colored(info[field], "white"))

    secondary_fields = ['favorite_club', 'hobby', 'pet_name', 'favorite_color']
    print(colored("\nInterests and Preferences:", "blue"))
    print(colored("--------------------------", "blue"))
    for field in secondary_fields:
        if info[field]:
            #print(colored(f"{field.capitalize()}: ", "cyan") + colored(info[field], "white"))
            print(colored(f"{field.replace('_', ' ').capitalize()}: ", "cyan") + colored(info[field], "white"))
            
    extra_info = info.get('extra_info')
    if extra_info:
        print(colored("\nExtra Information:", "blue"))
        print(colored("------------------", "blue"))
        print(colored("Info:", "cyan"), colored(extra_info, "white"))
        
# Calculate total size of password files
def calculate_total_size(password_files):
    total_size = 0
    for password_file in password_files:
        if os.path.exists(password_file):
            total_size += os.path.getsize(password_file)
    # Convert size to megabytes
    total_size_mb = total_size / (1024 * 1024)
    return total_size_mb

# Calculate total number of combinations
def calculate_total_combinations(words):
    total_combinations = 0
    for r in range(1, len(words) + 1):
        total_combinations += len(list(itertools.permutations(words, r)))
    return total_combinations

def format_size(size):
    units = ["bytes", "KB", "MB", "GB", "TB"]
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:.2f}"
  
# Main program
if __name__ == "__main__":
    picture = colored("""
            
  ███╗   ███╗ ██████╗ ██████╗ ██████╗ ██╗  ██╗██╗ █████╗ ███╗   ██╗  
  ████╗ ████║██╔═══██╗██╔══██╗██╔══██╗██║  ██║██║██╔══██╗████╗  ██║  
  ██╔████╔██║██║   ██║██████╔╝██████╔╝███████║██║███████║██╔██╗ ██║  
  ██║╚██╔╝██║██║   ██║██╔══██╗██╔═══╝ ██╔══██║██║██╔══██║██║╚██╗██║  
  ██║ ╚═╝ ██║╚██████╔╝██║  ██║██║     ██║  ██║██║██║  ██║██║ ╚████║  
  ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝  
                                                                    
              Author: Christoforos Apostolopoulos                    
              Github: https://github.com/ApChris                     
              License: GNU General Public License v3.0                                                                        
    """, "yellow")

    print(picture)

    password_files = ["weak.txt", "average.txt", "strong.txt", "verystrong.txt"]
    total_combinations = 0
    total_size = 0
    delete_files(password_files)
 
    user_info = get_user_info()
    print_user_info(user_info)

    word_list_user = [user_info['name'], user_info['surname'], user_info['birthday'], user_info['nickname']]
    word_list_parents = [user_info['father_name'], user_info['mother_name']]
    word_list_preferences = [user_info['favorite_club'], user_info['hobby'], user_info['pet_name'], user_info['favorite_color']]
    word_list_children = []
    word_list_extra = [user_info['extra_info']]
    children_info = user_info.get('children', []) 


    print(colored("\nGenerating passwords...", "yellow"))
    start_time = time.time()

    with ProcessPoolExecutor() as executor:

        total_combinations += executor.submit(generate_passwords, word_list_user).result()

        total_combinations += executor.submit(generate_passwords, word_list_parents).result()
        total_combinations += executor.submit(generate_passwords, word_list_preferences).result()

        word_list_children = [(child['name'], child['birthday'], child['nickname']) for child in children_info]
        total_combinations += sum(executor.map(generate_passwords, word_list_children))

        total_combinations += executor.submit(generate_passwords, word_list_extra).result()

    print(colored("\nCompleted!", "green"))

    print(colored("\nGenerated passwords saved in the following text files:", "magenta"))
    for password_file in password_files:
        if os.path.exists(password_file):
            size = os.path.getsize(password_file)
            print(colored(f"{password_file} (Size: {colored(format_size(size), 'white')})", "cyan"))
            total_size += size

    print(colored("\nTotal Size:", "blue"), colored(format_size(total_size), "white"))

    print(colored("\nTotal Passwords:", "blue"), colored(total_combinations, "white"))

    end_time = time.time()
    total_time = end_time - start_time
    formatted_time = format_time(total_time)

    print(colored("\nTotal time:", "blue"), colored(formatted_time, "white"))

