package lsp

import (
	"bufio"
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"log/slog"
	"os"
	"unsafe"

	"PyGoLspTest/lsp_db"

	_ "github.com/mattn/go-sqlite3"

	"github.com/ebitengine/purego"
	tree_sitter "github.com/tree-sitter/go-tree-sitter"
)

type Server struct {
	Logger       *slog.Logger
	Python       *tree_sitter.Language
	Yaml         *tree_sitter.Language
	PythonParser *tree_sitter.Parser
	YamlParser   *tree_sitter.Parser
	Queries      *lsp_db.Queries
	Trees        []*tree_sitter.Tree
}

func loadLanguage(path string, lib_name string, logger *slog.Logger) *tree_sitter.Language {
	lib, err := purego.Dlopen(path, purego.RTLD_NOW|purego.RTLD_GLOBAL)
	if err != nil {
		panic(1)
	} else {
		logger.Info("Treesitter parser found", "path", path)
	}

	var lang_ptr func() uintptr
	purego.RegisterLibFunc(&lang_ptr, lib, lib_name)

	lang := tree_sitter.NewLanguage(unsafe.Pointer(lang_ptr()))

	return lang
}

func runSchemaFile(db *sql.DB) error {
	file, err := os.ReadFile("./schema.sql")
	if err != nil {
		return err
	}
	_, err = db.Exec(string(file))
	return err
}

func NewLsp(logFilePath string) Server {
	// Logger
	logFile, err := os.OpenFile(logFilePath, os.O_CREATE|os.O_TRUNC|os.O_WRONLY, 0o666)
	if err != nil {
		panic("Cannot open the logging file")
	}
	hanndler := slog.NewTextHandler(logFile, &slog.HandlerOptions{
		Level: slog.LevelDebug,
	})
	logger := slog.New(hanndler)

	//  Treesitters
	python_tree_sitter_path := "/home/plisik/.local/share/nvim/lazy/nvim-treesitter/parser/python.so"
	yaml_tree_sitter_path := "/home/plisik/.local/share/nvim/lazy/nvim-treesitter/parser/yaml.so"
	python := loadLanguage(python_tree_sitter_path, "tree_sitter_python", logger)
	yaml := loadLanguage(yaml_tree_sitter_path, "tree_sitter_yaml", logger)

	parser_python := tree_sitter.NewParser()
	parser_python.SetLanguage(python)

	parser_yaml := tree_sitter.NewParser()
	parser_yaml.SetLanguage(yaml)

	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		logger.Error("Error during DB connection", "err", err)
		panic(1)
	}

	err = runSchemaFile(db)
	if err != nil {
		logger.Error("Error during DB schema creation", "err", err)
		panic(1)
	}

	trees:= make([]*tree_sitter.Tree, 0, 50)

	return Server{Logger: logger, Python: python, Yaml: yaml, PythonParser: parser_python, YamlParser: parser_yaml, Queries: lsp_db.New(db), Trees: trees}
}

func (server *Server) handleMessage(method string, msg []byte, ctx context.Context) (any, error) {
	switch method {
	case "initialize":
		var request InitializeRequest
		err := json.Unmarshal(msg, &request)
		if err != nil {
			server.Logger.Error("Cannon parse initialize content", "error", err)
			return nil, err
		}
		server.Logger.Info("Connected to", request.Params.ClientInfo.Name, request.Params.ClientInfo.Version, "Root", request.Params.RootPath)
		server.InitialAnalysis(request, ctx)
		response := NewInitializeResponse(1)
		return response, nil

	case "initialized":
		return nil, nil
	case "textDocument/didOpen":
		break
	case "textDocument/didChange":
		var request DidChangeRequest
		err := json.Unmarshal(msg, &request)
		if err != nil {
			server.Logger.Error("Cannon parse textDocument/didChange", "error", err)
			return nil, err
		}
		server.Logger.Info("Did change", "request", request)
		return nil, server.updateDocument(request, ctx)
	case "textDocument/definition":
		var request DefinitionRequest
		err := json.Unmarshal(msg, &request)
		if err != nil {
			server.Logger.Error("Cannon parse go to definition content", "error", err)
			return nil, err
		}
		return server.GoToDefinition(request, ctx), nil
	}
	return nil, fmt.Errorf("Cannot handle method %s", method)
}

func (server *Server) Run() {

	ctx:= context.Background()
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Split(Split)
	for scanner.Scan() {
		msg := scanner.Bytes()
		server.Logger.Info("New message", "body", (string(msg)))

		method, content, err := DecodeMessage(msg)
		if err != nil {
			server.Logger.Error("Cannot decode message", err)
			continue
		}

		server.Logger.Info("Received message", "method", method)
		response, err := server.handleMessage(method, content, ctx)
		if err != nil {
			server.Logger.Error(err.Error())
			continue
		}

		if response != nil {
			encoded := EncodeMessage(response)

			server.Logger.Info("Response sent", "body", encoded)
			os.Stdout.Write([]byte(encoded))
		}
	}
}
