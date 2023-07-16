package main

import (
	"html/template"
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		name := c.Query("name")
		tmpl := `<!DOCTYPE html>
		<html lang="en">
		<head>
			<meta charset="UTF-8">
			<title>Document</title>
			</head>
			<body>
				<h1>Hello ` + name + `</h1>
			</body>
		</html>`
		t, err := template.New("tmpl").Parse(tmpl)
		if err != nil {
			c.String(http.StatusBadRequest, err.Error())
			return
		}
		err = t.Execute(c.Writer, c)
		if err != nil {
			c.String(http.StatusBadRequest, err.Error())
			return
		}
	})

	r.GET("/upload", func(c *gin.Context) {
		c.String(http.StatusOK, "This function has been disabled!")
	})

	r.Run(":3000")
}
