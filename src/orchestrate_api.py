# -*- coding: utf-8 -*-
"""
API-based orchestrator: fetch data from API instead of running collectors.

Usage:
  # Fetch all data from API
  python -m src.orchestrate_api

  # Fetch with specific API key
  python -m src.orchestrate_api --api-key YOUR_KEY
"""
import argparse
import os
import sys
import asyncio
from .api_fetcher import fetch_all_data


def main(argv=None) -> int:
    """Main entry point for API-based orchestration."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--api-key", default=os.getenv('API_KEY'), help="API key for authentication")
    ap.add_argument("--output-dir", default="data/api", help="Output directory for API data")
    args = ap.parse_args(argv)
    
    if not args.api_key:
        print("[error] API key required. Set API_KEY environment variable or use --api-key")
        return 1
    
    print(f"[orchestrate-api] Fetching data from API to {args.output_dir}")
    
    # Fetch all data from API
    result = asyncio.run(fetch_all_data(args.api_key, args.output_dir))
    
    if result == 0:
        print("[orchestrate-api] Successfully fetched all data from API")
    else:
        print("[orchestrate-api] Failed to fetch data from API")
    
    return result


if __name__ == "__main__":
    raise SystemExit(main())
