-- name: InsertDocument :one
INSERT INTO Document(path, tree_id, code) VALUES(?, ?, ?) RETURNING *;

-- name: GetDocumentByPath :one
SELECT * FROM Document WHERE path=?;

-- name: UpdateDocumentCode :exec
UPDATE document SET code=? WHERE id=?;

-- name: InsertPyEnv :exec
INSERT INTO PyEnv(py_name, os_name,py_row, py_start_column, py_end_column, py_document_id) VALUES(?,?,?,?,?,?);

-- name: DeletePyEnvByDocID :exec
DELETE FROM PyEnv WHERE py_document_id=?;

-- name: DeleteYamlEnvByDocID :exec
DELETE FROM YamlEnv WHERE yaml_document_id=?;

-- name: InsertYamlEnv :exec
INSERT INTO YamlEnv( os_name,yaml_row, yaml_start_column, yaml_end_column, yaml_document_id) VALUES(?,?,?,?,?);
			
-- name: SelectYamlEnvByName :one
SELECT yaml_row, yaml_start_column, yaml_end_column, Document.path  FROM YamlEnv 
JOIN Document ON Document.id=yaml_document_id 
WHERE os_name=?;

-- name: PyEnvByLocation :one
SELECT os_name FROM PyEnv 
JOIN Document ON Document.id=PyEnv.py_document_id  
WHERE Document.path=? 
AND PyEnv.py_start_column>=? 
AND PyEnv.py_end_column>=? 
AND PyEnv.py_row=?;
