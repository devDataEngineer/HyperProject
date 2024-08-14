from src.read_extract import read_table
import pytest


def test_function_returns_counterparty_table():
    result = read_table("counterparty")
    assert isinstance(result, list)

def test_function_returns_currency_table():
    result = read_table("currency")
    assert isinstance(result, list)

def test_function_returns_department_table():
    result = read_table("department")
    assert isinstance(result, list)

def test_function_returns_staff_table():
    result = read_table("staff")
    assert isinstance(result, list)

def test_function_returns_design_table():
    result = read_table("design")
    assert isinstance(result, list)   

def test_function_returns_sales_order_table():
    result = read_table("sales_order")
    assert isinstance(result, list) 

def test_function_returns_address_table():
    result = read_table("address")
    assert isinstance(result, list) 

def test_function_returns_payment_table():
    result = read_table("payment")
    assert isinstance(result, list)    

def test_function_returns_purchase_order_table():
    result = read_table("purchase_order")
    assert isinstance(result, list)  

def test_function_returns_payment_type_table():
    result = read_table("payment_type")
    assert isinstance(result, list) 

def test_function_returns_transaction_table():
    result = read_table("transaction")
    assert isinstance(result, list)                   


def test_function_non_whitelist_string(): 
    with pytest.raises(ValueError):
        read_table("nonexist")