# For our destination table(postgres) we need an incremental sync, What this does
# 1. Pull metadata: last updated data based on the table
# 2. For every table create a schema metadata table: that has info on unique identifiers for that table -> date, ids


# This can be called: source sync pipline that gets trigged when data needs to be pulled from Postgres
