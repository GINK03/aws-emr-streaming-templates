package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	dic := map[string]int{}
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		ents := strings.Split(line, "\t")
		term := ents[0]
		_ = ents[1]

		_, ok := dic[term]
		if ok == false {
			dic[term] = 0
		}
		dic[term] += 1
	}

	for term, freq := range dic {
		out := fmt.Sprintf("%s %d", term, freq)
		fmt.Println(out)
	}
}
