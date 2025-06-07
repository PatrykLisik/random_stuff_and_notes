CREATE TABLE IF NOT EXISTS  Document (
			id INTEGER PRIMARY KEY AUTOINCREMENT ,
			path TEXT NOT NULL,
			tree_id Int NOT NULL,
			code TEXT NOT NULL
		);

CREATE TABLE IF NOT EXISTS  PyEnv (
			id INTEGER PRIMARY KEY AUTOINCREMENT,

			os_name TEXT UNIQUE NOT NULL,
			py_name TEXT DEFAULT NULL,
			py_row INT DEFAULT NULL,
			py_start_column INT,
			py_end_column INT,
			py_document_id INT,

			FOREIGN KEY(py_document_id) REFERENCES Document(id)
		);

CREATE TABLE IF NOT EXISTS  YamlEnv (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			os_name TEXT UNIQUE NOT NULL,
			yaml_row INT,
			yaml_start_column INT,
			yaml_end_column INT,
			yaml_document_id INT,

			FOREIGN KEY(yaml_document_id) REFERENCES Document(id) 
		);
