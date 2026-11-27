"""One-time safe setup: create database if missing, schema, RLS, reader, Indian demo users."""
import json
from pathlib import Path
from psycopg import sql
from common import connect, DBNAME, READER_ROLE, READER_PASSWORD, TENANT
ROOT=Path(__file__).resolve().parent

def main():
    print('Starting bootstrap process...')
    if not READER_PASSWORD: raise RuntimeError('READER_PASSWORD is missing in .env')
    print('Checking database and roles...')
    with connect(server=True, autocommit=True) as db:
        print('Checking if database exists...')
        exists=db.execute('SELECT 1 FROM pg_database WHERE datname=%s',(DBNAME,)).fetchone()
        if not exists:
            db.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(DBNAME)))
            print(f'Created PostgreSQL database: {DBNAME}')
        else: print(f'Using existing PostgreSQL database: {DBNAME}')
    with connect(admin=True, register=False) as db:
        # DDL of an existing schema is non-destructive to existing documents.
        db.execute((ROOT/'sql/schema.sql').read_text())
        print('Checking if reader role exists...')
        role_exists=db.execute('SELECT 1 FROM pg_roles WHERE rolname=%s',(READER_ROLE,)).fetchone()
        if not role_exists:
            db.execute(sql.SQL('CREATE ROLE {} LOGIN PASSWORD {}').format(sql.Identifier(READER_ROLE),sql.Literal(READER_PASSWORD)))
            print(f'Created reader role: {READER_ROLE}')
        else:
            db.execute(sql.SQL('ALTER ROLE {} WITH LOGIN PASSWORD {}').format(sql.Identifier(READER_ROLE),sql.Literal(READER_PASSWORD)))
            print(f'Updated reader role password: {READER_ROLE}')
        db.execute(sql.SQL('GRANT CONNECT ON DATABASE {} TO {}').format(sql.Identifier(DBNAME),sql.Identifier(READER_ROLE)))
        print(f'Granted CONNECT on database {DBNAME} to {READER_ROLE}')
        db.execute(sql.SQL('GRANT USAGE ON SCHEMA chunk_rolebased_security TO {}').format(sql.Identifier(READER_ROLE)))
        print(f'Granted USAGE on schema chunk_rolebased_security to {READER_ROLE}')
        db.execute(sql.SQL('GRANT SELECT ON chunk_rolebased_security.chunks TO {}').format(sql.Identifier(READER_ROLE)))
        print(f'Granted SELECT on chunk_rolebased_security.chunks to {READER_ROLE}')
        db.execute(sql.SQL('GRANT EXECUTE ON FUNCTION chunk_rolebased_security.may_read(text,text) TO {}').format(sql.Identifier(READER_ROLE)))
        print(f'Granted EXECUTE on function chunk_rolebased_security.may_read to {READER_ROLE}')
        # Explicitly prevent reading underlying ACL and identity tables via the restricted login.
        db.execute(sql.SQL('REVOKE ALL ON chunk_rolebased_security.documents, chunk_rolebased_security.document_acl, chunk_rolebased_security.users, chunk_rolebased_security.user_groups FROM {}').format(sql.Identifier(READER_ROLE)))
        print(f'Revoked all privileges on underlying ACL and identity tables from {READER_ROLE}')
        users=json.loads((ROOT/'data/users.json').read_text())
        for u in users:
            db.execute("""INSERT INTO chunk_rolebased_security.users(user_id,display_name,tenant_id)
                          VALUES (%s,%s,%s) ON CONFLICT(user_id) DO UPDATE
                          SET display_name=excluded.display_name,tenant_id=excluded.tenant_id""",
                       (u['user_id'],u['display_name'],TENANT))
            db.execute('DELETE FROM chunk_rolebased_security.user_groups WHERE user_id=%s',(u['user_id'],))
            for group in u['groups']:
                db.execute('INSERT INTO chunk_rolebased_security.user_groups(user_id,group_name) VALUES(%s,%s)',(u['user_id'],group))
                print(f'Added user {u["user_id"]} to group {group}')
            print(f'Processed user {u["user_id"]}')
    print('Next: python ingest.py')

if __name__=='__main__': main()
