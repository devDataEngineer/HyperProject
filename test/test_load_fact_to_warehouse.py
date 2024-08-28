from src.loadlambda.load_fact_to_warehouse import load_fact_to_warehouse
from dfmock import DFMock



def test_load_fact_to_warehouse():
    colum = { "sales_record_id": "integer",
            "sales_order_id": "integer",
            "created_date": "datetime",
            "created_time": "datetime",
            "last_updated_date": "datetime",
            "last_updated_time": "datetime",
            "sales_staff_id": "integer",
            "counterparty_id": "integer",
            "units_sold": "integer",
            "unit_price": "integer",
            "currency_id": "integer",
            "design_id": "integer",
            "agreed_payment_date": "datetime",
            "agreed_delivery_date": "datetime",
            "agreed_delivery_location_id": "integer"
          }
    
    dfmock = DFMock(count=2, columns=colum)
    dfmock.generate_dataframe()
    my_mocked_dataframe = dfmock.dataframe
    result = load_fact_to_warehouse(my_mocked_dataframe, "fact_sales_order") 