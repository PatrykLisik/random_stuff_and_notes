package lsp

import (
	"context"
	"database/sql"
	"fmt"
	"io/fs"
	"log/slog"
	"os"
	"path"

	"PyGoLspTest/lsp_db"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
)

func TSQueryCode(query string, lang *tree_sitter.Language, code []byte, root_node *tree_sitter.Node, logger *slog.Logger) [][]tree_sitter.Node {
	q, query_error := tree_sitter.NewQuery(lang, query)

	result := make([][]tree_sitter.Node, 0)
	if query_error != nil {
		logger.Error("Query to failed to parse. Returniug empty list", "error", query_error)
		return result
	}
	query_c := tree_sitter.NewQueryCursor()
	m := query_c.Matches(q, root_node, code)
	for {
		cs := m.Next()
		if cs == nil {
			break
		}
		result_line := make([]tree_sitter.Node, len(cs.Captures))
		for i, c := range cs.Captures {
			result_line[i] = c.Node
		}
		result = append(result, result_line)
	}
	return result
}

func codeUnderNode(node *tree_sitter.Node, code []byte) string {
	start, end := node.ByteRange()
	return string(code[start:end])
}

func filesToAnalyze(init_request InitializeRequest) ([]string, []string) {
	pythonFiles := make([]string, 0, 200)
	ymalFiles := make([]string, 0, 200)

	fs.WalkDir(os.DirFS(init_request.Params.RootPath), ".", func(p string, d os.DirEntry, err error) error {
		if d.Type().IsRegular() {
			full_path := path.Join(init_request.Params.RootPath, p)
			extension := path.Ext(full_path)

			if extension == ".py" {
				pythonFiles = append(pythonFiles, full_path)
			}

			if extension == ".yaml" {
				ymalFiles = append(ymalFiles, full_path)
			}
		}
		return nil
	})
	return pythonFiles, ymalFiles
}

func addYamlDocument(server *Server, ctx context.Context, path string) (*lsp_db.Document, error) {
	code_yaml, err := os.ReadFile(path)
	if err != nil {
		server.Logger.Error("Error while reading yaml file", "error", err, "path", path)
		return nil, err
	}

	yaml_tree := server.YamlParser.Parse(code_yaml, nil)

	server.Trees = append(server.Trees, yaml_tree)
	tree_id := len(server.Trees) - 1

	yaml_doc, err := server.Queries.InsertDocument(ctx, lsp_db.InsertDocumentParams{
		Path:   path,
		TreeID: int64(tree_id),
		Code:   string(code_yaml),
	})
	if err != nil {
		server.Logger.Error("Error during insertin document", "err", err, "path", yaml_doc)
		return nil, fmt.Errorf("Error during insertin document")
	}
	return &yaml_doc, nil
}

func upsertYamlEnvsFromDoc(server *Server, ctx context.Context, yamlDoc *lsp_db.Document) {
	yaml_envs := FindEnvsConfigYAML(server.Yaml, []byte(yamlDoc.Code), server.Trees[yamlDoc.TreeID].RootNode(), server.Logger)
	// server.Logger.Info("Envs", "found", yaml_envs)

	err := server.Queries.DeleteYamlEnvByDocID(ctx, sql.NullInt64{
		Int64: yamlDoc.ID,
		Valid: true,
	})
	if err != nil {
		server.Logger.Error("Error duing deleing old ymal envs", "err", err)
	}

	for _, env := range yaml_envs {
		err = server.Queries.InsertYamlEnv(ctx, lsp_db.InsertYamlEnvParams{
			OsName: env.OSName,
			YamlRow: sql.NullInt64{
				Int64: int64(env.OSNameLoc.FileLocation.Row),
				Valid: true,
			},
			YamlStartColumn: sql.NullInt64{
				Int64: int64(env.OSNameLoc.FileLocation.Col),
				Valid: true,
			},
			YamlEndColumn: sql.NullInt64{
				Int64: int64(env.OSNameLoc.FileLocation.Col + uint(len(env.OSName))),
				Valid: true,
			},
			YamlDocumentID: sql.NullInt64{
				Int64: yamlDoc.ID,
				Valid: true,
			},
		})
		if err != nil {
			server.Logger.Error("Error during insertion of yaml env", "err", err)
		}
	}
}

func addPythonDocument(server *Server, ctx context.Context, path string) (*lsp_db.Document, error) {
	code_python, err := os.ReadFile(path)
	if err != nil {
		server.Logger.Error("Error while reading Python file", "error", err, "path", path)
		panic(err)
	}

	tree := server.PythonParser.Parse(code_python, nil)
	server.Trees = append(server.Trees, tree)
	tree_id := len(server.Trees) - 1

	doc, err := server.Queries.InsertDocument(ctx, lsp_db.InsertDocumentParams{
		Path:   path,
		TreeID: int64(tree_id),
		Code:   string(code_python),
	})
	if err != nil {
		server.Logger.Error("error during insertin document", "err", err, "path", path)
		return nil, err
	}
	return &doc, nil
}

func upsertPythonEnvs(server *Server, ctx context.Context, doc *lsp_db.Document) {
	envs := findPythonEnvs(server, []byte(doc.Code), server.Trees[doc.TreeID].RootNode())
	// server.Logger.Info("Python parsed", "Envs", envs, "file_path", doc.Path)

	err := server.Queries.DeletePyEnvByDocID(ctx, sql.NullInt64{
		Int64: doc.ID,
		Valid: true,
	})
	if err != nil {
		server.Logger.Error("Error duing deleing old python evs", "err", err)
	}

	for _, env := range envs {
		err := server.Queries.InsertPyEnv(ctx, lsp_db.InsertPyEnvParams{
			PyName: sql.NullString{
				String: env.PythonName,
				Valid:  true,
			},
			OsName: env.OSName,
			PyRow: sql.NullInt64{
				Int64: int64(env.OSNameLoc.FileLocation.Row),
				Valid: true,
			},
			PyStartColumn: sql.NullInt64{
				Int64: int64(env.OSNameLoc.FileLocation.Col),
				Valid: true,
			},
			PyEndColumn: sql.NullInt64{
				Int64: int64(env.OSNameLoc.FileLocation.Col + uint(len(env.OSName))),
				Valid: true,
			},
			PyDocumentID: sql.NullInt64{
				Int64: int64(doc.ID),
				Valid: true,
			},
		})
		if err != nil {
			server.Logger.Error("Error during  insertion of env", "err", err)
			break
		}
	}
}

func (server *Server) InitialAnalysis(init_request InitializeRequest, ctx context.Context) {
	pythonFiles, ymalFiles := filesToAnalyze(init_request)

	for _, yamlfile := range ymalFiles {
		doc, err := addYamlDocument(server, ctx, yamlfile)
		if err != nil {
			server.Logger.Error("Error adding file", "err", err, "file", yamlfile)
			continue
		}
		upsertYamlEnvsFromDoc(server, ctx, doc)
	}

	for _, file_path := range pythonFiles {
		doc, err := addPythonDocument(server, ctx, file_path)
		if err != nil {
			continue
		}
		upsertPythonEnvs(server, ctx, doc)

	}
}

func findPythonEnvs(server *Server, code []byte, root_node *tree_sitter.Node) []PyEnvVariable {
	new_envs := make([]PyEnvVariable, 0, 100)
	for _, query := range FindPyEnvsQueries {
		env_ := FindPyEnvs(server.Python, code, root_node, query, server.Logger)
		server.Logger.Debug("Env", "envs:", env_, "query", query)
		new_envs = append(new_envs, env_...)
		server.Logger.Debug("FindPythonEnvs new_envs: ", "new_envs", new_envs)
	}
	return new_envs
}

func print_query_result(res [][]tree_sitter.Node, code []byte, logger *slog.Logger) {
	for _, nodes_list := range res {
		for _, node := range nodes_list {
			start, end := node.ByteRange()
			logger.Info(string(code[start:end]))
		}
	}
}
