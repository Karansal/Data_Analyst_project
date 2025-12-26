import time
students = {
    "101": {'name': "fulwari karan", 'marks': 85, 'grade': "A"},
    "102": {'name': "Nevin thalip", 'marks': 92, 'grade': "A+"},
    "103": {'name': "Aryan Singh", 'marks': 74, 'grade': "B"},
    "104": {'name': "Sneha Patel", 'marks': 62, 'grade': "C"},
    "105": {'name': "Vikram Das", 'marks': 45, 'grade': "D"}
}


def calculate_grade(marks):
    """Marks ke hisaab se Grade return karta hai"""
    if marks >= 90: return "A+"
    elif marks >= 80: return "A"
    elif marks >= 70: return "B"
    elif marks >= 60: return "C"
    elif marks >= 40: return "D"
    else: return "F (Fail)"

def print_header(title):
    """Sundar header print karne ke liye function"""
    print("\n" + "=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50)

# --- . create ---

def add_student():
    print_header("ADD NEW STUDENT")
    roll_no = input("Enter Roll Number: ").strip()
    
    if roll_no in students:
        print("Error: Ye Roll Number pehle se maujood hai!")
        return

    name = input("Enter Name: ").strip()
    if not name:
        print("Error: Naam khali nahi ho sakta.")
        return

    try:
        marks = int(input("Enter Marks (0-100): "))
        if 0 <= marks <= 100:
            grade = calculate_grade(marks)
            students[roll_no] = {'name': name, 'marks': marks, 'grade': grade}
            print(f"✅ Success: Student {name} successfully add ho gaya!")
        else:
            print("Error: Marks 0 se 100 ke beech hone chahiye.")
    except ValueError:
        print("Error: Kripya marks numbers mein daalein.")

#  --read---
def view_students():
    print_header("STUDENT RECORDS")
    if not students:
        print("Abhi koi data nahi hai.")
    else:
        # Table Header
        print(f"{'Roll No':<10} | {'Name':<20} | {'Marks':<8} | {'Grade':<5}")
        print("-" * 52)
        
        # Loop through sorted dictionary (Roll no ke hisaab se sort)
        for roll in sorted(students.keys()):
            details = students[roll]
            print(f"{roll:<10} | {details['name']:<20} | {str(details['marks']):<8} | {details['grade']:<5}")
        print("-" * 52)
        print(f"Total Students: {len(students)}")

# ---update--

def update_student():
    print_header("UPDATE STUDENT DETAILS")
    view_students() # Pehle list dikhate hain taaki user ko aasani ho
    print("-" * 52)
    
    roll_no = input("Kis Roll Number ko update karna hai?: ").strip()
    
    if roll_no in students:
        current = students[roll_no]
        print(f"\nCurrent Details -> Name: {current['name']}, Marks: {current['marks']}")
        print("(Agar change nahi karna to seedha Enter dabayein)")
        
        new_name = input("New Name: ").strip()
        new_marks_str = input("New Marks: ").strip()

        # Update Name
        if new_name:
            students[roll_no]['name'] = new_name
            
        # Update Marks (Isme thoda logic hai kyunki Grade bhi badalna padega)
        if new_marks_str:
            try:
                new_marks = int(new_marks_str)
                if 0 <= new_marks <= 100:
                    students[roll_no]['marks'] = new_marks
                    students[roll_no]['grade'] = calculate_grade(new_marks) 
                else:
                    print("Error: Marks invalid the, update nahi hua.")
            except ValueError:
                print("Error: Marks number hone chahiye.")

        print("Success: Details update ho gayi hain.")
    else:
        print("Error: Ye Roll Number nahi mila.")

# --delete--
def delete_student():
    print_header("DELETE STUDENT")
    roll_no = input("Delete karne ke liye Roll Number batayein: ").strip()
    
    if roll_no in students:
        confirm = input(f"Kya aap sure hain ki {students[roll_no]['name']} ko delete karna hai? (y/n): ")
        if confirm.lower() == 'y':
            del students[roll_no]
            print("Success: Record delete kar diya gaya.")
        else:
            print("Operation Cancelled.")
    else:
        print("Error: Record nahi mila.")

# --- 4. Main loop system ---
def main():
    while True:
        print("\n")
        print("╔════════════════════════════════╗")
        print("║   SCHOOL MANAGEMENT SYSTEM     ║")
        print("╠════════════════════════════════╣")
        print("║ 1. View All Students           ║")
        print("║ 2. Add New Student             ║")
        print("║ 3. Update Student Details      ║")
        print("║ 4. Delete Student              ║")
        print("║ 5. Exit System                 ║")
        print("╚════════════════════════════════╝")
        
        choice = input("Enter Choice (1-5): ")
        
        if choice == '1':
            view_students()
        elif choice == '2':
            add_student()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("Save ho gaya hai. Thank you for using the system!")
            time.sleep(1) 
            print("System Shutting Down. Goodbye!")
            break
        else:
            print("Invalid Option. Try again.")
        
        # User ko output padhne ka time dene ke liye pause
        input("\nPress Enter to return to Main Menu...")

# Code Run
if __name__ == "__main__":
    main()