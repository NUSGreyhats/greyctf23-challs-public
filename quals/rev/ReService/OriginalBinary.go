package main

import (
	"fmt"
	"hash/crc32"
	"io/ioutil"
	"math/rand"
	"net/http"
	"strings"
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
	// Generate a path from base url
	base_url := "http://34.124.157.94:5010/"
	path := path_generator()
	visit := base_url + path

	// Visit the website using a get request
	resp, err := http.Get(visit)
	if err != nil {
		fmt.Println(err)
	}

	// Get response body
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
	}

	// Convert Body from bytes to string
	str_body := string(body)

	isMatch := strings.Contains(str_body, "grey{")
	if !isMatch {
		fmt.Println("This is not the correct server")
	} else {
		fmt.Println("Communication complete")
	}

}
