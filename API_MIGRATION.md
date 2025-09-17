# API Migration Guide

This document describes the migration from GitHub raw files to the Perps API.

## Overview

The system has been migrated from using GitHub raw files to using the Perps API for data fetching. This provides better performance, caching, and real-time data access.

## Changes Made

### 1. Frontend (index.html)
- **Replaced** GitHub CSV fetching with API calls
- **Added** API client with caching and error handling
- **Added** symbol alias resolution
- **Added** progress indicators and error messages
- **Added** support for loading all historical data at once

### 2. Backend
- **Created** `src/common/api_client.py` - API client with caching
- **Created** `src/common/symbol_resolver.py` - Symbol alias resolution
- **Created** `src/api_fetcher.py` - API-based data fetcher
- **Created** `src/orchestrate_api.py` - API-based orchestration
- **Updated** `src/common/schema.py` - Added symbol alias support

### 3. Configuration
- **Created** `config.js` - API key configuration for local development
- **Updated** `requirements.txt` - Added aiohttp dependency

## API Endpoints Used

- `GET /v1/marketcompare/latest_data` - Current market data
- `GET /v1/marketcompare/daily_data` - Historical data
- `GET /v1/marketcompare/symbol_aliases` - Symbol alias mappings
- `GET /v1/marketcompare/symbol_registry` - Symbol registry

## Configuration

### Local Development
1. Copy `config.js` and update with your API key:
   ```javascript
   window.API_KEY = 'your-api-key-here';
   ```

### Production (GitHub Actions)
1. Set `API_KEY` as a GitHub Secret
2. The HTML will automatically read from the environment

## Usage

### Frontend
The frontend now automatically loads data from the API on page load. No changes needed for users.

### Backend (Optional)
If you need to fetch data programmatically:
```bash
# Using the API fetcher
python -m src.orchestrate_api --api-key YOUR_KEY

# Or set environment variable
export API_KEY=your-key
python -m src.orchestrate_api
```

## Features

### Symbol Alias Resolution
- Automatically resolves complex symbols to canonical forms
- Example: `FARTCOIN,RAYDIUM,9BB6NFECJBCTNNLFKO2FQVQBQ8HHM13KCYYCDQBGPUMP-USD` → `FARTCOIN-USD`

### Caching
- API responses are cached for 10 minutes
- Reduces API calls and improves performance

### Error Handling
- Graceful error handling with user-friendly messages
- Progress indicators during data loading
- Fallback error display in table

### Performance
- Loads all data in parallel for faster initial load
- Preloads historical data for instant chart rendering
- Efficient symbol resolution

## Migration Benefits

1. **Real-time Data**: Direct API access instead of file-based updates
2. **Better Performance**: Caching and parallel loading
3. **Symbol Aliases**: Automatic symbol resolution
4. **Error Handling**: Better user experience
5. **Scalability**: API can handle more requests than file serving

## Troubleshooting

### API Key Issues
- Ensure `API_KEY` is set in `config.js` for local development
- Ensure `API_KEY` GitHub Secret is set for production

### Network Issues
- Check API endpoint availability
- Verify API key permissions
- Check browser console for error messages

### Data Issues
- Verify API responses in browser network tab
- Check symbol alias mappings
- Ensure data format matches expected schema
