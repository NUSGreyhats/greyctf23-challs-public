package main

import (
	"fmt"
	"hash/crc32"
	"log"
	"math/rand"
	"net/http"
	"os"
	"time"
)

func path_generator() string {

	// Generates a random string with time as seed
	now := time.Now()
	sec := now.Unix()

	// Shift slightly
	sec >>= 4

	// Use time as seed
	rand.Seed(sec)
	// Generate random hex string and pass it into crc32
	crc_val := crc32.ChecksumIEEE([]byte(fmt.Sprintf("%x", rand.Int())))

	return fmt.Sprintf("%x", crc_val)
}

func main() {
	port := 8080

	// Get flag from environment variable
	FLAG := os.Getenv("FLAG")
	if FLAG == "" {
		FLAG = "greyctf{fake_flag}"
	}

	// Handle dynamic path
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Retrieve path after '/'
		path := r.URL.Path[1:]
		if path == "" {
			// Return hello world response
			w.Write([]byte("Hello! Have you reversed the binary yet? If not, go ahead and do it! If you have, then you should know what to do next! Good luck!"))
			return
		}

		// Check if the path is correct
		if path != path_generator() {
			// Return wrong path
			w.Write([]byte("Ah man, you got the wrong path!"))
			return
		}

		// Return flag
		w.Write([]byte(FLAG))
		return
	})

	fmt.Printf("Server is starting at port %d\n", port)
	if err := http.ListenAndServe(fmt.Sprintf(":%d", port), nil); err != nil {
		log.Fatal(err)
	}
}
