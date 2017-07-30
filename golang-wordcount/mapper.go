package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		terms := strings.Split(line, " ")
		for _, term := range terms {
			out := fmt.Sprintf("%s\t1", term)
			fmt.Println(out)
		}
	}
}
