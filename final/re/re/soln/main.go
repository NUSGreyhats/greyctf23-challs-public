package Soln

import (
	"encoding/base64"
	"fmt"
	"log"
	"math"
	"math/bits"
	"math/rand"
	"strings"
)

type OrderedString struct {
	Str   string `json:"str" bson:"str"`
	Index int    `json:"index" bson:"index"`
}

type Routine func(string) string

func RoutineGenerator(f Routine, name string) Routine {
	return func(s string) string {
		logger := log.Default()
		logger.Printf("[%s]", name)
		return f(s)
	}
}

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

func GetRandFromSeed(seed int64) *rand.Rand {
	return rand.New(rand.NewSource(seed))
}
func GenerateArr(n int) []int {
	arr := make([]int, n)
	for i := 0; i < n; i++ {
		arr[i] = i
	}
	return arr
}

var (
	// Rotate the string by n bits.
	CounterRotate = RoutineGenerator(func(s string) string {
		if len(s) <= 1 {
			return s
		}
		rand := GetRandFromSeed(int64(len(s)))

		// Rotate the string by n bits
		n := len(s) - (rand.Intn(256) % len(s))
		return s[n:] + s[:n]
	}, "rotate")

	Sub = RoutineGenerator(func(s string) string {
		rand := GetRandFromSeed(int64(len(s)))
		// Add n bits to each rune
		acc := strings.Builder{}
		for i := 0; i < len(s); i++ {
			var diffuse uint
			if i == 0 {
				diffuse = 0
			} else {
				diffuse = uint(acc.String()[i-1])
			}
			n := rand.Uint32() % 256
			b := (uint(s[i]) - uint(n) - diffuse) % 256
			acc.Write([]byte{byte(b)})
		}
		return acc.String()
	}, "Sub")

	UnShuffle = RoutineGenerator(func(s string) string {
		rand := GetRandFromSeed(int64(len(s)))
		arr := GenerateArr(len(s))
		bArr := []byte(s)
		rand.Shuffle(len(arr), func(i, j int) {
			arr[i], arr[j] = arr[j], arr[i]
		})
		acc := make([]byte, len(s))
		for i := 0; i < len(arr); i++ {
			finalIdx := arr[i]
			acc[finalIdx] = bArr[i]
		}
		return string(acc)
	}, "UnShuffle")

	// Xor each rune with n.
	UnXor = RoutineGenerator(func(s string) string {
		rand := GetRandFromSeed(int64(len(s)))
		// Xor each rune with n
		acc := strings.Builder{}
		for i := 0; i < len(s); i++ {
			var diffuse uint
			if i == 0 {
				diffuse = 0
			} else {
				diffuse = uint(acc.String()[i-1])
			}
			b := s[i] ^ byte(rand.Intn(256)) ^ byte(diffuse)
			acc.Write([]byte{b})
		}
		return acc.String()
	}, "unXor")

	ReverseBits = RoutineGenerator(func(s string) string {
		// Reverse bits
		acc := strings.Builder{}
		for i := 0; i < len(s); i++ {
			acc.Write([]byte{bits.Reverse8(byte(uint8(s[i])))})
		}
		return acc.String()
	}, "ReverseBits")

	DncFunctions = []Routine{
		Sub,
		CounterRotate,
		UnXor,
		ReverseBits,
		UnShuffle,
	}
	LayerArr = []int{1, 2, 4, 8, 16, 32, 16, 8, 4, 2, 1}
)

func Decrypt(final string) string {
	dec, err := base64.URLEncoding.DecodeString(final)
	if err != nil {
		panic(err)
	}

	noLayers := len(LayerArr)
	layers := make([][]Routine, noLayers)

	for i := 0; i < noLayers; i++ {
		layerSize := LayerArr[i]
		arr := make([]Routine, layerSize)
		for j := 0; j < layerSize; j++ {
			arr[j] = DncFunctions[j%len(DncFunctions)]
		}
		layers[i] = arr
	}

	acc := string(dec)
	for i := noLayers - 1; i >= 0; i-- {
		tmp := strings.Builder{}
		currLayer := layers[i]
		layerSize := len(currLayer)
		parts := SplitStringIntoParts(acc, layerSize)

		// For each part apply function in layer
		recvChan := make(chan OrderedString, layerSize)
		for j := layerSize - 1; j >= 0; j-- {
			part := parts[j]
			f := currLayer[j]

			go func(recvChan chan OrderedString, i int) {
				res := f(part)
				recvChan <- OrderedString{Str: res, Index: i}
			}(recvChan, j)
		}

		tmpAcc := make([]string, layerSize)
		for j := 0; j < layerSize; j++ {
			res := <-recvChan
			tmpAcc[res.Index] = res.Str
		}

		// Join parts
		for j := 0; j < layerSize; j++ {
			tmp.WriteString(tmpAcc[j])
		}
		acc = tmp.String()
		fmt.Println(len(acc))
	}

	// Combine into a string
	return acc
}
