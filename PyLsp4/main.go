package main

import (
	"PyGoLspTest/lsp"
	"fmt"
	tree_sitter "github.com/tree-sitter/go-tree-sitter"
)

func main() {
	loggerFilePath := "./lsp.log"
	LSP := lsp.NewLsp(loggerFilePath)
	LSP.Logger.Info("PyuGoLSP staring ...")
	LSP.Run()

	LSP.Logger.Info("PyuGoLSP ending ....")
}

// func not_main() {
// python_tree_sitter_path := "/home/plisik/.local/share/nvim/lazy/nvim-treesitter/parser/python.so"
// yaml_tree_sitter_path := "/home/plisik/.local/share/nvim/lazy/nvim-treesitter/parser/yaml.so"
// python := load_language(python_tree_sitter_path)
// yaml:= load_language(yaml_tree_sitter_path)

// code_python, err := os.ReadFile("./test.py")
// if err != nil {
// 	panic(err)
// }
// // code_yaml, err:=os.ReadFile("./configmap.yaml")

// if err != nil {
// 	panic(err)
// }

// parser_python := tree_sitter.NewParser()
// defer parser_python.Close()
// parser_python.SetLanguage(python)

// tree := parser_python.Parse(code_python, nil)
// defer tree.Close()

// res := find_envs_os_environ_bracket(python, code_python, tree.RootNode())
// fmt.Println("OS_ENVS ", res)
// }

func print_tree(node tree_sitter.Node, tree *tree_sitter.TreeCursor, code []byte) {
	start, end := node.ByteRange()
	println(string(code[start:end]))
	println(node.GrammarName())
	println()
	for i, child := range node.NamedChildren(tree) {
		fmt.Println("Print child", i)
		print_tree(child, tree, code)
	}
}
