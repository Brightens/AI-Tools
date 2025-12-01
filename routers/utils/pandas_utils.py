from urllib.parse import urlparse


def parse_url_to_name(url: str):
    """
    Convert URL to filename (source name)
    """
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "").split(".")[0]
    
    path_parts = [p for p in parsed.path.split("/") if p]
    path = path_parts[0] if path_parts else "root"

    parsed_url = f"{domain}_{path}"

    return parsed_url
