from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

def canonicalize_url(url):
    """Canonicalizes a URL by sorting query parameters and optionally removing some."""
    remove_params = set(["utm_source", "utm_medium", "utm_campaign", "ref", "source"])

    parsed = urlparse(url)
    # Sort and filter query parameters
    query_params = parse_qsl(parsed.query, keep_blank_values=True)
    filtered_params = [(k, v) for k, v in query_params if k not in remove_params]
    sorted_params = sorted(filtered_params)

    # Rebuild the query string
    canonical_query = urlencode(sorted_params)

    # Rebuild the full URL
    canonical = parsed._replace(query=canonical_query, fragment="")
    return urlunparse(canonical)