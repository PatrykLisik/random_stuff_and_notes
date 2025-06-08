package lsp

import (
	"context"
	"fmt"
	"path"
	"strings"

	"PyGoLspTest/lsp_db"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
)

type DidChangeRequest struct {
	Request
	Params DidChangeRequestParams `json:"params"`
}

type DidChangeRequestParams struct {
	TextDocument   Document         `json:"textDocument"`
	ContentChanges []ContentChanges `json:"contentChanges"`
}

type ContentChanges struct {
	Range       Range  `json:"range"`
	Text        string `json:"text"`
	RangeLength int    `json:"rangeLength"`
}

type DidChangeDocument struct {
	Version int    `json:"version"`
	URI     string `json:"uri"`
}

func findIndexNthLine(blob string, line_number int) (int, error) {
	current_line := 0
	for i := range blob {
		if blob[i] == byte('\n') {
			current_line += 1
			if current_line == line_number {
				return i, nil
			}
		}
	}
	return 0, fmt.Errorf("Not enough lines in blob")
}

func (server *Server) updateDocument(request DidChangeRequest, ctx context.Context) error {
	doc, err := server.Queries.GetDocumentByPath(ctx, uriToFilePath(request.Params.TextDocument.Uri))
	if err != nil {
		server.Logger.Error("Error during retriving document", "err", err)
	}
	new_code := doc.Code
	tree := server.Trees[doc.TreeID]

	extension := path.Ext(doc.Path)

	for _, change := range request.Params.ContentChanges {
		index_of_start_line, err := findIndexNthLine(new_code, change.Range.Start.Line)
		if err != nil {
			server.Logger.Error("Cannot find line in document", "path", doc.Path, "line", change.Range.Start.Line, "document", doc.Code)
			return fmt.Errorf("Cannot find line in document %s", doc.Path)
		}

		index_of_end_line, err := findIndexNthLine(new_code, change.Range.End.Line)
		if err != nil {
			server.Logger.Error("Cannot find line in document", "path", doc.Path, "line", change.Range.Start.Line, "document", doc.Code)
			return fmt.Errorf("Cannot find line in document %s", doc.Path)
		}

		start_change_index := index_of_start_line + change.Range.Start.Character + 1
		end_change_index := index_of_end_line + change.Range.End.Character + 1
		new_code = new_code[:start_change_index] + change.Text + new_code[end_change_index:]

		replacment_line_count := strings.Count(change.Text, "\n")

		var newEndColumn int
		if replacment_line_count > 0 {
			//cant fail. Lines are counted in replacment_line_count
			last_line_break_index, _ := findIndexNthLine(change.Text, replacment_line_count)
			newEndColumn = len(change.Text) - last_line_break_index
		} else {
			newEndColumn = change.Range.Start.Character + len(change.Text)
		}

		tree.Edit(&tree_sitter.InputEdit{
			StartByte:  uint(start_change_index),
			OldEndByte: uint(end_change_index),
			NewEndByte: uint(start_change_index + len(change.Text)),
			StartPosition: tree_sitter.Point{
				Row:    uint(change.Range.Start.Character),
				Column: uint(change.Range.Start.Line),
			},
			OldEndPosition: tree_sitter.Point{
				Row:    uint(change.Range.End.Character),
				Column: uint(change.Range.End.Line),
			},
			NewEndPosition: tree_sitter.Point{
				Row:    uint(start_change_index + replacment_line_count),
				Column: uint(newEndColumn),
			},
		})

		if extension == ".py" {
			tree = server.PythonParser.Parse([]byte(new_code), tree)
		}

		if extension == ".yaml" {
			tree = server.YamlParser.Parse([]byte(new_code), tree)
		}
	}

	server.Trees[doc.TreeID] = tree

	server.Queries.UpdateDocumentCode(ctx, lsp_db.UpdateDocumentCodeParams{
		Code: new_code,
		ID:   doc.ID,
	})

	doc.Code = new_code

	if extension == ".py" {
		upsertPythonEnvs(server, ctx, &doc)
	}

	if extension == ".yaml" {
		upsertYamlEnvsFromDoc(server, ctx, &doc)
	}

	return nil
}
