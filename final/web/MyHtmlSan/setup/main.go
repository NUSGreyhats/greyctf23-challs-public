package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"path"
	"regexp"
	"time"

	"github.com/go-rod/rod"
	"github.com/go-rod/rod/lib/launcher"
	"github.com/go-rod/rod/lib/proto"
	"github.com/google/uuid"
)

var (
	tagRegex     = regexp.MustCompile("<(?:\"[^\"]*\"['\"]*|'[^']*'['\"]*|[^'\">])+>")
	commentRegex = regexp.MustCompile("<!--(?:[^-]+|-(?:[^-]+|-[^->]))*-->")
)

func sanitizeHTML(html string) string {

	// Replace HTML tags and comments with empty strings
	sanitizedHTML := tagRegex.ReplaceAllString(html, "")
	sanitizedHTML = commentRegex.ReplaceAllString(sanitizedHTML, "")

	return sanitizedHTML
}

func wrapHtml(html, uuidStr string) string {
	return fmt.Sprintf(`<!DOCTYPE html>
<html>
  <head>
    <title>Html Hosting Service</title>
    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
    />
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <a class="navbar-brand" href="#">Html Hosting Service</a>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item active">
            <a class="nav-link" href="#">Home</a>
          </li>
        </ul>
      </div>
    </nav>
	This is your input: <p>%s</p>

	<!-- Report to admin button -->
	<form action="/report" method="POST">
		<input type="hidden" name="url" value="/uploads/%s.html" />
		<input type="submit" class="btn btn-primary" value="Report to admin" />
	</form>
	<hr class="my-4" />

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  </body>
</html>`, html, uuidStr)
}

func adminVisit(url string) {
	ctrlUrl := launcher.New().MustLaunch()
	log.Default().Println("Visiting:", url)
	browser := rod.New().ControlURL(ctrlUrl).MustConnect()
	defer browser.Close()
	err := browser.MustSetCookies().MustPage(url).MustSetCookies(&proto.NetworkCookieParam{
		Name:     "session",
		Value:    os.Getenv("FLAG"),
		Domain:   "35.187.245.7:32004",
		HTTPOnly: false,
		Expires:  proto.TimeSinceEpoch(time.Now().Add(180 * 24 * time.Hour).Unix()),
	}).MustWaitLoad().WaitStable(time.Minute, 1)

	if err != nil {
		log.Default().Println("Error visiting:", err.Error())
	} else {
		log.Default().Println("Done visiting:", url)
	}
}

func main() {
	// A simple html upload and download server
	// Create a file server that serves static files from the "static" directory
	fileServer := http.FileServer(http.Dir("./static"))

	// Register the file server to handle requests for static files
	http.Handle("/", fileServer)

	// Handle file upload and store them in the "uploads" directory
	http.HandleFunc("/upload", func(w http.ResponseWriter, r *http.Request) {
		// Reject none PATCH requests
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		// Get message attr from form
		if err := r.ParseForm(); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		msg := r.Form.Get("message")

		// Store in a file with a random UUID
		uuidStr := uuid.New().String()
		fileName := fmt.Sprintf("./static/uploads/%s.html", uuidStr)
		log.Default().Println("Writing to file:", fileName)

		// Sanitize the HTML
		sanitizedHTML := sanitizeHTML(msg)
		finalHtml := wrapHtml(sanitizedHTML, uuidStr)

		// Read only access to the file
		err := os.WriteFile(fileName, []byte(finalHtml), 0444)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		// Redirect client to UUID website
		http.Redirect(
			w,
			r,
			path.Clean(
				fmt.Sprintf("/uploads/%s.html", uuidStr),
			),
			http.StatusFound,
		)
	})

	// Handle post request to /report
	http.HandleFunc("/report", func(w http.ResponseWriter, r *http.Request) {
		// Reject none POST requests
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		// Get message attr from form
		if err := r.ParseForm(); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		url := r.Form.Get("url")

		// Get currently hosted address
		hostedAddress := fmt.Sprintf("http://%s", r.Host)

		// Visit the url
		go adminVisit(fmt.Sprintf("%s/%s", hostedAddress, url))

		// Return success
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("<html>Success <a href='/'>Go back</a></html>"))
	})

	// Start the web server on port 8080
	fmt.Println("Server listening on port 8080...")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Error starting server:", err)
	}
}
