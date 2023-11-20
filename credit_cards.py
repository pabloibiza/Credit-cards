#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
from random import randint


def validator(cc_number):
    final_sum = 0
    numbers = list(reversed(cc_number))

    # Converts each character into integer.
    for x in range(0, len(numbers)):
        numbers[x] = int(numbers[x])

    # Multiplies each odd position (in the list) digit per 2 and rests 9 if is higher than 9.
    for i in range(1, len(numbers)):
        if i % 2 != 0:
            numbers[i] = numbers[i] * 2
            if numbers[i] > 9:
                numbers[i] = numbers[i] - 9
    # Sumatory of all digits.
    for number in numbers:
        final_sum += number

    # If the sum is divisible by 10, the number is valid.
    if (final_sum % 10) == 0:
        return True
    else:
        return False


def get_vendor(cc_number):
    possible_vendors = []
    vendor = ""
    identifier = ""

    # Makes a list with the possible vendors to save time when checking identifiers. It searches the matches with the
    # numbers length.
    with open('vendors_length', newline='') as vendors_length_file:
        reader = csv.reader(vendors_length_file)
        for row in reader:
            for column in range(1, len(row)):
                if len(cc_number) == int(row[column]):
                    possible_vendors.append(row[0])

    # Searhes a match in the possible_vendors list.
    with open('vendors', newline='') as vendors_file:
        reader = csv.reader(vendors_file)
        for row in reader:
            if row[0] in possible_vendors:
                for column in range(1, len(row)): # Each identifier of the vendor. Avoids position 0, is the vendor name
                    if len(identifier) < len(row[column]): # Only does it if the current identifier is shorter.
                        for i in range(1, 6):   # Identifiers length form 1 to 6.
                            if cc_number[0:i] == row[column]:
                                vendor = row[0]
                                identifier = row[column]
    return vendor

def calculate_checksum(firs_protion):
    final_sum = 0
    numbers = list(reversed(firs_protion))

    # Converts each character into integer.
    for x in range(0, len(numbers)):
        numbers[x] = int(numbers[x])

    # Multiplies each pair position (in the list) digit per 2 and rests 9 if is higher than 9.
    for i in range(0, len(numbers)):
        if i % 2 == 0:
            numbers[i] = numbers[i] * 2
            if numbers[i] > 9:
                numbers[i] = numbers[i] - 9
    # Sumatory of all digits.
    for number in numbers:
        final_sum += number
    # The checksum will be the remainter of the final sum divided by 10.
    checksum = str(10 - (final_sum % 10))

    return checksum

def generate_number(vendor):
    if vendor not in vendors_list(): return "Vendor not in list"
    pre_final = ""
    number_length = 0
    base_number = ""

    reader_length = csv.reader(open('vendors_length', newline=''))
    for row in reader_length:
        if row[0] == vendor:
            random_col = randint(1, len(row) - 1)
            number_length = row[random_col]

    reader_vendor = csv.reader(open('vendors', newline=''))
    for row in reader_vendor:
        if row[0] == vendor:
            base_number = row[randint(1, len(row)-1)]

    digits_to_generate = int(number_length) - len(base_number) - 1
    for i in range(0, digits_to_generate):
            pre_final += str(randint(0, 9))
    pre_final = base_number + pre_final

    cc_number = pre_final + calculate_checksum(pre_final)

    if not validator(cc_number):
        print("Number not valid, generating a new one")
        generate_number(vendor)

    return cc_number

def vendors_list():
    vendors_list = []
    reader_length = csv.reader(open('vendors_length', newline=''))
    for row in reader_length:
        vendors_list.append(row[0])
    return vendors_list

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    while(True):
        cls()
        print("SELECT AN OPTION: \n" + "1. Validate a credit card number\n" + "2. See vendor from a credir card\n" +
              "3. Calculate the checksum of a number\n" + "4. Generate a random card number from a given vendor\n" +
              "0. Exit\n\n" + "Option: ")
        option = input()
        cls()
        if option == "1":
            print("Credit card number: ")
            if validator(input()):
                print("\n\nThe credit card is valid")
            else:
                print("\n\nThe credit card is not valid")
            print("Press any key to return")
            input()
            cls()
        elif option == "2":
            print("Credit card number: ")
            print(get_vendor(input()))
            print("\n\nPress any key to return")
            input()
            cls()
        elif option == "3":
            print("Number: ")
            print(calculate_checksum(input()))
            print("\n\nPress any key to return")
            input()
            cls()
        elif option == "4":
            print("1. See vendors list")
            print("2. Introduce vendor")
            print("Option: ")
            option4 = input()
            cls()
            if option4 == "1":
                for vendor in vendors_list():
                    print(vendor)
            elif option4 == "2":
                print("Vendor: ")
                print(generate_number(input()))
            else:
                print("\n\nOption not valid")
            print("\n\nPress any key to return")
            input()
            cls()
        elif option == "0":
            break
        else:
            print("option not valid")


if __name__ == "__main__":
    main()
