import json
from flask import Flask, jsonify, request # pyright: ignore[reportMissingImports]

app = Flask(__name__)

# Sample data
employees = [
    {'id': 1, 'name': 'Ashley'},
    {'id': 2, 'name': 'Kate'},
    {'id': 3, 'name': 'Joe'}
]

nextEmployeeId = 4


# ------------------- Helper Functions -------------------

def get_employee(id):
    return next((e for e in employees if e['id'] == id), None)


def employee_is_valid(employee):
    # Only 'name' field is allowed
    for key in employee.keys():
        if key != 'name':
            return False
    return True


# ------------------- API Routes -------------------

# GET all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)


# GET employee by ID
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id):
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404
    return jsonify(employee)


# POST (Create new employee)
@app.route('/employees', methods=['POST'])
def create_employee():
    global nextEmployeeId

    employee = json.loads(request.data)

    if not employee_is_valid(employee):
        return jsonify({'error': 'Invalid employee properties.'}), 400

    employee['id'] = nextEmployeeId
    nextEmployeeId += 1

    employees.append(employee)

    return '', 201, {'location': f'/employees/{employee["id"]}'}


# PUT (Update employee)
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = get_employee(id)

    if employee is None:
        return jsonify({'error': 'Employee does not exist.'}), 404

    updated_employee = json.loads(request.data)

    if not employee_is_valid(updated_employee):
        return jsonify({'error': 'Invalid employee properties.'}), 400

    employee.update(updated_employee)

    return jsonify(employee)


# DELETE employee
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    global employees

    employee = get_employee(id)

    if employee is None:
        return jsonify({'error': 'Employee does not exist.'}), 404

    employees = [e for e in employees if e['id'] != id]

    return jsonify(employee), 200


# ------------------- Run Server -------------------

if __name__ == '__main__':
    app.run(port=5000)