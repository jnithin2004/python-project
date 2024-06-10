import sqlite3
from datetime import datetime

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('payroll.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    department TEXT,
    position TEXT,
    salary REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS payroll (
    payroll_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    pay_date TEXT,
    gross_salary REAL,
    tax REAL,
    net_salary REAL,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
)
''')

conn.commit()

# Employee management functions
def add_employee():
    employee_id = int(input("Enter employee ID: "))
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    department = input("Enter department: ")
    position = input("Enter position: ")
    salary = float(input("Enter salary: "))
    cursor.execute('''
    INSERT INTO employees (employee_id, first_name, last_name, department, position, salary)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (employee_id, first_name, last_name, department, position, salary))
    conn.commit()
    print("Employee added successfully.")

def update_employee():
    employee_id = int(input("Enter employee ID to update: "))
    cursor.execute('SELECT * FROM employees WHERE employee_id = ?', (employee_id,))
    employee = cursor.fetchone()

    if employee:
        first_name = input("Enter new first name (or press Enter to skip): ")
        last_name = input("Enter new last name (or press Enter to skip): ")
        department = input("Enter new department (or press Enter to skip): ")
        position = input("Enter new position (or press Enter to skip): ")
        salary = input("Enter new salary (or press Enter to skip): ")
        salary = float(salary) if salary else None
        fields = ['first_name', 'last_name', 'department', 'position', 'salary']
        values = [first_name, last_name, department, position, salary]
        updates = ', '.join(f"{field} = ?" for field, value in zip(fields, values) if value)
        cursor.execute(f'''
        UPDATE employees
        SET {updates}
        WHERE employee_id = ?
        ''', (*[value for value in values if value], employee_id))
        conn.commit()
        print("Employee updated successfully.")
    else:
        print("Employee ID not found. Adding new employee.")
        add_employee()

def delete_employee():
    employee_id = int(input("Enter employee ID to delete: "))
    cursor.execute('''
    DELETE FROM employees
    WHERE employee_id = ?
    ''', (employee_id,))
    conn.commit()
    print("Employee deleted successfully.")

# Payroll calculation function
def calculate_payroll():
    employee_id = int(input("Enter employee ID to calculate payroll for: "))
    pay_date = input("Enter pay date (YYYY-MM-DD): ")
    cursor.execute('SELECT salary FROM employees WHERE employee_id = ?', (employee_id,))
    salary = cursor.fetchone()[0]
    
    # Assuming a flat tax rate of 20%
    tax_rate = 0.20
    tax = salary * tax_rate
    net_salary = salary - tax

    cursor.execute('''
    INSERT INTO payroll (employee_id, pay_date, gross_salary, tax, net_salary)
    VALUES (?, ?, ?, ?, ?)
    ''', (employee_id, pay_date, salary, tax, net_salary))
    conn.commit()
    print("Payroll calculated successfully.")

# Function to generate and display payslips
def generate_payslip():
    employee_id = int(input("Enter employee ID to generate payslip for: "))
    pay_date = input("Enter pay date (YYYY-MM-DD): ")
    cursor.execute('''
    SELECT e.first_name, e.last_name, p.gross_salary, p.tax, p.net_salary
    FROM employees e
    JOIN payroll p ON e.employee_id = p.employee_id
    WHERE e.employee_id = ? AND p.pay_date = ?
    ''', (employee_id, pay_date))
    payslip = cursor.fetchone()

    if payslip:
        first_name, last_name, gross_salary, tax, net_salary = payslip
        print(f"Payslip for {first_name} {last_name} on {pay_date}:")
        print(f"Gross Salary: ${gross_salary:.2f}")
        print(f"Tax: ${tax:.2f}")
        print(f"Net Salary: ${net_salary:.2f}")
    else:
        print("No payslip found for the given employee and date.")

# Main loop for user interaction
def main():
    while True:
        print("\nPayroll System")
        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. Calculate Payroll")
        print("5. Generate Payslip")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_employee()
        elif choice == '2':
            update_employee()
        elif choice == '3':
            delete_employee()
        elif choice == '4':
            calculate_payroll()
        elif choice == '5':
            generate_payslip()
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

    # Close the connection
    conn.close()

if __name__ == '__main__':
    main()
