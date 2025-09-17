# -*- coding: utf-8 -*-
"""
API client for Perps API integration.
"""
import asyncio
import aiohttp
import os
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode


class PerpsAPIClient:
    """Client for Perps API with caching and error handling."""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or "https://perps-node-d942af6814fa.herokuapp.com"
        self.api_key = api_key or os.getenv('API_KEY', '')
        self.session = None
        self.cache = {}
        self.cache_ttl = 600  # 10 minutes
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _get_cache_key(self, endpoint: str, params: Dict) -> str:
        """Generate cache key for endpoint and parameters."""
        return f"{endpoint}:{urlencode(sorted(params.items()))}"
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid."""
        if cache_key not in self.cache:
            return False
        
        import time
        cached_time, _ = self.cache[cache_key]
        return (time.time() - cached_time) < self.cache_ttl
    
    async def _get(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """Make GET request to API with caching."""
        if params is None:
            params = {}
        
        cache_key = self._get_cache_key(endpoint, params)
        
        # Check cache first
        if self._is_cache_valid(cache_key):
            _, data = self.cache[cache_key]
            return data
        
        # Make API request
        url = f"{self.base_url}{endpoint}"
        headers = {"x-api-key": self.api_key}
        
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status == 401:
                    raise Exception("Invalid API key")
                elif response.status == 429:
                    raise Exception("Rate limit exceeded")
                elif response.status != 200:
                    raise Exception(f"API error: {response.status}")
                
                data = await response.json()
                
                # Cache the response
                import time
                self.cache[cache_key] = (time.time(), data)
                
                return data
                
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
    
    async def get_latest_data(self, limit: int = 1000, exchange: str = None, symbol: str = None) -> Dict[str, Any]:
        """Get current market data for table."""
        params = {"limit": limit}
        if exchange:
            params["exchange"] = exchange
        if symbol:
            params["symbol"] = symbol
        
        return await self._get("/v1/marketcompare/latest_data", params)
    
    async def get_all_daily_data(self, limit: int = 10000, exchange: str = None, symbol: str = None) -> Dict[str, Any]:
        """Get ALL historical data for charts with smart pagination."""
        # Try single request first
        params = {"all": 1, "limit": limit}
        if exchange:
            params["exchange"] = exchange
        if symbol:
            params["symbol"] = symbol
        
        response = await self._get("/v1/marketcompare/daily_data", params)
        
        # If we got less data than requested, we have everything
        if len(response.get("data", [])) < limit:
            return response
        
        # If we got exactly the limit, check if there's more data
        check_params = params.copy()
        check_params["offset"] = limit
        check_params["limit"] = 1
        
        next_response = await self._get("/v1/marketcompare/daily_data", check_params)
        
        # If there's more data, use pagination
        if next_response.get("data"):
            return await self._get_all_daily_data_paginated(limit, exchange, symbol)
        
        return response
    
    async def _get_all_daily_data_paginated(self, limit: int, exchange: str = None, symbol: str = None) -> Dict[str, Any]:
        """Get ALL historical data with pagination for large datasets."""
        all_data = []
        offset = 0
        batch_size = 1000  # API max per request
        
        while len(all_data) < limit:
            remaining = limit - len(all_data)
            current_batch_size = min(batch_size, remaining)
            
            params = {"all": 1, "limit": current_batch_size, "offset": offset}
            if exchange:
                params["exchange"] = exchange
            if symbol:
                params["symbol"] = symbol
            
            response = await self._get("/v1/marketcompare/daily_data", params)
            batch_data = response.get("data", [])
            
            if not batch_data:
                break
                
            all_data.extend(batch_data)
            offset += current_batch_size
            
            # If we got less than requested, we're done
            if len(batch_data) < current_batch_size:
                break
        
        return {
            "cached": False,
            "data": all_data[:limit],
            "pagination": {"limit": limit, "offset": 0},
            "meta": {"total_fetched": len(all_data), "paginated": True}
        }
    
    async def get_symbol_aliases(self, limit: int = 1000) -> Dict[str, Any]:
        """Get symbol alias mappings."""
        return await self._get("/v1/marketcompare/symbol_aliases", {"limit": limit})
    
    async def get_symbol_registry(self, limit: int = 1000, exchange: str = None) -> Dict[str, Any]:
        """Get symbol registry."""
        params = {"limit": limit}
        if exchange:
            params["exchange"] = exchange
        
        return await self._get("/v1/marketcompare/symbol_registry", params)
    
    async def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        return await self._get("/v1/health")
    
    async def db_check(self) -> Dict[str, Any]:
        """Check database connectivity."""
        return await self._get("/v1/dbcheck")


# Convenience function for easy usage
async def get_api_client() -> PerpsAPIClient:
    """Get configured API client."""
    return PerpsAPIClient()
