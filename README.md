# Market Comparer — API-Powered

> A real-time market comparison tool for **Drift**, **Hyperliquid**, and **dYdX** markets (pairs, leverage, 24h volume, OI) powered by the Perps API with symbol alias resolution and advanced filtering.

---

## What this repo does

* **API Integration** fetches real-time data:
  * `src/common/api_client.py` - Perps API client with smart pagination & caching
  * `src/common/symbol_resolver.py` - Symbol alias resolution system
  * `src/api_fetcher.py` - API-based data fetcher (optional backend)
  * `src/orchestrate_api.py` - API orchestration script (optional)

* **Real-time Data Sources**:
  * Latest market data (1000+ records)
  * Complete historical data (10,000+ records with smart pagination)
  * Symbol aliases (1000+ mappings)
  * Symbol registry (1000+ symbols)

* **UI (`index.html`)**:
  * **Real-time data** from Perps API (no file dependencies)
  * **Symbol alias resolution** - complex symbols → canonical forms
  * **Advanced filtering** (symbol, market type, presence filters)
  * **Sortable columns** (Leverage, Vol, OI, Vol/OI, "vs Baseline" ×)
  * **Interactive charts** (Volume & OI with rolling averages)
  * **Change tracking** (market type / leverage changes over time)
  * **Progress indicators** during data loading
  * **Error handling** with user-friendly messages

## How it works

### API-Powered Architecture

* **Frontend** loads data directly from Perps API
* **Pagination** handles large datasets (1000+ records per batch)
* **Caching** reduces API calls (10-minute TTL)
* **Symbol aliases** resolve complex symbols automatically
* **Real-time updates** with progress indicators

### Data Flow

1. **Page Load** → API calls for latest data, historical data, symbol aliases
2. **Symbol Resolution** → Complex symbols mapped to canonical forms
3. **Data Processing** → Filtering, sorting, chart preparation
4. **User Interaction** → Instant chart loading from preloaded data

---

## Configuration

### Local Development
1. Copy `config.js.example` to `config.js`:
   ```bash
   cp config.js.example config.js
   ```
2. Update `config.js` with your API key:
   ```javascript
   window.API_KEY = 'your-api-key-here';
   ```

### Production
1. Set `API_KEY` as a GitHub Secret
2. Deploy - no additional configuration needed

---

## API Endpoints

* `GET /v1/marketcompare/latest_data` - Current market data
* `GET /v1/marketcompare/daily_data` - Historical data (with pagination)
* `GET /v1/marketcompare/symbol_aliases` - Symbol mappings (with pagination)
* `GET /v1/marketcompare/symbol_registry` - Symbol registry (with pagination)

---

## Features

### Symbol Alias Resolution
- **Automatic mapping**: `FARTCOIN,RAYDIUM,9BB6NFECJBCTNNLFKO2FQVQBQ8HHM13KCYYCDQBGPUMP-USD` → `FARTCOIN-USD`
- **Real-time resolution** during data processing
- **Transparent to users** - works automatically

### Pagination & Performance
- **Large datasets**: Handles 50,000+ historical records
- **Batch loading**: 1000 records per API call
- **Progress indicators**: Real-time loading status
- **Caching**: 10-minute TTL reduces API calls

### Error Handling
- **Network errors**: Graceful fallbacks with user messages
- **API errors**: Specific error handling (401, 429, etc.)
- **Loading states**: Progress bars and status updates

---

## Migration from GitHub Files

This project has been migrated from GitHub raw file dependencies to the Perps API:

### Before (GitHub Files)
- File-based data loading
- Manual symbol management
- Limited to 1000 records
- No real-time updates

### After (API Integration)
- Real-time API data
- Automatic symbol alias resolution
- Pagination for unlimited records
- Live updates with caching
- Better error handling

See `API_MIGRATION.md` for detailed migration information.

---

## UI Features

* **Real-time data** from Perps API
* **Symbol filtering** with alias resolution
* **Market type filtering** (CROSS/ISOLATED)
* **Presence filtering** (Not on specific exchanges)
* **Baseline comparison** (Vol/OI ratios vs selected exchange)
* **Interactive charts** with rolling averages
* **Change tracking** over time
* **Date-only timestamps** (updates hourly)
* **Responsive design** with dark theme
