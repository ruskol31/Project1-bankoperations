import pandas as pd

from src.reports import spending_by_category
from src.services import cashback_analiser
from views import main_page

if __name__ == "__main__":
    print(main_page("2018.05.10 11:10:10"))
    # print(cashback_analiser(r'C:\pytnon\Project1 bankoperations\data\operations.xlsx', 2018, 5))

    df = pd.read_excel(r'C:\pytnon\Project1 bankoperations\data\operations.xlsx')
    result_report = spending_by_category(df, "Супермаркеты", "2018.05.10")
    print(result_report)

    print(cashback_analiser(r'C:\pytnon\Project1 bankoperations\data\operations.xlsx', 2019, 5))
