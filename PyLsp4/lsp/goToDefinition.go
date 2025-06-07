package lsp

import (
	"context"
	"database/sql"
	"fmt"
	"strings"

	"PyGoLspTest/lsp_db"
)

type DefinitionRequest struct {
	Request
	Params DefinitionRequestParams `json:"params"`
}

type DefinitionRequestParams struct {
	Position Position `json:"position"`
	Document Document `json:"textDocument"`
}

type Document struct {
	Uri string `json:"uri"`
}

type Position struct {
	Character int `json:"character"`
	Line      int `json:"line"`
}

type DefinitionResponse struct {
	Response
	Result *LspLocation `json:"result"`
}

// type DefintionResult struct {
// 	location *DefinitionLocation `json:"contents"`
// }

type LspLocation struct {
	Uri   string `json:"uri"`
	Range Range  `json:"range"`
}

type Range struct {
	Start Position `json:"start"`
	End   Position `json:"end"`
}

func uriToFilePath(uri string) string {
	// file:///home/plisik/Proj/PyGoLspTest/test.py -> /home/plisik/Proj/PyGoLspTest/test.py
	after, found := strings.CutPrefix(uri, "file://")
	if found {
		return after
	}
	return ""
}

func pathToUri(path string) string {
	return fmt.Sprintf("file://%s", path)
}

func (server *Server) GoToDefinition(request DefinitionRequest, ctx context.Context) DefinitionResponse {
	// file_path:= uriToFilePath(request.Params.Document.Uri)
	os_name, err := server.Queries.PyEnvByLocation(ctx, lsp_db.PyEnvByLocationParams{
		Path: uriToFilePath(request.Params.Document.Uri),
		PyRow: sql.NullInt64{
			Int64: int64(request.Params.Position.Line),
			Valid: true,
		},
		PyStartColumn: sql.NullInt64{
			Int64: int64(request.Params.Position.Character),
			Valid: true,
		},
		PyEndColumn: sql.NullInt64{
			Int64: int64(request.Params.Position.Character),
			Valid: true,
		},
	})
	if err != nil {
		server.Logger.Error("Error druing PyEnvByLocation query", "err", err)
		return DefinitionResponse{
			Response: Response{RPC: "2.0", ID: &request.ID},
			Result:   nil,
		}
	}
	yaml_env, err := server.Queries.SelectYamlEnvByName(ctx, os_name)
	if err != nil {
		server.Logger.Error("Errod druing SelectYamlEnvByName query", "err", err)
		return DefinitionResponse{
			Response: Response{RPC: "2.0", ID: &request.ID},
			Result:   nil,
		}
	}

	return DefinitionResponse{
		Response: Response{RPC: "2.0", ID: &request.ID},
		Result: &LspLocation{
			Uri: pathToUri(yaml_env.Path),
			Range: Range{
				Start: Position{
					Character: int(yaml_env.YamlStartColumn.Int64),
					Line:      int(yaml_env.YamlRow.Int64),
				},
				End: Position{
					Character: int(yaml_env.YamlEndColumn.Int64),
					Line:      int(yaml_env.YamlRow.Int64),
				},
			},
		},
	}
}
