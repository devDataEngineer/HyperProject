from src.loadlambda.load_dim_date import load_dim_date_to_warehouse
from dfmock import DFMock


    






# @pytest.fixture(scope="function")
# def sqlalchemy_declarative_base():
#     return Base

# @pytest.fixture(scope="function")
# def sqlalchemy_mock_config():
#     return [("user", [{"id": 1, "name": "Kevin"}, {"id": 2, "name": "Dwight"}])]


def test_load_fact_to_warehouse_stablish_connection(mocked_session):
    user = mocked_session.query(user).filter_by(id=2).first()
    assert user.name == "Dwight"



def test_load_fact_to_warehouse():
    colum = { "date_id": "datetime",
            "year": "integer",
            "month": "integer",
            "day": "integer",
            "day_of_week": "integer",
            "day_name": "string",
            "month_name": "string",
            "quarter": "integer"
          }
    
    dfmock = DFMock(count=2, columns=colum)
    dfmock.generate_dataframe()
    my_mocked_dataframe = dfmock.dataframe
    result = load_dim_date_to_warehouse(my_mocked_dataframe, "dim_date") 