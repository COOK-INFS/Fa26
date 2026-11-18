import module1

print ("This is the main script")

module1.helper_function()

module1.main()

print("_______________")
print(f"Module 2' name is: {__name__}")
print(f"Module 1's name is: {module1.__name__}")