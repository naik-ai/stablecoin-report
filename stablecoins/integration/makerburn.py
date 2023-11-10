import dlt
import pandas as pd
from dlt.common.libs.pydantic import pydantic_to_table_schema_columns
from dlt.sources.helpers import requests

from stablecoins.helper import models
from stablecoins.integration.urls import makerburn as url


@dlt.resource(
    table_name="makerburn_history",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(models.MakerburnHistory),
)
def makerburn_history():
    response = requests.get(url["MAKERBURN_URL_HIST"])
    response.raise_for_status()
    yield response.json()


@dlt.resource(
    table_name="makerburn_collateral_list",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(models.MakerburnCollateralList),
)
def collateral_list(makerburn_url_status=dlt.config.value):
    response = requests.get(url["MAKERBURN_URL_STATUS"])
    response.raise_for_status()
    data = response.json()
    yield data["collateral_list"]


# after getting this just pull the id's and loop it to the history
@dlt.transformer(
    data_from=collateral_list,
    table_name="makerburn_collateral_history",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(models.CollateralHistory),
)
def collateral_history(
    collaterallist,
):
    for collatoral in collaterallist:
        print(f"Pulling data for {collatoral['type']}")
        makerburn_url_history = url["MAKERBURN_URL_HIST"]
        hist_url = f"{makerburn_url_history}/{collatoral['type']}"
        response = requests.get(hist_url)
        response.raise_for_status()
        data = response.json()
        history = data["history"]
        for day in history:
            day["name"] = collatoral["type"]

            for key in day:
                day[key] = str(day[key])

            print(f"for {collatoral['type']}: {day}")
        yield history


@dlt.source(max_table_nesting=0)
def makerburn_raw():
    return [makerburn_history, collateral_list, collateral_history]


def makerburn_pipeline() -> None:
    p = dlt.pipeline(
        pipeline_name="makeburn",
        destination="bigquery",
        dataset_name="raw",
        credentials=dlt.secrets.value,
    )
    print("pipeline running")
    p.run(makerburn_raw())


if __name__ == "__main__":
    print(makerburn_pipeline())
