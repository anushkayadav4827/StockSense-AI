import pytest
import pandas as pd
from data_provider import get_company_logo_url

def test_company_logo_url():
    url = get_company_logo_url("AAPL", "https://www.apple.com")
    assert "clearbit.com" in url or "apple.com" in url
    
    url_no_domain = get_company_logo_url("TSLA", None)
    assert url_no_domain is None or "clearbit" in url_no_domain
