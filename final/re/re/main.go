package main

import (
	"encoding/base64"
	"fmt"
	"os"
	"strings"

	"Re/common"
	"Re/subroutine"
	"Re/utils"
)

var (
	EncFunctions = []subroutine.Routine{
		subroutine.Add,
		subroutine.Rotate,
		subroutine.Xor,
		subroutine.ReverseBits,
		subroutine.Shuffle,
	}
	LayerArr = []int{1, 2, 4, 8, 16, 32, 16, 8, 4, 2, 1}
)

func main() {
	flag := os.Args[1]

	// Create layers with 1, 2, 4, 8, 16, 32, 16, 8, 4, 2, 1 functions
	noLayers := len(LayerArr)
	layers := make([][]subroutine.Routine, noLayers)

	for i := 0; i < noLayers; i++ {
		layerSize := LayerArr[i]
		arr := make([]subroutine.Routine, layerSize)
		for j := 0; j < layerSize; j++ {
			arr[j] = EncFunctions[j%len(EncFunctions)]
		}
		layers[i] = arr
	}

	// Encrypt flag using the layers
	acc := flag
	for i := 0; i < noLayers; i++ {
		tmp := strings.Builder{}
		currLayer := layers[i]
		layerSize := len(currLayer)
		parts := utils.SplitStringIntoParts(acc, layerSize)

		// For each part apply function in layer
		recvChan := make(chan common.OrderedString, layerSize)
		for j := 0; j < layerSize; j++ {
			part := parts[j]
			f := currLayer[j]

			go func(recvChan chan common.OrderedString, i int) {
				res := f(part)
				recvChan <- common.OrderedString{Str: res, Index: i}
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
	}

	// Combine into a string
	uEnc := base64.URLEncoding.EncodeToString([]byte(acc))
	fmt.Printf("%+v\n", uEnc)
}
