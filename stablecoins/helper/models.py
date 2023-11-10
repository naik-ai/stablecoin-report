import enum
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, HttpUrl


# DEFILAMMA
class DefilammaStables(BaseModel):
    id: int
    name: str
    symbol: str
    gecko_id: str
    pegType: str
    pegMechanism: str
    circulating: Optional[float]
    circulatingPrevDay: Optional[float]
    circulatingPrevWeek: Optional[float]
    circulatingPrevMonth: Optional[float]
    price: Optional[float]
    delisted: Optional[str]
    chains: Optional[List[str]]


class DefilammaHistory(BaseModel):
    date: int
    circulating_peggedUSD: Optional[float]
    circulating_peggedEUR: Optional[float]
    circulating_peggedVAR: Optional[float]
    minted_peggedUSD: Optional[float]
    unreleased_peggedUSD: Optional[float]
    bridgedTo_peggedUSD: Optional[float]
    bridgedTo_bridges: Optional[Dict]
    chain: Optional[str]
    minted_bridges: Optional[Dict]
    unreleased_bridges: Optional[Dict]
    id: int
    name: str
    address: Optional[str]
    symbol: Optional[str]
    url: Optional[str]
    description: Optional[str]
    mintRedeemDescription: Optional[str]
    onCoinGecko: Optional[bool]
    gecko_id: Optional[str]
    cmcId: Optional[int]
    pegType: Optional[str]
    pegMechanism: Optional[str]
    priceSource: Optional[str]
    auditLinks: Optional[List[str]]
    twitter: Optional[str]
    wiki: Optional[str]
    price: Optional[float]


class DefilammaStablesPrices(BaseModel):
    date: Optional[datetime]
    stablecoin: Optional[str]
    price: Optional[float]


class DefilammaHistTvl(BaseModel):
    date: Optional[datetime]
    tvl: Optional[float]


class DefilammaProtocols(BaseModel):
    id: str
    name: Optional[str]
    address: Optional[str]
    symbol: Optional[str]
    url: Optional[HttpUrl]
    description: Optional[str]
    chain: Optional[str]
    logo: Optional[HttpUrl]
    audits: Optional[str]
    audit_note: Optional[str]
    gecko_id: Optional[str]
    cmcId: Optional[str]
    category: Optional[str]
    chains: Optional[List[str]]
    module: Optional[str]
    twitter: Optional[str]
    forkedFrom: Optional[List[str]]
    oracles: Optional[List[str]]
    listedAt: Optional[int]
    slug: Optional[str]
    tvl: Optional[float]
    chainTvls: Optional[Dict]
    change_1h: Optional[float]
    change_1d: Optional[float]
    change_7d: Optional[float]
    tokenBreakdowns: Optional[Dict]
    mcap: Optional[float]
    referralUrl: Optional[HttpUrl]
    treasury: Optional[str]
    audit_links: Optional[List[HttpUrl]]
    openSource: Optional[str]
    governanceID: Optional[List[str]]
    github: Optional[List[str]]
    stablecoins: Optional[List[str]]
    parentProtocol: Optional[str]
    wrongLiquidity: Optional[str]
    staking: Optional[str]
    pool2: Optional[str]
    assetToken: Optional[str]
    language: Optional[str]
    oraclesByChain: Optional[List[str]]
    deadUrl: Optional[bool]
    rugged: Optional[bool]


class DefilammaYieldsPools(BaseModel):
    apy: Optional[float]
    apyBase: Optional[float]
    apyBase7d: Optional[float]
    apyBaseInception: Optional[float]
    apyMean30d: Optional[float]
    apyPct1D: Optional[float]
    apyPct30D: Optional[float]
    apyPct7D: Optional[float]
    apyReward: Optional[float]
    binnedConfidence: Optional[float]
    chain: Optional[str]
    count: Optional[int]
    exposure: Optional[str]
    il7d: Optional[float]
    ilRisk: Optional[str]
    mu: Optional[float]
    outlier: Optional[bool]
    pool: Optional[str]
    poolMeta: Optional[str]
    predictedClass: Optional[str]
    predictedProbability: Optional[float]
    project: Optional[str]
    rewardTokens: Optional[List[str]]
    sigma: Optional[float]
    stablecoin: Optional[bool]
    symbol: Optional[str]
    tvlUsd: Optional[int]
    underlyingTokens: Optional[List[str]]
    volumeUsd1d: Optional[float]
    volumeUsd7d: Optional[float]


# MAKERBURN


class MakerburnHistory(BaseModel):
    date: Optional[datetime]
    sai_cap: Optional[float]
    total_dai_supply: Optional[float]
    total_sai_supply: Optional[float]
    mkr_burned: Optional[float]
    annual_fees_sai: Optional[float]
    annual_interest_dsr: Optional[float]
    mcd_dsr_rate: Optional[float]
    mkr_price: Optional[float]
    annual_mkr_vesting: Optional[float]
    eth_price: Optional[float]
    dai_in_dsr: Optional[float]
    mkr_treasury: Optional[float]
    mkr_uni_pool: Optional[float]
    surplus: Optional[float]
    sb: Optional[float]
    psm_fees_monthly: Optional[float]
    liq_income_monthly: Optional[float]
    expenses_annually: Optional[float]
    dai_expenses_1_mth: Optional[float]
    dai_expenses_3_mth: Optional[float]
    dai_expenses_12_mth: Optional[float]
    psm_swap_fees_1_mth: Optional[float]
    psm_swap_fees_3_mth: Optional[float]
    psm_swap_fees_12_mth: Optional[float]
    liq_profit_1_mth: Optional[float]
    liq_profit_3_mth: Optional[float]
    liq_profit_12_mth: Optional[float]
    sc_dai: Optional[float]
    non_sc_dai: Optional[float]
    annual_fees: Optional[float]


class MakerburnCollateralList(BaseModel):
    type: Optional[str]
    name: Optional[str]
    ilk: Optional[str]
    psm_adr: Optional[str]
    is_uni_v2: Optional[int]
    is_rwa: Optional[int]
    symbol: Optional[str]
    is_sc: Optional[int]
    is_liq_2_0: Optional[int]
    jar_adr: Optional[str]
    dai: Optional[float]
    dai_ath: Optional[float]
    dai_change: Optional[float]
    cap_temp: Optional[float]
    cap_max: Optional[int]
    fee: Optional[float]
    fee_is_calculated: Optional[int]
    psm_fee_in: Optional[str]
    psm_fee_out: Optional[str]
    dc_iam_line: Optional[int]
    dc_iam_gap: Optional[int]
    dc_iam_ttl: Optional[int]
    price: Optional[float]
    next_price: Optional[float]
    locked: Optional[float]
    liq_ratio: Optional[float]
    auctions_open: Optional[int]
    auctions_total: Optional[int]
    debt_auctioned: Optional[float]
    debt_sold: Optional[float]
    liq_profit: Optional[float]
    dust: Optional[int]
    liq_2_0_hole: Optional[int]
    liq_2_0_chop: Optional[float]
    liq_2_0_buf: Optional[float]
    liq_2_0_tail: Optional[int]
    liq_2_0_cusp: Optional[float]
    liq_2_0_chip: Optional[float]
    liq_2_0_tip: Optional[int]
    liq_2_0_step: Optional[int]
    liq_2_0_cut: Optional[float]
    dai_yesterday: Optional[float]
    fee_yesterday: Optional[float]
    fees_owed: Optional[float]


class CollateralHistory(BaseModel):
    date: datetime
    dai_cap: str
    temp_dai_cap: str
    dai_total: str
    fee: str
    psm_fee_in: Optional[str]
    psm_fee_out: Optional[str]
    fees_owed: str
    liquidation_profit: Optional[str]
    price: str
    name: str


# COINGECKO
# CMC
#
