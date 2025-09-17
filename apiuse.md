# Perps API — Usage

Base URL: `https://perps-node-1234.herokuapp.com`

Auth: send header `x-api-key: <YOUR_KEY>`

## Endpoints

### 1) Health (no DB)

**GET** `/v1/health`
Returns process status.

```bash
curl https://perps-node-12345.herokuapp.com/v1/health
```

### 2) DB check

**GET** `/v1/dbcheck`
Checks DB connectivity.

```bash
curl https://perps-node-12345.herokuapp.com/v1/dbcheck -H "x-api-key: <YOUR_KEY>"
```

### 3) Facts (table: `md.facts_perps`)

**GET** `/v1/facts`

**Filters:** `date`, `date_gte`, `date_lte`, `exchange`, `instrument_id`, `symbol`

**Sorting:** `sort` in {`date`,`exchange`,`instrument_id`,`symbol`,`price`,`volume_usd`,`open_interest_usd`}, `order` = asc|desc

**Pagination:** `limit` (default 100, max 1000), `offset`

**Cache:** `nocache=1` to bypass

**Clamp:** last 30 days by default. Pass `all=1` or explicit dates to scan full history.

Numbers are JSON strings (high precision).

#### Examples

```bash
# Last 30 days, 5 rows
curl "https://perps-node-12345.herokuapp.com/v1/facts?limit=5" -H "x-api-key: <YOUR_KEY>"

# Full history, latest first
curl "https://perps-node-12345.herokuapp.com/v1/facts?all=1&limit=5&sort=date&order=desc" -H "x-api-key: <YOUR_KEY>"

# Filtered
curl "https://perps-node-12345.herokuapp.com/v1/facts?all=1&exchange=Binance&symbol=BTC/USDT&limit=10" -H "x-api-key: <YOUR_KEY>"
```

### 4) Depth (table: `md.depth_2pct_snapshots`)

**GET** `/v1/depth`

**Filters:** `date`, `date_gte`, `date_lte`, `exchange`, `instrument_id`, `symbol`

**Sorting:** `sort` in {`date`,`exchange`,`instrument_id`,`symbol`,`bids_usd`,`asks_usd`}, `order` = asc|desc

**Pagination, cache, clamp:** same as `/v1/facts`

#### Examples

```bash
curl "https://perps-node-12345.herokuapp.com/v1/depth?all=1&limit=5&sort=date&order=desc" -H "x-api-key: <YOUR_KEY>"
```

---

## PowerShell tips (Windows)

PowerShell’s `curl` is `Invoke-WebRequest`. Use either:

```powershell
curl.exe "https://.../v1/dbcheck" -H "x-api-key: <YOUR_KEY>"

# or
Invoke-WebRequest "https://perps-node-12345.herokuapp.com/v1/dbcheck" -Headers @{ "x-api-key"="<YOUR_KEY>" } | Select-Object -Expand Content
```

---

## Responses

### Success

```json
{
  "cached": false,
  "data": [ { "date":"2025-09-08", "exchange":"Binance", ... } ],
  "pagination": { "limit": 5, "offset": 0 },
  "meta": { "sort":"date", "order":"DESC", "where":"...", "ms": 3373 }
}
```

### Errors

* `401` { "error":"unauthorized" }
* `400` { "error":"invalid\_params", ... }
* `429` { "message":"Too many requests" }
* `500` { "error":"query\_failed", "message":"..." }

---

## Caching and performance

* Server cache TTL: 10 min (configurable).
* First query after dyno boot may be slow (extension load + cold caches).
* Prefer date filters for large scans; `all=1` forces full history.

---

## Rate limits

* Default 60 req/min per dyno (configurable via env).

---

## Versioning

* All routes under `/v1`.
* Breaking changes go to `/v2`.

---

## Adding more tables later

### Option A: New dedicated route (recommended)

Create a new route file (copy `src/routes/facts.js`) and update:

* Table name (e.g., `md.new_table`)
* Allowed sort columns
* Filter allowlist (only real columns)
* Wire it in `src/server.js` (e.g., `app.use('/v1/newtable', newtable)`).
* Push to GitHub → Heroku deploys.

Pros: strict validation, per-table tuning.
Cons: one file per table.

### Option B: Generic table endpoint with allowlist

Maintain a map:

```js
const TABLES = {
  facts: { name: 'md.facts_perps', sort: [...], filters: [...] },
  depth: { name: 'md.depth_2pct_snapshots', sort: [...], filters: [...] },
  // add more here
};
```

Route like `/v1/tables/:key` reads config from `TABLES[key]` and builds SQL.

Pros: less code to add new tables.
Cons: slightly looser separation; still safe with strict allowlist.

---

## Notes

* Keep numbers as strings in JSON for DECIMAL/HUGEINT.
* If you need floats, cast in SQL (precision loss).

---

## Config vars (Heroku)

* `MOTHERDUCK_TOKEN`
* `MOTHERDUCK_DATABASE=md:perps`
* `API_KEY`
* `CACHE_TTL_SECONDS=600`
* `RATE_LIMIT_MAX=60`
* `RATE_LIMIT_WINDOW_MS=60000`
* `NODE_ENV=production`
