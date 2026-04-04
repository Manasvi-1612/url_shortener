import hashlib
import base62


# Optional  
def canonicalize(url: str) -> str:
    """Normalize URL before hashing to avoid duplicate short codes."""
    url = url.strip().lower()
    # Remove default ports
    url = url.replace(":80/", "/").replace(":443/", "/")
    # Remove trailing slash
    url = url.rstrip("/")
    return url

def generate_short_code(long_url):
    res = hashlib.md5(long_url.encode('utf-8')).hexdigest() # hexadecimal

    truncated_hex = res[:12] # Since 1 byte(8 bits) equals 2 hex characters, 6 bytes = 12 hex characters, 12 hex characters = 48 bits 
    
    hash_int = int(truncated_hex,16) # Convert the truncated hexadecimal string to an integer using base 16 (hexadecimal) as the base. This will give you a large integer representation of the truncated hash, which can then be encoded into a shorter string using base62 encoding.
    
    short_code = base62.encode(hash_int)

    return short_code



def resolve_collision(long_url, attempt):
    """On collision, append a counter to the URL before re-hashing."""

    salted = f"{long_url}_{attempt}"
    hex_digest = hashlib.md5(salted.encode("utf-8")).hexdigest()
    truncated_hex = hex_digest[:12]
    hash_int = int(truncated_hex, 16)
    return base62.encode(hash_int)