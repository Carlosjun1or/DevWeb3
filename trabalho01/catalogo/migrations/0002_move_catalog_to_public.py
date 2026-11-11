from django.db import migrations


TABLES = ('catalogo_categoria', 'catalogo_servico')
POLICY_NAMES = {
    'catalogo_categoria': 'catalogo_categoria_public_read',
    'catalogo_servico': 'catalogo_servico_public_read',
}


def _table_schema(cursor, table_name):
    cursor.execute(
        '''
        SELECT namespace.nspname
        FROM pg_class AS relation
        JOIN pg_namespace AS namespace ON namespace.oid = relation.relnamespace
        WHERE relation.relname = %s
          AND relation.relkind IN ('r', 'p')
          AND namespace.nspname IN ('django', 'public')
        ''',
        [table_name],
    )
    schemas = [row[0] for row in cursor.fetchall()]
    if len(schemas) != 1:
        raise RuntimeError(
            f'Expected one django/public table named {table_name}; found {schemas}.'
        )
    return schemas[0]


def move_catalog_to_public(apps, schema_editor):
    connection = schema_editor.connection
    if connection.vendor != 'postgresql':
        return

    with connection.cursor() as cursor:
        for table_name in TABLES:
            current_schema = _table_schema(cursor, table_name)
            if current_schema == 'django':
                cursor.execute(
                    f'ALTER TABLE django.{table_name} SET SCHEMA public'
                )

        cursor.execute(
            "SELECT rolname FROM pg_roles "
            "WHERE rolname IN ('anon', 'authenticated', 'service_role')"
        )
        roles = {row[0] for row in cursor.fetchall()}

        for table_name, policy_name in POLICY_NAMES.items():
            cursor.execute(
                f'ALTER TABLE public.{table_name} ENABLE ROW LEVEL SECURITY'
            )
            cursor.execute(
                f'DROP POLICY IF EXISTS {policy_name} ON public.{table_name}'
            )
            cursor.execute(f'REVOKE ALL ON TABLE public.{table_name} FROM PUBLIC')

            for role in ('anon', 'authenticated'):
                if role in roles:
                    cursor.execute(
                        f'REVOKE ALL ON TABLE public.{table_name} FROM {role}'
                    )

            if {'anon', 'authenticated'} <= roles:
                cursor.execute(
                    f'CREATE POLICY {policy_name} ON public.{table_name} '
                    'FOR SELECT TO anon, authenticated USING (true)'
                )
                cursor.execute(
                    f'GRANT SELECT ON TABLE public.{table_name} '
                    'TO anon, authenticated'
                )

        if {'anon', 'authenticated'} <= roles:
            cursor.execute(
                'GRANT USAGE ON SCHEMA public TO anon, authenticated'
            )

        if 'service_role' in roles:
            for table_name in TABLES:
                cursor.execute(
                    f'GRANT ALL PRIVILEGES ON TABLE public.{table_name} '
                    'TO service_role'
                )
                cursor.execute(
                    f'GRANT USAGE, SELECT ON SEQUENCE '
                    f'public.{table_name}_id_seq TO service_role'
                )


def move_catalog_to_django(apps, schema_editor):
    connection = schema_editor.connection
    if connection.vendor != 'postgresql':
        return

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT rolname FROM pg_roles "
            "WHERE rolname IN ('anon', 'authenticated', 'service_role')"
        )
        roles = {row[0] for row in cursor.fetchall()}

        for table_name, policy_name in POLICY_NAMES.items():
            cursor.execute(
                f'DROP POLICY IF EXISTS {policy_name} ON public.{table_name}'
            )
            cursor.execute(
                f'ALTER TABLE public.{table_name} DISABLE ROW LEVEL SECURITY'
            )
            cursor.execute(
                f'REVOKE ALL ON TABLE public.{table_name} FROM PUBLIC'
            )
            for role in roles:
                cursor.execute(
                    f'REVOKE ALL ON TABLE public.{table_name} FROM {role}'
                )

        for table_name in reversed(TABLES):
            cursor.execute(
                f'ALTER TABLE public.{table_name} SET SCHEMA django'
            )


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0001_initial'),
        ('pedidos', '0003_pedidoitem'),
    ]

    operations = [
        migrations.RunPython(move_catalog_to_public, move_catalog_to_django),
    ]
