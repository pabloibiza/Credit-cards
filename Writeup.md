# Credit card verifier - Writeup

This is the credit cards verifier lab of the Secure Communications module.

## Exersices

* Verify: Take a credit card number as input and output if it is a valid or invalid
credit card number.
* Vendor: Again take a credit card number as input and output the issuing vendor.
* Checksum: Given just the first portion of a credit card calculate the checksum.
* Generate: Select the issuing vendor, then generate a random valid credit card.

### 1. Verify
When you have a sequence of digits and you want to know if those numbers correspond or not to a possible payment card number (PAN), Luhn's algorithm is applied, whose result must be 0 if that sequence is valid.

The algorithm of Luhn, is used to validate all kinds of numbers, including those of credit cards, IMEI (cell phones), etc. It is not a cryptographic method, but a method of verification of errors, that none have been committed during its transmission or registration.

To check a credit card number using Luhn's algorithm, these are the steps:

1. The given number must be reversed (and converted into integers to operate with them).
    ```python
    # cc_number is the given credit card number.
    numbers = list(reversed(cc_number))

    for x in range(0, len(numbers)):
    numbers[x] = int(numbers[x])
    ```
2. The numbers in odd positions must be multiplied by 2. If the result is bigger than 9, the options are:
    * Rest 9 to the result.
    * Sum the two digits.
    
    The result will be the same.
    ```python
    for i in range(1, len(numbers)):
        if i % 2 != 0:
            numbers[i] = numbers[i] * 2
            if numbers[i] > 9:
                numbers[i] = numbers[i] - 9
    ```
3. Then sum all digits.
    ```python
    for number in numbers:
        final_sum += number
    ```
4. To finish the proces, calculate the modulus 10 of the final sum. If the number is divisible by 10, the card number is valid.
  
   ```python
   if (final_sum % 10) == 0:
       return True
   else:
       return False
   ```

### 2. See vendor
To see the vendor of a given card number I have two files `vendors.csv` and `vendors_length.csv`. In `vendors.csv` there 
are the identifiers of the vendors and in `vendors_length.csv` there are the possible legth of their cards.

1. It starts creating a list with the possible vendors to reduce the checked vendors.

    ```python
        with open('vendors_length', newline='') as vendors_length_file:
        reader = csv.reader(vendors_length_file)
        for row in reader:
            for column in range(1, len(row)):
                if len(cc_number) == int(row[column]):
                    possible_vendors.append(row[0])
    ``` 

2. Then searches matches in the possible vendors. 
The first six numbers of a credit card number are the identifier, but for each company can differ the length of this identifier.
So the loop checks matches for lengths from 1 to 6. 
If there are multiple matches, saves the longest identifier.
    
    ```python
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
    ``` 
3. Once it has finished returns the longest match found.

### 3. Calculate the checksum
The last digit of each credit card is the checksum or check digit. It is used to validate the card using the Luhn algorithm.

The steps to calculate the checksum of a number are the same, in exception of in this case we don't know the last digit.


1. Calculates the sum of the given numbers multiplying by two the pair position numbers (in this case are pair position numbers because the last digit must be generated then. 

    ```python
    # first_portion is the given number
    numbers = list(reversed(firs_protion))

    # Converts each character into integer.
    for x in range(0, len(numbers)):
        numbers[x] = int(numbers[x])

    # Multiplies each even position (in the list) digit per 2 and rests 9 if is higher than 9.
    for i in range(0, len(numbers)):
        if i % 2 == 0:
            numbers[i] = numbers[i] * 2
            if numbers[i] > 9:
                numbers[i] = numbers[i] - 9
    # Sumatory of all digits.
    for number in numbers:
        final_sum += number
    ```
2. Makes final sum modulo 10. The checksum is the number that must be added to this result to make the next multiple of 10.

    ```python
    checksum = str(10 - (final_sum % 10))
    ```

### 4. Generate a random card number from a given vendor
To generate the card number, we need first a list of the vendors names. In my case, I have two lists, one for the 
vendors identifiers, and one for the vendors cards length (both in `.csv` format).

Steps:
1. Checks if the vendor is in the vendors list.

    ```python
    if vendor not in vendors_list(): return "Vendor not in list"
    ```
      * I have crated a method for this:
        ```python
            def vendors_list():
                vendors_list = []
                reader_length = csv.reader(open('vendors_length', newline=''))
                for row in reader_length:
                    vendors_list.append(row[0])
                return vendors_list
        ```

2. Selects a random length from the `vendors_length` file.

    ```python
    reader_length = csv.reader(open('vendors_length', newline=''))
    for row in reader_length:
        if row[0] == vendor:
            random_col = randint(1, len(row) - 1)
            number_length = row[random_col]
    ```
3. Selects a random identifier from the `vendors` file.

    ```python
    reader_vendor = csv.reader(open('vendors', newline=''))
    for row in reader_vendor:
        if row[0] == vendor:
            base_number = row[randint(1, len(row)-1)]
    ```
4. Then it generates the remaining digits until reaching the previously chosen size (except the last number, which will be the checksum).

    ```python
    digits_to_generate = int(number_length) - len(base_number) - 1
    for i in range(0, digits_to_generate):
            pre_final += str(randint(0, 9))
    pre_final = base_number + pre_final
    ```

5. To finish, calculates the checksum of the `pre_final` number and add it to the number.
    
    ```python
    cc_number = pre_final + calculate_checksum(pre_final)
    ```

## Menu
To imporve the usability, I have created a menu. The API is running until the exit option is chosen.

```python
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
```
