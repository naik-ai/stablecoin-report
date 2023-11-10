---
title: Stablecoins Daily
sources:
  - summary_stats_protocol_stable_count: kpis/summary_stats_protocol_stable_count.sql
  - stablecoin_count_by_lauch_date: kpis/stablecoin_count_by_lauch_date.sql
  - stablecoin_peg_off_summary: kpis/stablecoin_peg_off_summary.sql
---

### Stablecoins Market

<BigValue
data={stablecoin_count_by_lauch_date}
title='Total Stablecoin lauched till date'
value='total_stablecoins'
maxWidth='20'
/>

<DataTable data={stablecoin_count_by_lauch_date} rowLines="false">
  <Column id="peg_mechanism" />
  <Column id="stablecoins" />
  <Column id="days_since_last_lauch" />
</DataTable>

The above table show protocol count for given number of Stablecoins they launched.

### Peg Analysis

For peg analysis, we will only consider stablecoins with marketcap of more than 20M.

- Protocols off pegs

  - When was last time peg went off
  - How long was peg off
  - Total number of peg off for a protocol
  - peg off by category(we hv 3)
  - Days from last peg was off
  - Days from first peg was off
  - currently peg off
  - No peg off till date
  - Accordian(based on the above KPIs)
    - peg KPI distributions and percentiles

<DataTable data={stablecoin_peg_off_summary} rowLines="false">
</DataTable>

<ScatterPlot
data={stablecoin_peg_off_summary}
x=days_since_last_peg_off
y= days_peg_off
/>

### Circulating Supply

- $ amount in stablecoins that are in ciculation
  - Sparkline of stablecoin last 30 days
- Categorical split of circulating supply
  - Sparkline of stablecoin last 30 days
- % change
  - over 7 days
- Stablecoins % marketcap YTD
  - YTD gains by top 3 coins
  - YTD marketshare loss by other coins
