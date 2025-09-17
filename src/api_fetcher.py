# -*- coding: utf-8 -*-
"""
API-based data fetcher for frontend integration.
This replaces the need for individual collectors when using the API.
"""
import asyncio
import argparse
import os
import sys
from typing import Dict, List, Any
from .common.api_client import PerpsAPIClient
from .common.symbol_resolver import SymbolResolver


async def fetch_all_data(api_key: str, output_dir: str) -> int:
    """Fetch all data from API and save to files."""
    try:
        async with PerpsAPIClient(api_key=api_key) as client:
            # Load symbol aliases first
            symbol_resolver = SymbolResolver(client)
            await symbol_resolver.load_aliases()
            
            # Fetch all data in parallel
            print("[api] Fetching latest data...")
            latest_response = await client.get_latest_data(limit=1000)
            
            print("[api] Fetching historical data...")
            historical_response = await client.get_all_daily_data(limit=10000)
            
            print("[api] Fetching symbol aliases...")
            aliases_response = await client.get_symbol_aliases(limit=1000)
            
            print("[api] Fetching symbol registry...")
            registry_response = await client.get_symbol_registry(limit=1000)
            
            # Process and save data
            os.makedirs(output_dir, exist_ok=True)
            
            # Save latest data
            latest_data = latest_response.get('data', [])
            with open(os.path.join(output_dir, 'latest_data.json'), 'w') as f:
                import json
                json.dump(latest_data, f, indent=2)
            print(f"[api] Saved {len(latest_data)} latest records")
            
            # Save historical data
            historical_data = historical_response.get('data', [])
            with open(os.path.join(output_dir, 'historical_data.json'), 'w') as f:
                json.dump(historical_data, f, indent=2)
            print(f"[api] Saved {len(historical_data)} historical records")
            
            # Save symbol aliases
            aliases_data = aliases_response.get('data', [])
            with open(os.path.join(output_dir, 'symbol_aliases.json'), 'w') as f:
                json.dump(aliases_data, f, indent=2)
            print(f"[api] Saved {len(aliases_data)} symbol aliases")
            
            # Save symbol registry
            registry_data = registry_response.get('data', [])
            with open(os.path.join(output_dir, 'symbol_registry.json'), 'w') as f:
                json.dump(registry_data, f, indent=2)
            print(f"[api] Saved {len(registry_data)} symbol registry entries")
            
            return 0
            
    except Exception as e:
        print(f"[error] Failed to fetch data from API: {e}")
        return 1


def main(argv=None) -> int:
    """Main entry point."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--api-key", default=os.getenv('API_KEY'), help="API key for authentication")
    ap.add_argument("--output-dir", default="data/api", help="Output directory for API data")
    args = ap.parse_args(argv)
    
    if not args.api_key:
        print("[error] API key required. Set API_KEY environment variable or use --api-key")
        return 1
    
    return asyncio.run(fetch_all_data(args.api_key, args.output_dir))


if __name__ == "__main__":
    raise SystemExit(main())
