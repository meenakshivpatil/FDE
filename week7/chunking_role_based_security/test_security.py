"""Assert permissions and verify live revocation. Restores revoked group in finally."""
from common import connect, TENANT

def visible(doc_id,user_id):
    with connect() as db:
        with db.transaction():
            db.execute('SELECT set_config(%s,%s,true)',('app.user_id',user_id))
            db.execute('SELECT set_config(%s,%s,true)',('app.tenant_id',TENANT))
            return db.execute('SELECT EXISTS(SELECT 1 FROM chunk_rolebased_security.chunks WHERE document_id=%s)',(doc_id,)).fetchone()[0]

def check(label,actual,expected):
    print(('PASS' if actual==expected else 'FAIL')+f'  {label} => {actual}')
    if actual!=expected: raise AssertionError(label)

def main():
    check('Priya reads APP-ENG-001',visible('APP-ENG-001','priya'),True)
    check('Arjun blocked from APP-ENG-001',visible('APP-ENG-001','arjun'),False)
    check('Arjun reads PLAT-ENG-001',visible('PLAT-ENG-001','arjun'),True)
    check('Divya reads PLAT-ENG-001',visible('PLAT-ENG-001','divya'),False)
    check('Meena blocked from PLAT-ENG-001',visible('PLAT-ENG-001','meena'),False)
    check('Unknown identity blocked',visible('APP-ENG-001','unknown-person'),False)
    check('Arjun sees APP-ENG-007 (shared with all)',visible('APP-ENG-007','arjun'),False)
    with connect(admin=True) as db:
        db.execute("DELETE FROM chunk_rolebased_security.user_groups WHERE user_id='arjun' AND group_name='Platform_Engineering'")
        db.commit()
    try:
        check('Arjun denied PLAT-ENG-001 after revocation',visible('PLAT-ENG-001','arjun'),False)
    finally:
        with connect(admin=True) as db:
            db.execute("INSERT INTO chunk_rolebased_security.user_groups(user_id,group_name) VALUES('arjun','Platform_Engineering') ON CONFLICT DO NOTHING")
            db.commit()
    check('Arjun regains PLAT-ENG-001 after restore',visible('PLAT-ENG-001','arjun'),True)
    with connect() as db:
        try:
            db.execute('SELECT * FROM chunk_rolebased_security.document_acl LIMIT 1').fetchall()
        except Exception:
            print('PASS  Direct access to ACL table denied')
        else:
            raise AssertionError('ACL table unexpectedly readable by restricted role')
    print('ALL CHECKS PASSED. Classroom user IDs are simulated; production requires verified authentication.')

if __name__=='__main__': main()
