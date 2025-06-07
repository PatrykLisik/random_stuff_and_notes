package lsp

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"strconv"
)

func Split(data []byte, _ bool) (advance int, token []byte, err error) {
	header, content, found := bytes.Cut(data, []byte{'\r', '\n', '\r', '\n'})
	if !found {
		return 0, nil, nil
	}

	// Content-Length: <number>
	contentLengthBytes := header[len("Content-Length: "):]
	contentLength, err := strconv.Atoi(string(contentLengthBytes))
	if err != nil {
		return 0, nil, err
	}

	if len(content) < contentLength {
		return 0, nil, nil
	}

	totalLength := len(header) + 4 + contentLength
	return totalLength, data[:totalLength], nil
}

func EncodeMessage(msg any) string {
	content, err := json.Marshal(msg)
	if err != nil {
		panic(err)
	}

	return fmt.Sprintf(
		"Content-Length: %d \r\n\r\n%s",
		len(content),
		string(content),
	)
}

type BaseMessage struct {
	Method string `json:"method"`
}

func DecodeMessage(msg []byte) (string, []byte, error) {
	header, content, found := bytes.Cut(msg, []byte{'\r', '\n', '\r', '\n'})
	if !found {
		return "", nil, errors.New("Decoding failed separator not found")
	}

	content_len_byte := header[len("Content-Length: "):]
	content_length, err := strconv.Atoi(string(content_len_byte))
	if err != nil {
		return "", nil, fmt.Errorf("Unable to parse content length bytes %b", content_len_byte)
	}
	var base_message BaseMessage
	err = json.Unmarshal(content[:content_length], &base_message)
	if err != nil {
		return "", nil, errors.New(fmt.Sprintf("Content length %d, actual %d  Unable to parse content  %s",content_length, len(content), string(content[:content_length])))
	}
	return base_message.Method, content[:content_length], nil
}
