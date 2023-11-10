import os

import dlt
from dotenv import dotenv_values

from .yfi import Yfi


@dlt.source
def yahoofi_source(ticker):
    yfi_client = Yfi(ticker=ticker)

    report_type = ["info", "balance_sheet", "income_stmt", "history"]
    for report in report_type:
        if report == "history":
            resource = yfi_client.get_history(which=report, period="max")
        else:
            resource = yfi_client.get_reports(which=report)

        print(f"Loading: {report} in yahoo_{report} table")
        yield dlt.resource(
            resource, name=f"yahoo_{report}_v1", write_disposition="replace"
        )


def yahoo_pipeline(ticker):
    p = dlt.pipeline(
        pipeline_name="yahoofi",
        destination="postgres",
        dataset_name="integrations",
        credentials=dlt.secrets.value,
    )
    yh_source = yahoofi_source(ticker=ticker)
    print(yh_source.resources.keys())
    load_info = p.run(yh_source)

    # pretty print the information on data that was loaded
    print(load_info)
