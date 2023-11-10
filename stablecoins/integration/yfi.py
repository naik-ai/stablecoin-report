import asyncio
import json
from datetime import datetime
from pprint import pprint
from typing import Annotated

import yfinance as yf
from pandas import DataFrame as df

# TODO on yfi client
# [ ] get info data
# [ ] get end of the day close price and open price saved


class Yfi:
    def __init__(self, ticker: str) -> None:
        """
        Data input formats
        ticker: ste
        str_date: ISO 8601 format
        end_date: ISO 8601 format
        """
        self.ticker = ticker
        self.ticker_obj = yf.Ticker(self.ticker)

    def get_history(self, which="history", **kwargs):
        """
        INPUT:
        - history
            we need additional arguments
            - start: datetime | None
            - end: datetime | None
            - interval= '1d'
            - period= 'max'
        """
        data = getattr(self.ticker_obj, which)(**kwargs)
        data["ticker"] = self.ticker
        return json.loads(data.reset_index().to_json(orient="records"))

    def get_reports(self, which):
        """
        [ ] TODO
        Adding pydantic/Enum for input type
        INPUT:
            which: type of report
                - info
                - income_stmt
                - balance_sheet
        Output:
            This function gives out a dictionary report
        """

        data = getattr(self.ticker_obj, which)

        if type(data) == df:
            values = json.loads(self.unpivot_dfs(data).to_json(orient="records"))
            return values
        return [data]

    @staticmethod
    def unpivot_dfs(df):
        return (
            df.unstack()
            .reset_index(name="value")
            .rename(columns={"level_0": "year", "level_1": "report_name"})
        )


# EG: RUN this cmd:`pipenv run python -m stablecoins.integration.yahoo.yfi`
# if __name__ == "__main__":
#     reliance = Yfi(ticker="RELIANCE.NS")
#     pprint(reliance.get_history(period="max"))
