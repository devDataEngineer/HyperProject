from src.read_extract import read_table
import pytest

def test_function_returns_counterparty_table():
    result = read_table("counterparty")
    assert isinstance(result, list)
    assert result[0]['commercial_contact'] == 'Micheal Toy'

def test_function_returns_currency_table():
    result = read_table("currency")
    assert isinstance(result, list)
    assert result[0]['currency_id'] == 1

def test_function_returns_department_table():
    result = read_table("department")
    assert isinstance(result, list)
    assert result[0]['department_name'] == 'Sales'

def test_function_returns_staff_table():
    result = read_table("staff")
    assert isinstance(result, list)
    assert result[0]['department_id'] == 2


def test_function_returns_design_table():
    result = read_table("design")
    assert isinstance(result, list)
    assert result[0]['design_id'] == 8   

def test_function_returns_sales_order_table():
    result = read_table("sales_order")
    assert isinstance(result, list)
    assert result[0]['agreed_delivery_location_id'] == 8   

def test_function_returns_address_table():
    result = read_table("address")
    assert isinstance(result, list)
    assert result[0]['address_line_1'] == '6826 Herzog Via'   

def test_function_returns_payment_table():
    result = read_table("payment")
    assert isinstance(result, list)
    assert result[0]['counterparty_ac_number'] == 31622269      

def test_function_returns_purchase_order_table():
    result = read_table("purchase_order")
    assert isinstance(result, list)
    assert result[0]['agreed_delivery_date'] == '2022-11-09'    

def test_function_returns_payment_type_table():
    result = read_table("payment_type")
    assert isinstance(result, list)
    assert result[0]['payment_type_id'] == 1

def test_function_returns_transaction_table():
    result = read_table("transaction")
    assert isinstance(result, list)
    assert result[0]['purchase_order_id'] == 2                     


def test_function_non_whitelist_string(): 
    with pytest.raises(ValueError):
        read_table("nonexist")
       
