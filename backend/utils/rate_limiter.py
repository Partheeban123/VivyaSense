"""
Rate limiting utility for preventing spam
"""
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from loguru import logger as log


class RateLimiter:
    """
    Simple in-memory rate limiter
    
    Tracks requests by IP address and enforces rate limits.
    For production, consider using Redis for distributed rate limiting.
    """
    
    def __init__(self):
        # Structure: {ip_address: [(timestamp1, timestamp2, ...)]}
        self._requests: Dict[str, list] = defaultdict(list)
        self._cleanup_interval = timedelta(hours=2)
        self._last_cleanup = datetime.now()
    
    def _cleanup_old_requests(self):
        """Remove old request records to prevent memory bloat"""
        now = datetime.now()
        
        # Only cleanup every 2 hours
        if now - self._last_cleanup < self._cleanup_interval:
            return
        
        cutoff_time = now - timedelta(hours=2)
        
        # Remove old timestamps
        for ip in list(self._requests.keys()):
            self._requests[ip] = [
                ts for ts in self._requests[ip]
                if ts > cutoff_time
            ]
            
            # Remove IP if no recent requests
            if not self._requests[ip]:
                del self._requests[ip]
        
        self._last_cleanup = now
        log.info(f"Rate limiter cleanup completed. Active IPs: {len(self._requests)}")
    
    def is_rate_limited(
        self,
        ip_address: str,
        max_requests: int = 3,
        time_window: timedelta = timedelta(hours=1)
    ) -> tuple[bool, Optional[int]]:
        """
        Check if an IP address has exceeded the rate limit
        
        Args:
            ip_address: IP address to check
            max_requests: Maximum number of requests allowed
            time_window: Time window for rate limiting
        
        Returns:
            tuple: (is_limited, seconds_until_reset)
                - is_limited: True if rate limit exceeded
                - seconds_until_reset: Seconds until rate limit resets (None if not limited)
        """
        self._cleanup_old_requests()
        
        now = datetime.now()
        cutoff_time = now - time_window
        
        # Get recent requests for this IP
        recent_requests = [
            ts for ts in self._requests[ip_address]
            if ts > cutoff_time
        ]
        
        # Update the requests list
        self._requests[ip_address] = recent_requests
        
        # Check if rate limit exceeded
        if len(recent_requests) >= max_requests:
            # Calculate when the oldest request will expire
            oldest_request = min(recent_requests)
            reset_time = oldest_request + time_window
            seconds_until_reset = int((reset_time - now).total_seconds())
            
            log.warning(
                f"Rate limit exceeded for IP {ip_address}. "
                f"Requests: {len(recent_requests)}/{max_requests}. "
                f"Reset in {seconds_until_reset}s"
            )
            
            return True, max(seconds_until_reset, 0)
        
        return False, None
    
    def record_request(self, ip_address: str):
        """
        Record a new request from an IP address
        
        Args:
            ip_address: IP address making the request
        """
        now = datetime.now()
        self._requests[ip_address].append(now)
        log.debug(f"Recorded request from IP {ip_address}. Total: {len(self._requests[ip_address])}")
    
    def get_request_count(
        self,
        ip_address: str,
        time_window: timedelta = timedelta(hours=1)
    ) -> int:
        """
        Get the number of requests from an IP in the time window
        
        Args:
            ip_address: IP address to check
            time_window: Time window to check
        
        Returns:
            int: Number of requests in the time window
        """
        now = datetime.now()
        cutoff_time = now - time_window
        
        recent_requests = [
            ts for ts in self._requests.get(ip_address, [])
            if ts > cutoff_time
        ]
        
        return len(recent_requests)
    
    def reset_ip(self, ip_address: str):
        """
        Reset rate limit for a specific IP address
        
        Args:
            ip_address: IP address to reset
        """
        if ip_address in self._requests:
            del self._requests[ip_address]
            log.info(f"Rate limit reset for IP {ip_address}")


# Global rate limiter instance
rate_limiter = RateLimiter()

