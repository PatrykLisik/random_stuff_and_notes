package lsp

import (
	"log/slog"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
)

type CodeLocation struct {
	Start uint
	End   uint
}

type FileLocation struct {
	Col uint
	Row uint
}

type Location struct {
	CodeLocation CodeLocation
	FileLocation FileLocation
}

type PyEnvVariable struct {
	PythonName    string
	OSName        string
	PythonNameLoc Location
	OSNameLoc     Location
}

type YamlEnvVariable struct {
	OSName    string
	OSNameLoc Location
}

func nodeToLocation(node *tree_sitter.Node) Location {
	return Location{
		CodeLocation{Start: node.Range().StartByte, End: node.Range().EndByte},
		FileLocation{Col: node.EndPosition().Column, Row: node.EndPosition().Row},
	}
}

// os.environ["ENV_1_os"]
const findEnvsPyOsEnvironBracketQuery = `(expression_statement 
    (assignment
      left: (identifier)@py_var 
      right: (subscript 
        value: (attribute 
          object: (identifier)@os_pkg (#eq? @os_pkg "os")
          attribute: (identifier)@environ(#eq? @environ "environ")) 
        subscript: (string  
          (string_start)  
          (string_content)@os_var 
          (string_end)))))`

// environ["ENV_1_os"]
const findEnvPYEnvironBracketQuery = `(expression_statement 
    (assignment 
      left: (identifier)
      right: (subscript
        value: (identifier)@environ(#eq? @environ "environ") 
        subscript: (string 
          (string_start) 
          (string_content)@os_var 
          (string_end)))))`

// environ.get("ENV_2_0")
const findEnvsPyOsEnvironGetQuery = `(expression_statement 
    (assignment 
      left: (identifier) @py_var
      right: (call 
        function: (attribute 
          object: (identifier)@en(#eq? @en "environ") 
          attribute: (identifier)) 
        arguments: (argument_list 
          (string 
            (string_start) 
            (string_content)@os_name 
            (string_end))))))`

// getenv("ENV_6", "value")
// getenv("ENV_6", default="value")
const findEnvsPyGetenvCallQuery = `(expression_statement 
    (assignment 
      left: (identifier) @py_env 
      right: (call 
        function: (identifier) @foo (#eq? @foo "getenv") 
        arguments: (argument_list 
                     .
                     (string 
                       (string_start) 
                       (string_content) @os_name 
                       (string_end)) 
                     ))))`

// ENV_5_0 = os.getenv(default={"k":"v"}, key="ENV_5_0")
// ENV_5_1 = os.getenv("ENV_5_1", default={"k":"v"})
const findEnvsPyGetenvKey = `(expression_statement 
    (assignment 
      left: (identifier) @py_env
      right: (call 
        function: (attribute 
          object: (identifier) @os (#eq? @os "os") 
          attribute: (identifier)@foo (#eq? @foo "getenv"))
        arguments: (argument_list 
          (keyword_argument 
            name: (identifier) @key_name (#eq? @key_name "key") 
            value: (string 
              (string_start)
              (string_content) @os_name 
              (string_end)))))))`

// ENV_2_1 = os.environ.get("ENV_2_1")
const findEnvsPyOsEnvironGet = `(expression_statement 
    (assignment 
      left: (identifier)
      right: (call 
        function: (attribute 
          object: (attribute
            object: (identifier) @os (#eq? @os "os")
            attribute: (identifier))
          attribute: (identifier)@foo_name (#eq? @foo_name "get"))
        arguments: (argument_list
          (string 
            (string_start) 
            (string_content) @py_var
            (string_end))))))`

// ENV_6_1 = os.getenv("ENV_6_1")
// ENV_5_1 = os.getenv("ENV_5_1", default={"k":"v"})
const findEnvsPyGetenvDefault = `(expression_statement 
    (assignment 
      left: (identifier) 
      right: (call 
        function: (attribute 
          object: (identifier)@os (#eq? @os "os") 
          attribute: (identifier)@foo (#eq? @foo "getenv")) 
        arguments: (argument_list 
                     .
          (string 
            (string_start) 
            (string_content) @os_var 
            (string_end)) 
          ))))`

var FindPyEnvsQueries = []string{
	findEnvsPyOsEnvironBracketQuery,
	findEnvPYEnvironBracketQuery,
	findEnvsPyOsEnvironGetQuery,
	findEnvsPyGetenvCallQuery,
	findEnvsPyGetenvKey,
	findEnvsPyOsEnvironGet,
	findEnvsPyGetenvDefault,
}

func FindPyEnvs(lang *tree_sitter.Language, code []byte, root_node *tree_sitter.Node, query string, logger *slog.Logger) []PyEnvVariable {
	query_res := TSQueryCode(query, lang, code, root_node, logger)
	result := make([]PyEnvVariable, len(query_res))
	for i, tokens := range query_res {
		py_var_token := tokens[0]
		env_var_token := tokens[len(tokens)-1]
		py_var := codeUnderNode(&py_var_token, code)
		env_var := codeUnderNode(&env_var_token, code)
		result[i] = PyEnvVariable{
			PythonName: py_var, OSName: env_var,
			PythonNameLoc: nodeToLocation(&py_var_token), OSNameLoc: nodeToLocation(&env_var_token),
		}
	}
	return result
}

const findEnvsConfigYAMLQuery = `(block_mapping_pair
          key: (flow_node 
            (plain_scalar 
              (string_scalar)))@data (#eq? @data "data")
          value: (block_node 
            (block_mapping 
              (block_mapping_pair 
                key: (flow_node 
                  (plain_scalar 
                    (string_scalar)@var_name))
                value: (flow_node 
                  (double_quote_scalar))) 
              )))`

func FindEnvsConfigYAML(lang *tree_sitter.Language, code []byte, root_node *tree_sitter.Node, logger *slog.Logger) []YamlEnvVariable {
	query_res := TSQueryCode(findEnvsConfigYAMLQuery, lang, code, root_node, logger)
	result := make([]YamlEnvVariable, len(query_res))
	for i, tokens := range query_res {
		env_var_token := tokens[1]
		name := codeUnderNode(&env_var_token, code)
		result[i] = YamlEnvVariable{
			OSName:    name,
			OSNameLoc: nodeToLocation(&env_var_token),
		}
	}
	return result
}
