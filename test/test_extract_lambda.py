from src.extractlambda.extract import read_table
from unittest.mock import Mock
import pytest

read_table_mock=Mock()

def test_function_returns_counterparty_table():
    result = read_table("counterparty")
    mocked = read_table_mock.return_value = {'commercial_contact':'Micheal Toy'}
    assert isinstance(result[0], list)
    assert mocked['commercial_contact'] == 'Micheal Toy'

def test_function_returns_currency_table():
    result = read_table("currency")
    mocked = read_table_mock.return_value = {'currency_id':1}
    assert isinstance(result[0], list)
    assert mocked['currency_id'] == 1

def test_function_returns_department_table():
    result = read_table("department")
    mocked = read_table_mock.return_value = {'department_name':'Sales'}
    assert isinstance(result[0], list)
    assert mocked['department_name'] == 'Sales'

def test_function_returns_staff_table():
    result = read_table("staff")
    mocked = read_table_mock.return_value = {'department_id':2}
    assert isinstance(result[0], list)
    assert mocked['department_id'] == 2

def test_function_returns_design_table():
    result = read_table("design")
    mocked = read_table_mock.return_value = {'design_id':8}
    assert isinstance(result[0], list)
    assert mocked['design_id'] == 8   

def test_function_returns_sales_order_table():
    result = read_table("sales_order")
    mocked = read_table_mock.return_value = {'agreed_delivery_location_id':8}
    assert isinstance(result[0], list)
    assert mocked['agreed_delivery_location_id'] == 8   

def test_function_returns_address_table():
    result = read_table("address")
    mocked = read_table_mock.return_value = {'address_line_1':'6826 Herzog Via'}
    assert isinstance(result[0], list)
    assert mocked['address_line_1'] == '6826 Herzog Via'   

def test_function_returns_payment_table():
    result = read_table("payment")
    mocked = read_table_mock.return_value = {'counterparty_ac_number':31622269}
    assert isinstance(result[0], list)
    assert mocked['counterparty_ac_number'] == 31622269      

def test_function_returns_purchase_order_table():
    result = read_table("purchase_order")
    mocked = read_table_mock.return_value = {'agreed_delivery_date':'2022-11-09'}
    assert isinstance(result[0], list)
    assert mocked['agreed_delivery_date'] == '2022-11-09'    

def test_function_returns_payment_type_table():
    result = read_table("payment_type")
    mocked = read_table_mock.return_value = {'payment_type_id':1}
    assert isinstance(result[0], list)
    assert mocked['payment_type_id'] == 1

def test_function_returns_transaction_table():
    result = read_table("transaction")
    mocked = read_table_mock.return_value = {'purchase_order_id':2}
    assert isinstance(result[0], list)
    assert mocked['purchase_order_id'] == 2                     


def test_function_non_whitelist_string(): 
    with pytest.raises(ValueError):
        read_table("nonexist")
       
