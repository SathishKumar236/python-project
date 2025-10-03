#pip install mysql-connector-python
#pip show mysql-connector-python

import mysql.connector

# Connect to MySQL 
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       
        password="SK23SQL",    
        database="staff_db"
    )

# Add staff
def add_staff(staff_id, name, dept, age, salary):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO staff (staff_id, name, department, age, salary) VALUES (%s, %s, %s, %s, %s)",
                       (staff_id, name, dept, int(age), float(salary)))
        conn.commit()
        print(f" Staff '{name}' added successfully!")
    except mysql.connector.IntegrityError:
        print(f" Staff ID '{staff_id}' already exists.")
    except Exception as e:
        print(" Error:", e)
    finally:
        conn.close()

# View staff
def view_staffs():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM staff")
        records = cursor.fetchall()
        if records:
            print("\n--- Staff List ---")
            for row in records:
                print(f"ID: {row[0]} | Name: {row[1]} | Dept: {row[2]} | Age: {row[3]} | Salary: {row[4]}")
        else:
            print("No staff data available.")
    except Exception as e:
        print(" Error:", e)
    finally:
        conn.close()

# Update staff
def update_staff(staff_id, name=None, dept=None, age=None, salary=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        updates = []
        values = []

        if name:
            updates.append("name = %s")
            values.append(name)
        if dept:
            updates.append("department = %s")
            values.append(dept)
        if age:
            updates.append("age = %s")
            values.append(int(age))
        if salary:
            updates.append("salary = %s")
            values.append(float(salary))

        if updates:
            values.append(staff_id)
            query = f"UPDATE staff SET {', '.join(updates)} WHERE staff_id = %s"
            cursor.execute(query, tuple(values))
            conn.commit()
            if cursor.rowcount:
                print(" Staff updated successfully.")
            else:
                print(" Staff ID not found.")
        else:
            print(" No update fields provided.")
    except Exception as e:
        print(" Error:", e)
    finally:
        conn.close()

# Delete staff
def delete_staff(staff_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM staff WHERE staff_id = %s", (staff_id,))
        conn.commit()
        if cursor.rowcount:
            print(f" Staff with ID '{staff_id}' deleted.")
        else:
            print(f" Staff with ID '{staff_id}' not found.")
    except Exception as e:
        print(" Error:", e)
    finally:
        conn.close()

# Menu function
def menu():
    while True:
        print("\n--- Staff Management System (MySQL) ---")
        print("1. Add Staff")
        print("2. View Staff")
        print("3. Update Staff")
        print("4. Delete Staff")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                print("\nEnter staff details (or type 'exit' to stop):")
                staff_id = input("Enter staff ID: ")
                if staff_id.lower() == 'exit':
                    break

                name = input("Enter name: ")
                if name.lower() == 'exit':
                    break

                dept = input("Enter department: ")
                if dept.lower() == 'exit':
                    break

                age_input = input("Enter age: ")
                if age_input.lower() == 'exit':
                    break

                salary_input = input("Enter salary: ")
                if salary_input.lower() == 'exit':
                    break

                try:
                    age = int(age_input)
                    salary = float(salary_input)
                    add_staff(staff_id, name, dept, age, salary)
                except ValueError:
                    print(" Invalid input. Age and salary must be numeric.")

        elif choice == '2':
            view_staffs()

        elif choice == '3':
            staff_id = input("Enter staff ID to update: ")
            name = input("Enter new name (leave blank to skip): ") or None
            dept = input("Enter new department (leave blank to skip): ") or None
            age = input("Enter new age (leave blank to skip): ") or None
            salary = input("Enter new salary (leave blank to skip): ") or None
            update_staff(staff_id, name, dept, age, salary)

        elif choice == '4':
            staff_id = input("Enter staff ID to delete: ")
            delete_staff(staff_id)

        elif choice == '5':
            print(" Exiting & GoodBye!")
            break

        else:
            print(" Invalid choice. Try Again.")


# Start program
menu()
