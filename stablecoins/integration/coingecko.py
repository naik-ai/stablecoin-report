import dlt
from dotenv import dotenv_values
from pycoingecko import CoinGeckoAPI

config = dotenv_values("config/.env")


@dlt.resource(write_disposition="replace", table_name="cg_overview")
def cg_coin_overview(vs_currency="usd"):
    cg = CoinGeckoAPI()
    data = cg.get_coins_markets(vs_currency=vs_currency)
    # print(type(data))
    # print(data)
    yield data


@dlt.source(max_table_nesting=0)
def s_coin_gecko():
    yield cg_coin_overview()


def cg_pipline():
    p = dlt.pipeline(
        pipeline_name="cg_pipline",
        import_schema_path="schemas/import",
        export_schema_path="schemas/export",
        destination="postgres",
        dataset_name="integrations",
        credentials=config["pg_fintech_url"],
    )
    load_info = p.run(s_coin_gecko())
    print(load_info)


# if __name__ == "__main__":
#     cg_pipline()
