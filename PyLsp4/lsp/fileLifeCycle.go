package lsp

type DidOpenTextDocumentParams struct{
	 TextDocument TextDocumentItem `json:"textDocument"`
}

type TextDocumentItem struct {
	Uri string `json:"uri"`

	LanguageId string `json:"languageId"`

	/**
	 * The version number of this document (it will increase after each
	 * change, including undo/redo).
	 */
	 Version int `json:"version"`

	/**
	 * The content of the opened text document.
	 */
	 Text string `json:"text"`
}
