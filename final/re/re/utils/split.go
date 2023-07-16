package utils

import "math"

func SplitStringIntoParts(str string, x int) []string {
	// Calculate the length of each part
	partLength := int(math.Ceil(float64(len(str)) / float64(x)))

	// Split the string into x parts
	parts := make([]string, x)
	for i := 0; i < x; i++ {
		start := i * partLength
		end := int(math.Min(float64(start+partLength), float64(len(str))))
		if start > end {
			break
		}
		parts[i] = str[start:end]
	}

	return parts
}
