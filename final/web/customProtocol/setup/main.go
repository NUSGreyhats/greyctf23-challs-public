package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
)

var (
	flag       = os.Getenv("FLAG")
	optCodeMap = map[string]func(map[string]string, string) (string, error){
		"read": func(_ map[string]string, fileName string) (string, error) {
			file, err := os.Open(fileName)
			if err != nil {
				return "", fmt.Errorf(caesarCipher(err.Error(), len(err.Error())))
			}
			defer file.Close()
			result, err := io.ReadAll(file)
			if err != nil {
				return "", err
			}
			return string(result), nil
		},
		"ping": func(_ map[string]string, s string) (string, error) {
			return "pong", nil
		},
		"print": func(m map[string]string, s string) (string, error) {
			if val, ok := m[s]; ok {
				return val, nil
			}
			return s, nil
		},
		"giv3-fl4g-p1s": func(_ map[string]string, _ string) (string, error) {
			return fmt.Sprintf("Good job, you broke the protocol: %s", flag), nil
		},
	}
)

func caesarCipher(text string, shift int) string {
	shift %= 26 // Wrap around the shift value if it exceeds 26
	shiftedText := ""
	for _, char := range text {
		if char >= 'a' && char <= 'z' {
			// Shift lowercase letters
			shiftedChar := 'a' + (char-'a'+rune(shift))%26
			shiftedText += string(shiftedChar)
		} else if char >= 'A' && char <= 'Z' {
			// Shift uppercase letters
			shiftedChar := 'A' + (char-'A'+rune(shift))%26
			shiftedText += string(shiftedChar)
		} else {
			// Keep non-alphabetic characters unchanged
			shiftedText += string(char)
		}
	}
	return shiftedText
}

func ExecuteInstructions(program string) string {
	program = strings.Trim(program, " \n\t")
	instructions := strings.Split(program, " ")
	log.Default().Println("Received: ", instructions)
	if len(instructions)%2 != 0 {
		return "Invalid instructions"
	}
	output := strings.Builder{}
	env := map[string]string{}

	for i := 0; i < len(instructions); i += 2 {
		instruction := instructions[i]
		instruction = caesarCipher(instruction, len(instruction)+i)
		argument := instructions[i+1]
		argument = caesarCipher(argument, len(argument)+i+1)
		cmd, ok := optCodeMap[instruction]
		if !ok {
			output.Write([]byte("Invalid instruction"))
			continue
		}

		result, err := cmd(env, argument)
		if err != nil {
			output.Write([]byte(err.Error()))
		} else {
			output.Write([]byte(result))
		}
		output.Write([]byte("\n"))
	}
	return strings.Replace(output.String(), "_", " ", -1)

}

type Resp struct {
	Code string `json:"code"`
}

func main() {
	if flag == "" {
		flag = "grey{test_flag}"
	}
	// A simple html upload and download server
	// Serve the files in the "static" directory
	fileServer := http.FileServer(http.Dir("static"))
	http.Handle("/", fileServer)

	// Handle file upload and store them in the "uploads" directory
	http.HandleFunc("/execute", func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if r := recover(); r != nil {
				log.Default().Println("Recovered from panic:", r)
				w.WriteHeader(http.StatusInternalServerError)
				w.Write([]byte("Error executing code"))
			}

		}()
		// Check if it is a POST request
		if r.Method != http.MethodPost {
			w.WriteHeader(http.StatusMethodNotAllowed)
			w.Write([]byte("Only POST requests are allowed"))
			return
		}

		// Get the `code` field
		val, err := io.ReadAll(r.Body)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte("Error reading code"))
			return
		}

		resp := Resp{}
		err = json.Unmarshal(val, &resp)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte("Error unmarshalling json"))
			return
		}

		// Execute the instruction
		result := ExecuteInstructions(resp.Code)
		res, err := json.Marshal(map[string]string{"result": result})
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte("Error marshalling json"))
			return
		}

		// Write the result back to the client
		w.Header().Set("Content-Type", "application/json")
		w.Write(res)
	})

	// Start the web server on port 8080
	fmt.Println("Server listening on port 8080...")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Error starting server:", err)
	}
}
