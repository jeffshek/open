from open.core.utilities.cloudflare import get_dashboard_history


def run():
    """
    To run
    python manage.py runscript cloudflare_extract_historical_traffic
    """
    get_dashboard_history()
