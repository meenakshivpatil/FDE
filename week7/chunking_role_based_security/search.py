"""Demo-only identity simulation. RLS is applied within PostgreSQL before retrieval."""
import argparse
from common import connect, embed, TENANT
USERS=('priya','arjun','meena','divya')

def run_search(user_id, question, k=5, show=True):
    if user_id.lower() not in USERS: raise ValueError(f'Unknown demo user: {user_id}')
    vector=embed([question])[0]
    with connect() as db:
        with db.transaction():
            db.execute('SELECT set_config(%s,%s,true)',('app.user_id',user_id.lower()))
            db.execute('SELECT set_config(%s,%s,true)',('app.tenant_id',TENANT))
            results=db.execute("""SELECT document_id,chunk_no,left(chunk_text,220),
                                  round((embedding <=> %s::vector)::numeric,4) AS distance
                                  FROM chunk_rolebased_security.chunks
                                  ORDER BY embedding <=> %s::vector LIMIT %s""",
                               (vector,vector,k)).fetchall()
    if show:
        print(f'IDENTITY={user_id.title()} | QUESTION={question!r} | authorized results={len(results)}')
        for doc,no,preview,distance in results:
            print(f'  {doc} / chunk {no} / cosine distance {distance}: {preview[:130]!r}')
        if not results: print('  No authorized matching chunks.')
    return results

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--user', required=True, choices=USERS)
    p.add_argument('--question',required=True)
    p.add_argument('--k',type=int,default=5)
    a=p.parse_args()
    run_search(a.user,a.question,a.k)
