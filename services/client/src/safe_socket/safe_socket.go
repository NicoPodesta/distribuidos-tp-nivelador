package safe_socket

import (
	"errors"
	"io"
)

func SendAll(socket io.Writer, bytes []byte) error {
	bytesSent := 0

	for bytesSent < len(bytes) {	
		n, err := socket.Write(bytes[bytesSent:])
		if err != nil {
			return err
		}
		if n == 0 {
			return errors.New("Zero bytes written to socket")
		}
		bytesSent += n
	}
	return nil
}

func RecvAll(socket io.Reader, size int) ([]byte, error) {
	buff := make([]byte, size)
	bytesRead := 0

	for bytesRead < size {	
		n, err := socket.Read(buff[bytesRead:])
		if err != nil {
			return nil, err
		}
		if n == 0 {
			return nil, io.ErrUnexpectedEOF
		}
		bytesRead += n
	}
	return buff, nil
}
