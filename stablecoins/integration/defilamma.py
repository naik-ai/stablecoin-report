from pprint import pprint
from typing import Any, Dict, Iterator, List, Literal, Sequence
from pathlib import Path
import dlt
import pandas as pd
from defillama2 import DefiLlama
from dlt.common.libs.pydantic import pydantic_to_table_schema_columns
from dlt.common.typing import TDataItem, TDataItems
from dlt.extract.source import DltResource
from dlt.sources.helpers import requests
from prefect import flow, serve, task
import google.cloud.bigquery
from prefect_gcp import GcpCredentials, GcpSecret
from stablecoins.helper import models
from stablecoins.integration.urls import defilamma as url
from prefect_dbt.cli.commands import DbtCoreOperation


# (EL)T: DLT- via Prefect
dl = DefiLlama()


@dlt.resource(
    table_name="defilamma_stables",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(models.DefilammaStables),
)
def defilamma_stables() -> Iterator[TDataItems]:
    stablecoins_list_url = url["STABLECOINS_LIST_URL"]
    resp = requests.get(stablecoins_list_url)
    resp.raise_for_status()
    lst = resp.json()["peggedAssets"]
    res = []
    res_chains = []
    for d0 in lst:
        _ = d0.pop("chainCirculating")
        chains = d0.pop("chains")
        res.append(pd.DataFrame(d0).reset_index(drop=True))
        res_chains.append(chains)
    df = pd.concat(res)
    df["chains"] = res_chains
    del df["priceSource"]
    df["id"] = df.id.astype(int)
    df["price"] = df["price"].astype(float)
    skip_null_price = ~df["price"].isna()
    yield df[skip_null_price].to_dict(orient="records")


@staticmethod
def flatten_stablecoins_historical_token(data: dict) -> list[dict]:
    chain_bals = data.pop("chainBalances", None)
    data.pop("tokens")
    data.pop("currentChainBalances", None)

    stable_chains_hist = []

    for chain, value in chain_bals.items():
        print(chain)
        df_chain_balances = pd.json_normalize(
            value,
            record_path=[
                "tokens",
            ],
            max_level=1,
            sep="_",
        )
        df_chain_balances["chain"] = chain

        if "bridgedTo.bridges" in df_chain_balances.columns:
            df_chain_balances.drop(columns="bridgedTo.bridges", inplace=True)
        stable_chains_hist.append(df_chain_balances)

    hist = pd.concat(stable_chains_hist, ignore_index=True).to_dict(orient="records")
    info = pd.json_normalize(data, sep="_").to_dict(orient="records")[0]

    return [{**s, **info} for s in hist]


@dlt.transformer(
    data_from=defilamma_stables,
    write_disposition="replace",
    table_name="defilamma_stables_history",
    columns=pydantic_to_table_schema_columns(models.DefilammaHistory),
)
def defilamma_stables_history(stable_coin_ids) -> Iterator[TDataItems]:
    all_data = []
    stablecoin_url = url["STABLECOIN_URL"]
    for sc in stable_coin_ids:
        resp = requests.get(f"{stablecoin_url}{sc['id']}")
        resp.raise_for_status()
        data = flatten_stablecoins_historical_token(data=resp.json())
        all_data.extend(data)
    yield all_data


@dlt.resource(
    table_name="defilamma_stables_prices",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(models.DefilammaStablesPrices),
)
def defilamma_stable_prices() -> Iterator[TDataItems]:
    """Get historical pricing for all stables"""
    df = dl.get_stablecoins_prices()
    yield df.reset_index().to_dict(orient="records")


# TVL: Total tvl by date
@dlt.resource(
    table_name="defilamma_hist_tvl",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(models.DefilammaHistTvl),
)
def defilamma_hist_tvl() -> Iterator[TDataItems]:
    yield dl.get_defi_hist_tvl().reset_index().to_dict(orient="records")


#  TVL:


# Protocols
@dlt.resource(
    table_name="defilamma_protocols",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(models.DefilammaProtocols),
)
def defilamma_protocols() -> Iterator[TDataItems]:
    yield dl.get_protocols().to_dict(orient="records")


# Yields
@dlt.resource(
    table_name="defilamma_yields_pools",
    write_disposition="replace",
    columns=pydantic_to_table_schema_columns(models.DefilammaYieldsPools),
)
def defilamma_yields_pools() -> Iterator[TDataItems]:
    df = dl.get_pools_yields()
    yield df.to_dict(orient="records")


# Sources
# @task
@dlt.source(
    max_table_nesting=0,
)
def defilamma_raw() -> Sequence[DltResource]:
    return [
        defilamma_protocols,
        defilamma_yields_pools,
        defilamma_stables,
        defilamma_stables_history(),
        defilamma_stable_prices,
    ]


@flow(name="defilamma get pipeline")
async def defilamma_get_pipeline() -> None:
    p = dlt.pipeline(
        pipeline_name="defilamma",
        destination="bigquery",
        dataset_name="raw",
        credentials=dlt.secrets.value,
    )
    p.run(defilamma_raw())


# EL(T): DBT- via Prefect
@flow(name="defilamma Transform pipeline")
def defilamma_t_pipeline() -> None:
    "This run DBT transformations for all models"

    pass


@flow
def secret_manager_flow():
    gcp_credentials_block = GcpCredentials.load("dataengg")
    gcp_secret = GcpSecret(secret_name="prefect_block_2", gcp_credentials=gcp_credentials_block)
    return gcp_secret.read_secret()


@flow
def create_bigquery_client():
    gcp_credentials = GcpCredentials.load("dataengg")
    bigquery_client = gcp_credentials.get_client("bigquery")
    return bigquery_client


def defilamma_pipeline() -> None:
    "This run DLT data pull and load + DBT transformations for all models"
    # defilamma_get_pipeline.serve(name="defilamma_get_pipeline-deployment", cron="0 8 * * *")

    get_p = defilamma_get_pipeline.to_deployment("defilamma_get_pipeline-deployment")
    t_p = defilamma_t_pipeline.to_deployment("defilamma_t_pipeline-deployment", tags=["dev"])
    # serve(get_p, t_p, cron="0 8 * * *")


@flow
def trigger_dbt_flow() -> str:
    result = DbtCoreOperation(
        commands=["pwd", "dbt debug", "dbt run"], project_dir=Path("actuarial_dbt")
    ).run()
    return result


if __name__ == "__main__":
    "Running DLT defilamma"
    p = dlt.pipeline(
        pipeline_name="defilamma",
        destination="bigquery",
        dataset_name="raw",
        credentials=dlt.secrets.value,
    )
    p.run(defilamma_raw())
