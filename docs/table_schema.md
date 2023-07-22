# Table schema
## Training data(CTR)
|    Column    |         Type          | Collation | Nullable | Default|
|--------------|-----------------------|-----------|----------|--------|
| ad_id        | integer               |           | not null ||
| status       | boolean               |           | not null ||
| bidding_cpc  | integer               |           |          ||
| advertiser   | character varying(50) |           |          ||
| banner_style | character varying(50) |           |          ||
| category     | character varying(50) |           |          ||
| height       | real                  |           |          ||
| width        | real                  |           |          ||
| item_price   | real                  |           |          ||
| layout_style | character varying(50) |           |          ||
| hist_ctr     | real                  |           |          ||
| hist_cvr     | real                  |           |          ||
| was_click    | boolean               |           |          ||