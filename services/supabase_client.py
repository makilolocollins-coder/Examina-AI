from supabase import Client, create_client

from config.settings import get_supabase_config


def get_supabase_client() -> Client:
    """
    Create the server-side Supabase client.

    The key is loaded from Streamlit Secrets and is never
    stored in GitLab.
    """

    supabase_url, supabase_key = get_supabase_config()

    return create_client(
        supabase_url,
        supabase_key
    )
