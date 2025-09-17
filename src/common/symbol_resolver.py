# -*- coding: utf-8 -*-
"""
Symbol alias resolution for API integration.
"""
from typing import Dict, List, Optional
from .api_client import PerpsAPIClient


class SymbolResolver:
    """Handles symbol alias resolution and normalization."""
    
    def __init__(self, api_client: PerpsAPIClient = None):
        self.api_client = api_client
        self.aliases = {}  # symbol_raw -> symbol_canonical
        self.reverse_aliases = {}  # symbol_canonical -> [symbol_raw, ...]
        self.loaded = False
    
    async def load_aliases(self) -> None:
        """Load symbol aliases from API."""
        if self.loaded:
            return
        
        try:
            if not self.api_client:
                from .api_client import get_api_client
                async with get_api_client() as client:
                    response = await client.get_symbol_aliases()
            else:
                response = await self.api_client.get_symbol_aliases()
            
            # Build alias mappings
            self.aliases = {}
            self.reverse_aliases = {}
            
            for item in response.get('data', []):
                symbol_raw = item.get('symbol_raw', '')
                symbol_canonical = item.get('symbol_canonical', '')
                
                if symbol_raw and symbol_canonical:
                    self.aliases[symbol_raw] = symbol_canonical
                    
                    # Build reverse mapping
                    if symbol_canonical not in self.reverse_aliases:
                        self.reverse_aliases[symbol_canonical] = []
                    self.reverse_aliases[symbol_canonical].append(symbol_raw)
            
            self.loaded = True
            
        except Exception as e:
            print(f"Warning: Failed to load symbol aliases: {e}")
            # Continue without aliases
    
    def resolve_symbol(self, symbol: str) -> str:
        """Resolve symbol to canonical form using aliases."""
        if not symbol:
            return symbol
        
        # Return canonical symbol if alias exists, otherwise return original
        return self.aliases.get(symbol, symbol)
    
    def get_aliases_for_symbol(self, canonical_symbol: str) -> List[str]:
        """Get all aliases for a canonical symbol."""
        return self.reverse_aliases.get(canonical_symbol, [canonical_symbol])
    
    def normalize_symbol(self, symbol: str) -> str:
        """Normalize symbol and apply alias resolution."""
        if not symbol:
            return symbol
        
        # Basic normalization (from schema.py)
        s = (symbol or "").strip().upper()
        
        # Force -USD suffix if missing
        if "-" not in s and s:
            s = f"{s}-USD"
        
        # Apply alias resolution
        return self.resolve_symbol(s)
    
    def get_all_canonical_symbols(self) -> List[str]:
        """Get list of all canonical symbols."""
        return list(self.reverse_aliases.keys())
    
    def get_alias_count(self) -> int:
        """Get total number of aliases loaded."""
        return len(self.aliases)


# Global instance for easy access
_symbol_resolver = None

async def get_symbol_resolver(api_client: PerpsAPIClient = None) -> SymbolResolver:
    """Get global symbol resolver instance."""
    global _symbol_resolver
    
    if _symbol_resolver is None:
        _symbol_resolver = SymbolResolver(api_client)
        await _symbol_resolver.load_aliases()
    
    return _symbol_resolver
