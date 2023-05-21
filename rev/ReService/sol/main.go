package main

import (
	"fmt"
	"hash/crc32"
	"log"
	"math/rand"
	"net/http"
	"time"
)

var BASE_URL = "http://34.124.157.94:5010/"

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
	path := path_generator()
	url := BASE_URL + path
	fmt.Println(url)

	// Make a get request to the url
	resp, err := http.Get(url)
	if err != nil {
		log.Fatal(err)
		return
	}

	// Read the response
	buf := make([]byte, 1024)
	resp.Body.Read(buf)

	// Convert to string
	payload := string(buf)
	fmt.Printf("Successfully received payload.\nFlag: %s\n", payload)
}
