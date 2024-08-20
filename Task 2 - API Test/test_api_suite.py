import requests
import pytest
import json
from jsonschema import validate

BASE_URL = "https://crudcrud.com/api/11c39b8cfd4546b6845c11e85fa3b470/employees"

# Load employee data
with open('src/employees.json') as f:
    employees = json.load(f)

# Load schema for validation
with open('schemas/employee_schema.json') as f:
    employee_schema = json.load(f)


def validate_employee_schema(employee):
    """Helper function to validate the schema of an employee."""
    validate(instance=employee, schema=employee_schema)


@pytest.fixture(scope='module')
def employee_id():
    """Fixture to hold the ID of the created employee."""
    return None


def test_create_employee(employee_id):
    """Test case for creating an employee."""
    response = requests.post(BASE_URL, json=employees[0])
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    employee = response.json()
    validate_employee_schema(employee)
    employee_id = employee['_id']
    return employee_id


def test_get_employee(employee_id):
    """Test case for retrieving an employee."""
    response = requests.get(f"{BASE_URL}/{employee_id}")
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    employee = response.json()
    validate_employee_schema(employee)
    assert employee['FirstName'] == employees[0]['FirstName']


def test_update_employee(employee_id):
    """Test case for updating an employee."""
    updated_data = {"JobTitle": "Senior Test Engineer"}
    response = requests.put(f"{BASE_URL}/{employee_id}", json=updated_data)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Verify update
    response = requests.get(f"{BASE_URL}/{employee_id}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    employee = response.json()
    assert employee['JobTitle'] == "Senior Test Engineer"


def test_delete_employee(employee_id):
    """Test case for deleting an employee."""
    response = requests.delete(f"{BASE_URL}/{employee_id}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    # Verify deletion
    response = requests.get(f"{BASE_URL}/{employee_id}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


def test_invalid_employee_creation():
    """Test case for invalid employee creation."""
    invalid_employee = employees[0].copy()
    invalid_employee.pop("FirstName")
    response = requests.post(BASE_URL, json=invalid_employee)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
