"""Ingest the 30 supplied synthetic documents and store their ACLs and vectors."""
from pathlib import Path
import json, time
from common import connect, embed, chunk_by_section
ROOT=Path(__file__).resolve().parent

def main():
    docs=[json.loads(line) for line in (ROOT/'data/kube_documents.jsonl').read_text().splitlines() if line.strip()]
    if len(docs)!=30: raise ValueError(f'Expected exactly 30 documents; found {len(docs)}')
    chunks=[(d['document_id'],d['tenant_id'],i,text)
            for d in docs for i,text in enumerate(chunk_by_section(d['content']))]
    print(f'Preparing {len(docs)} documents and {len(chunks)} chunks')
    started=time.monotonic(); vectors=[]
    for i in range(0,len(chunks),32):
        vectors.extend(embed([c[3] for c in chunks[i:i+32]]))
        print(f'Embedded {len(vectors)}/{len(chunks)} chunks')
    with connect(admin=True) as db:
        with db.transaction():
            for d in docs:
                db.execute("""INSERT INTO chunk_rolebased_security.documents
                     (document_id,tenant_id,department,title,visibility,version,source_path)
                     VALUES(%s,%s,%s,%s,%s,%s,%s)
                     ON CONFLICT(document_id) DO UPDATE SET
                     tenant_id=excluded.tenant_id,department=excluded.department,
                     title=excluded.title,visibility=excluded.visibility,
                     version=excluded.version,source_path=excluded.source_path""",
                     tuple(d[k] for k in ('document_id','tenant_id','department','title','visibility','version','source_path')))
                db.execute('DELETE FROM chunk_rolebased_security.document_acl WHERE document_id=%s',(d['document_id'],))
                for group in d['permitted_groups']:
                    db.execute('INSERT INTO chunk_rolebased_security.document_acl(document_id,group_name) VALUES(%s,%s)',(d['document_id'],group))
                db.execute('DELETE FROM chunk_rolebased_security.chunks WHERE document_id=%s',(d['document_id'],))
            with db.cursor() as cur:
                cur.executemany("""INSERT INTO chunk_rolebased_security.chunks(document_id,tenant_id,chunk_no,chunk_text,embedding)
                                   VALUES (%s,%s,%s,%s,%s)""",
                                [(c[0],c[1],c[2],c[3],v) for c,v in zip(chunks,vectors)])
    print(f'Finished: {len(docs)} docs, {len(chunks)} chunks in {time.monotonic()-started:.1f}s')
    print('Next: python search.py --user priya --question "employee onboarding checklist"')

if __name__=='__main__': main()
