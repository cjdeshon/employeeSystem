'''
Basic Employee Management system
    Steps to run:
        set up virtual environment
        run app.py
        test html requests using pullman
'''

import sys
print(sys.path)

from flask import Flask, jsonify, request, abort
import time

#create app
app = Flask(__name__)

class Employee:
    employees = {}
    
    def __init__(self, ID = None, name = None, hourly = None, hoursWorked = None, department = "Unknown"):
        if ID is None or name is None or hourly is None or hoursWorked is None:
            raise ValueError("Insufficient employee details")
        
        self.ID = ID
        self.name = name
        self.department = department
        self.hourly = hourly
        self.hoursWorked = hoursWorked
        self.clock_in_time = None
        
        Employee.employees[self.ID] = self
    
    @classmethod
    def readEmploy(cls, ID):
        return cls.employees.get(ID, None)
#         employee = cls.employees.get(ID)
#       
#         if employee:
#             print("Employee id: ", employee.ID)
#             print("Employee name: ", employee.name)
#             print("Employee department: ", employee.department)
#             print("Employee hourly: ", employee.hourly)
#             print("Employee hoursWorked: ", employee.hoursWorked)
#         else:
#             print(f"No employee found with ID: {ID}")

    @classmethod
    def outputEmploy(cls):
        return cls.employees.values()
#         if len(cls.employees):
#             for employee in cls.employees.values():
#                 print("Employee id: ", employee.ID)
#                 print("Employee name: ", employee.name)
#                 print("Employee department: ", employee.department)
#                 print("Employee hourly: ", employee.hourly)
#                 print("Employee hoursWorked: ", employee.hoursWorked)
#                 print("\n")
#         else:
#             print("Employee database empty")

    @classmethod
    def updateEmploy(cls, ID, change):
        employee = cls.employees.get(ID)
        
        if employee:
            if update_type == "hourly":
                employee.hourly = change
                return employee
            elif update_type == "dapartment": 
                employee.department = change
                return employee
        return None
#         if employee:
#             if type(change) == float:
#                 employee.hourly = change
#                 print("hourly wage updated\n")
#             elif type(change) == str:
#                 employee.department = change
#                 print("department updated\n")
#             else:
#                 print("Update not possible")
#         else:
#             print(f"No employee found with ID: {ID}")
            
    @classmethod
    def deleteEmploy(cls, ID):   
        return cls.employees.pop(ID, None)
#         if ID in cls.employees:
#             del cls.employees[ID]
#             print(f"Employee {ID} deleted from database\n")
#         else:
#             print(f"No employee found with ID: {ID}")
    
    @classmethod
    def calculatePayout(cls):   
        payouts = []
        for employee in cls.employees.values():
            payout = employee.hourly * employee.hoursWorked
            payouts.append({"id": employee.ID, "name": employee.name, "wage": payout})
            employee.hoursWorked = 0.0
        return payouts
            
#         if len(cls.employees):
#             for employee in cls.employees.values():
#                 print(f"Employee {employee.name} with ID-{employee.ID} wages = ${employee.hourly * employee.hoursWorked}")
#                 employee.hoursWorked = 0.0
#             print("\n")
#         else:
#             print("Employee database empty")

    @classmethod
    def clock_in(cls, ID):
        employee = cls.employees.get(ID)
        
        if employee and employee.clock_in_time is None:
            employee.clock_in_time = time.time()
            return employee
        return None
#         if not employee:
#             print(f"No employee found with ID: {ID}")
#             return
        
#         if employee.clock_in_time is not None:
#             print(f"Employee {employee.name} is already clocked in.")
#         else:
#             employee.clock_in_time = time.time()
#             print(f"Employee {employee.name} clocked in")
            
    @classmethod
    def clock_out(cls, ID):
        employee = cls.employees.get(ID)
        
        if employee and employee.clock_in_time is not None:
            clock_out_time = time.time()
            elapsed_time = clock_out_time - employee.clock_in_time
            hours = elapsed_time / 3600
            employee.hoursWorked += hours
            employee.clock_in_time = None
            return hours
        return None
#         if not employee:
#             print(f"No employee found with ID: {ID}")
#             return
#         if employee.clock_in_time is None:
#             print(f"Employee {employee.name} is not clocked in.")
#         clock_out_time = time.time()
#         elapsed_time = clock_out_time - employee.clock_in_time
#         hours = elapsed_time / 3600
#         print(f"Employee {employee.name} logged {hours} hours")
#         employee.hoursWorked += hours
#         employee.clock_in_time = None






# API Endpoints
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify([{"id": e.ID, "name": e.name, "department": e.department, "hourly": e.hourly, "hoursWorked": e.hoursWorked} for e in Employee.outputEmploy()])

@app.route('/employees/<int:ID>', methods=['GET'])
def get_employee(ID):
    employee = Employee.readEmploy(ID)
    if employee is None:
        abort(404)
    return jsonify({"id": employee.ID, "name": employee.name, "department": employee.department, "hourly": employee.hourly, "hoursWorked": employee.hoursWorked})

@app.route('/employees', methods=['POST'])
def create_employee():
    if not request.json or not all(k in request.json for k in ("ID", "name", "hourly")):
        abort(400)
    try:
        employee = Employee(
            ID = request.json["ID"], 
            name=request.json["name"],
            hourly=request.json["hourly"],
            hoursWorked=request.json.get("hoursWorked", 0),
            department=request.json.get("department", "Unknown")
        )
        return jsonify({"id": employee.ID}), 201
    except ValueError as e:
        abort(400)
        
@app.route('/employees/<int:ID>', methods=['PUT'])
def update_employee(ID):
    if not request.json:
        abort(400)
    employee = Employee.readEmploy(ID)
    if employee is None:
        abort(404)

    if 'hourly' in request.json:
        Employee.updateEmploy(ID, request.json['hourly']) #, "hourly")
    if 'department' in request.json:
        Employee.updateEmploy(ID, request.json['department']) #, "department")

    return jsonify({"id": employee.ID, "name": employee.name, "department": employee.department, "hourly": employee.hourly, "hoursWorked": employee.hoursWorked})

@app.route('/employees/<int:ID>', methods=['DELETE'])
def delete_employee(ID):
    if Employee.deleteEmploy(ID):
        return jsonify({'result': True})
    else:
        abort(404)

@app.route('/employees/payout', methods=['GET'])
def calculate_payout():
    payouts = Employee.calculatePayout()
    return jsonify(payouts)

@app.route('/employees/<int:ID>/clock_in', methods=['POST'])
def clock_in(ID):
    if Employee.clock_in(ID):
        return jsonify({"result": f"Employee {ID} clocked in."})
    else:
        abort(404)

@app.route('/employees/<int:ID>/clock_out', methods=['POST'])
def clock_out(ID):
    hours = Employee.clock_out(ID)
    if hours is not None:
        return jsonify({"result": f"Employee {ID} logged {hours:.2f} hours."})
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)


