import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


class SupabaseConfigurationError(RuntimeError):
    pass


def supabase_admin_configured():
    return bool(os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_SECRET_KEY'))


def _project_url():
    url = os.getenv('SUPABASE_URL')
    if not url:
        raise SupabaseConfigurationError('Configure SUPABASE_URL no arquivo .env.')
    return url


def get_supabase():
    url = _project_url()
    key = os.getenv('SUPABASE_KEY')
    if not key:
        raise SupabaseConfigurationError('Configure SUPABASE_KEY para leitura pública do Supabase.')
    return create_client(url, key)


def get_supabase_admin():
    url = _project_url()
    key = os.getenv('SUPABASE_SECRET_KEY')
    if not key:
        raise SupabaseConfigurationError(
            'Configure SUPABASE_SECRET_KEY para gerenciar integrantes com segurança.'
        )
    return create_client(url, key)
