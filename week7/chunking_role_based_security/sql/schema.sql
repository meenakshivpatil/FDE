-- Run as database owner / admin, not as rag_reader.
CREATE EXTENSION IF NOT EXISTS vector;
CREATE SCHEMA IF NOT EXISTS chunk_rolebased_security;
REVOKE ALL ON SCHEMA chunk_rolebased_security FROM PUBLIC;

CREATE TABLE IF NOT EXISTS chunk_rolebased_security.users (
    user_id text PRIMARY KEY,
    display_name text NOT NULL,
    tenant_id text NOT NULL
);
CREATE TABLE IF NOT EXISTS chunk_rolebased_security.user_groups (
    user_id text NOT NULL REFERENCES chunk_rolebased_security.users(user_id) ON DELETE CASCADE,
    group_name text NOT NULL,
    PRIMARY KEY (user_id, group_name)
);
CREATE TABLE IF NOT EXISTS chunk_rolebased_security.documents (
    document_id text PRIMARY KEY,
    tenant_id text NOT NULL,
    department text NOT NULL,
    title text NOT NULL,
    visibility text NOT NULL,
    version integer NOT NULL,
    source_path text NOT NULL
);
CREATE TABLE IF NOT EXISTS chunk_rolebased_security.document_acl (
    document_id text NOT NULL REFERENCES chunk_rolebased_security.documents(document_id) ON DELETE CASCADE,
    group_name text NOT NULL,
    PRIMARY KEY (document_id, group_name)
);
CREATE TABLE IF NOT EXISTS chunk_rolebased_security.chunks (
    chunk_id bigserial PRIMARY KEY,
    document_id text NOT NULL REFERENCES chunk_rolebased_security.documents(document_id) ON DELETE CASCADE,
    tenant_id text NOT NULL,
    chunk_no integer NOT NULL,
    chunk_text text NOT NULL,
    embedding vector(384) NOT NULL,
    UNIQUE(document_id, chunk_no)
);
CREATE INDEX IF NOT EXISTS chunks_document_id_idx ON chunk_rolebased_security.chunks(document_id);
CREATE INDEX IF NOT EXISTS documents_tenant_idx ON chunk_rolebased_security.documents(tenant_id);

-- SECURITY DEFINER: permissions checked against ACLs, without granting
-- rag_reader any direct SELECT on the user/group/ACL tables.
CREATE OR REPLACE FUNCTION chunk_rolebased_security.may_read(p_document_id text, p_tenant text)
RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER
SET search_path = pg_catalog, chunk_rolebased_security
AS $$
 SELECT EXISTS (
   SELECT 1 FROM chunk_rolebased_security.documents d
   JOIN chunk_rolebased_security.document_acl a ON a.document_id=d.document_id
   JOIN chunk_rolebased_security.user_groups ug ON ug.group_name=a.group_name
   JOIN chunk_rolebased_security.users u ON u.user_id=ug.user_id
   WHERE d.document_id=p_document_id
     AND d.tenant_id=p_tenant AND u.tenant_id=d.tenant_id
     AND u.user_id=nullif(current_setting('app.user_id', true),'')
     AND d.tenant_id=nullif(current_setting('app.tenant_id',true),'')
 );
$$;
REVOKE ALL ON FUNCTION chunk_rolebased_security.may_read(text,text) FROM PUBLIC;

ALTER TABLE chunk_rolebased_security.chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE chunk_rolebased_security.chunks FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS authorized_chunks ON chunk_rolebased_security.chunks;
CREATE POLICY authorized_chunks ON chunk_rolebased_security.chunks FOR SELECT
USING (
  tenant_id = nullif(current_setting('app.tenant_id',true),'')
  AND chunk_rolebased_security.may_read(document_id,tenant_id)
);
