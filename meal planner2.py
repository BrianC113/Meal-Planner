import csv
import time
import random

filename = 'meal_prep.csv'


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GET USERS CSV FILE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def getUsers():
    users = []
    # Open the users.csv file in read mode
    with open("users.csv", "r") as file:
        reader = csv.DictReader(file)   # Read rows as dictionaries
        for row in reader:
            users.append(row)  # Add each user to the list 
    return users    # Return list of user dictionaries


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> LOGIN <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def login(users):
    username = input("Enter username: ")
    password = input("Enter your password: ")

    # Check if the username and password match any user in the list
    for u in users:
        if u.get('Username') == username and u.get('Password') == password:
            return True, u  # Successful login returns True and user info

    return False, None  # Login failed returns False and None


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> VIEW RECIPES FUNCTION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def getRecipe():
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            recipes = list(reader)  # Convert reader object to list for easy use

            # Loop through recipes using indices
            if not recipes:
                print('\nNo recipes available yet.')    # If file is empty
                return

            print('\n--- Available Recipes: ---')
            for i in range(len(recipes)):
                recipe = recipes[i]
                print(f'{i + 1}. {recipe["MealName"]} - {recipe["MealPrep"]}')
    except FileNotFoundError:
        print('\nNo recipes file found yet!!! Please add recipes first.')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ADD TO MEAL PLAN <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def addMeal():
    try:
        n = int(input('How many meals would you like to add? '))

        if n <= 0:
            print('Please enter a number bigger than 0!!!')
            return  # Stop if invalid

        # Find highest MealID so far
        biggestID = 0
        try:
            with open(filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    mealID = int(row['MealID']) 
                    if mealID > biggestID:  
                        biggestID = mealID
        except FileNotFoundError:
            print("Meal doesn't exist yet!!!")  

        # Add new meals
        for no in range(n):
            name = input('Enter Meal Name: ')
            ingredients = input('Enter Ingredients (separated by ; ): ')
            prep = input('Enter Preparation instructions: ')

            biggestID += 1  # Unique MealID for new meal

            newMeal = {'MealID': biggestID, 'MealName': name, 'Ingredients': ingredients, 'MealPrep': prep}
            
            print('New meal added.')

            # Save to file
            with open(filename, "a", newline="") as file:
                fieldnames = ['MealID', 'MealName', 'Ingredients', 'MealPrep']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writerow(newMeal)

    except ValueError:
        print('Please enter a valid number!!!')


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>> REMOVE FROM MEAL PLAN <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def removeMeal():
    removeID = input('Enter the MealID of the meal you want to remove: ')

    # Read all meals into a list
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            meals = list(reader)
    except FileNotFoundError:
        print('Meal file not found!!!')
        return

    # Look for meal with matching MealID
    findID = False
    for meal in meals:
        if meal['MealID'] == removeID:
            meals.remove(meal) 
            findID = True
            break

    if findID:
        # Rewrite CSV without the removed meal
        with open(filename, "w", newline="") as file:
            fieldnames = ['MealID', 'MealName', 'Ingredients', 'MealPrep']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for meal in meals:
                writer.writerow(meal)

        print(f'Meal with MealID {removeID} deleted successfully.')
    else:
        time.sleep(1)
        print('MealID not found.')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>> VIEW WEEKLY PLAN <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def weeklyPlan():
    try:
        # Open the meals file and read all meals
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            meals = list(reader)

        if not meals:
            print('\nNo meals found! Please add some meals first.')
            return

        print('\n--- Your Weekly Meal Plan: ---')
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Pick 7 random MealIDs between 1 and 10 as strings
        randomID = []
        for n in range(7):
            num = random.randint(1, 10)
            randomID.append(str(num))

        # For each day, find and print the meal with matching MealID
        for i in range(7):
            found = False
            for meal in meals:
                if meal['MealID'] == randomID[i]:
                    print(f'{days[i]}: {meal["MealName"]}')
                    found = True
                    break
            if not found:
                print(f"{days[i]}: Meal ID {randomID[i]} not found.")

    except FileNotFoundError:
        print('\nMeal file not found! Please add some meals first.')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> EDIT RECIPES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def editMeal():
    try:
        findID = input('Enter the MealID of the meal you want to edit: ')

        # Read all meals from file
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            meals = list(reader)

        # Find the meal with matching MealID
        found = False
        for meal in meals:
            if meal['MealID'] == findID:
                found = True
                print(f"Current Meal Name: {meal['MealName']}")
                name = input('Enter new Meal Name (or press Enter to keep current): ')
                if name.strip() != "":
                    meal['MealName'] = name  # Update name if user typed something

                print(f"Current Ingredients: {meal['Ingredients']}")
                ingredients = input('Enter new Ingredients (separated by ;) (or press Enter to keep current): ')
                if ingredients.strip() != "":
                    meal['Ingredients'] = ingredients  # Update ingredients

                print(f"Current Preparation: {meal['MealPrep']}")
                prep = input('Enter new Preparation instructions (or press Enter to keep current): ')
                if prep.strip() != "":
                    meal['MealPrep'] = prep  # Update preparation

                break

        if not found:
            print('MealID not found!!!')
            return

        # Save updated meals back to the file
        with open(filename, "w", newline="") as file:
            fieldnames = ['MealID', 'MealName', 'Ingredients', 'MealPrep']  
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(meals)
        time.sleep(1)
        print('Meal updated successfully.')

    except FileNotFoundError:
        print('Meal file not found!!! Please add meals first.')

#----------------------MAIN MENU-------------------------------
def menu(user):
    while True:
        print(f'\n--- Welcome {user["Username"]} ---')
        print('Would you like to: ')
        print('1. View Recipes')
        print('2. Add to Meal Plan')
        print('3. Remove item from Meal Plan')
        print('4. View Weekly meal plan')
        print('5. Edit recipes')
        print('6. Logout')

        choice = input('Enter your choice (1-6): ')

        if choice == '1':
            getRecipe()
        elif choice == '2':
            addMeal()
        elif choice == '3':
            removeMeal()
        elif choice == '4':
            weeklyPlan()
        elif choice == '5':
            editMeal()
        elif choice == '6':
            print('\nLogging out...')
            time.sleep(1)
            print('Goodbye')
            break
        else:
            print('Invalid choice. Please try again.')



#---------------------USER INPUT-------------------------------
users = getUsers()

while True:
    success, user = login(users)

    if success:
        print('Login successful')
        menu(user) #fixed: directly calls on the menu function
        break
    else:
        print('Access denied')
        time.sleep(1)
        print('Please try again')
