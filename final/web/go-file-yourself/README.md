# Go File Yourself

Inspiration was taken from ACSC challenges easySSTI and 10av

### Challenge Details

I wanted to secure my server against malicious uploads, so I installed and set up ClamAV. Then I remembered that I don't even need file uploads on my webapp.

### Key Concepts

Arb file upload through SSTI, exploitation of shell script through ClamAV trigger

### Solution

`curl -X GET -g 'http://localhost:3000/?name={{$a+:=+.FormFile%20%22lol%22}}{{.SaveUploadedFile+$a+"/uploads/a\n~!%20echo%20<BASE64_COMMAND_HERE>|base64%20-d|bash\na"}}' -F 'lol=@eicar_test_file'`

An instance of [gin.Context](https://github.com/gin-gonic/gin/blob/master/context.go) is passed into template renderer allowing it to call any functions within the Context object. The first part of the challenge involved using the FormFile and SaveUploadedFile functions to obtain a reference to an uploaded form file (given by the user) and writing it to any location on disk, thus forming and arbitrary file write.

The second part of the challenge was intended to have players exploit a flaw in the mailvirus shell script that ClamAV calls when it detects a virus. If ClamAV processes a file with a newline, the environment variable CLAM_VIRUSEVENT_FILENAME will also contain a newline, which in the shell script context will result in multiple lines of input being sent to the mail program. The mail program will interpret lines starting with `~!` as shell commands to execute. Therefore, using the arb file write from above, a user could write a file containing malware (such as the EICAR test string) into /uploads, causing clamAV to process it and injecting a line beginning with `~!` into mail to run any command. (During the actual event, clamav would not execute the shell script for some unknown reason, so points were awarded to any player who could demonstrate the ability to upload a file)

### Flag
`grey{thEr3S_4_l3S50N_HErE_BuT_i_DonT_KN0w_wHAT}`
