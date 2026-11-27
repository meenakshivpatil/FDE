"""Shared configuration, database connections, embeddings, and section chunking."""
from functools import lru_cache
import os
from dotenv import load_dotenv
from psycopg import connect as pg_connect
from psycopg.conninfo import conninfo_to_dict, make_conninfo
from pgvector.psycopg import register_vector

load_dotenv()
TENANT = 'DEMO'
MODEL = os.getenv('EMBED_MODEL', 'BAAI/bge-small-en-v1.5')
DBNAME = os.getenv('DATABASE_NAME', 'chunk_rolebased_security')
SERVER_URL = os.environ.get('POSTGRES_SERVER_URL', '')
READER_ROLE = os.environ.get('READER_ROLE', 'security_lab_reader')
READER_PASSWORD = os.environ.get('READER_PASSWORD', '')

def connection_string(*, admin=False, server=False):
    if not SERVER_URL: raise RuntimeError('Set POSTGRES_SERVER_URL in .env')
    settings = conninfo_to_dict(SERVER_URL)
    if not server: settings['dbname'] = DBNAME
    if not admin and not server:
        settings['user'] = READER_ROLE
        settings['password'] = READER_PASSWORD
    return make_conninfo(**settings)

def connect(*, admin=False, server=False, autocommit=False, register=True):
    db = pg_connect(connection_string(admin=admin, server=server), autocommit=autocommit)
    if not server and register: register_vector(db)
    return db

@lru_cache(maxsize=1)
def get_model():
    from fastembed import TextEmbedding
    print(f'Loading local embedding model: {MODEL} (first run downloads weights)')
    return TextEmbedding(model_name=MODEL)

def embed(texts):
    vectors=[v.tolist() for v in get_model().embed(texts, batch_size=32)]
    if any(len(v)!=384 for v in vectors):
        raise RuntimeError('Expected BGE-small 384-dimensional embeddings')
    return vectors

def chunk_by_section(markdown, max_chars=1000):
    paras=[p.strip() for p in markdown.split('\n\n') if p.strip()]
    out=[]; block=''
    for p in paras:
        if len(p)>max_chars:
            if block: out.append(block); block=''
            out.extend(p[i:i+max_chars] for i in range(0,len(p),max_chars))
        elif not block: block=p
        elif len(block)+len(p)+2<=max_chars: block+='\n\n'+p
        else: out.append(block); block=p
    if block: out.append(block)
    return out
