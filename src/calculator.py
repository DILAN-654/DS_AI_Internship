while(1):
    print("Simple Calculator")
    a=int(input("Enter first number:"))
    print("first Number : ",a)
    b=int(input("Enter Second number:"))
    print("Second Number : ",b)

    print("Addition :+ \n Substraction :- \n multiplication :* \n Division :/ \n Modulas :% ")
    ch=input("Enter the Operation ")
    if ch=='+':
        print("Sum: ",a+b)
    elif ch=='-':
        print("Substraction: ",a-b)
    elif ch=='/':
        print("Division: ",a/b)
    elif ch=='*':
        print("product: ",a*b)
    elif ch=='%':
        print("remainder: ",a%b)
    else:
        print("Invalid Choice")
        break
