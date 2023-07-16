package subroutine

import (
	"Re/utils"
	"math/bits"
	"strings"
)

var (
	// Rotate the string by n bytes.
	Rotate = RoutineGenerator(func(s string) string {
		if len(s) <= 1 {
			return s
		}
		rand := GetRandFromSeed(int64(len(s)))
		// Rotate the string by n bytes.
		n := rand.Intn(256) % len(s)
		res := s[n:] + s[:n]
		return res
	}, "rotate")

	// Add n bits to each rune.
	Add = RoutineGenerator(func(s string) string {
		rand := GetRandFromSeed(int64(len(s)))
		// Add n bits to each rune
		acc := strings.Builder{}
		for i := 0; i < len(s); i++ {
			var diffuse uint
			if i == 0 {
				diffuse = 0
			} else {
				diffuse = uint(s[i-1])
			}
			n := rand.Uint32() % 256
			b := (uint(s[i]) + uint(n) + diffuse) % 256
			acc.Write([]byte{byte(b)})
		}
		return acc.String()
	}, "Add")

	// Xor each rune with n.
	Xor = RoutineGenerator(func(s string) string {
		rand := GetRandFromSeed(int64(len(s)))
		// Xor each rune with n
		acc := strings.Builder{}
		for i := 0; i < len(s); i++ {
			var diffuse uint
			if i == 0 {
				diffuse = 0
			} else {
				diffuse = uint(s[i-1])
			}
			b := s[i] ^ byte(rand.Intn(256)) ^ byte(diffuse)
			acc.Write([]byte{b})
		}
		return acc.String()
	}, "Xor")

	ReverseBits = RoutineGenerator(func(s string) string {
		// Reverse bits
		acc := strings.Builder{}
		for i := 0; i < len(s); i++ {
			acc.Write([]byte{bits.Reverse8(byte(uint8(s[i])))})
		}
		return acc.String()
	}, "ReverseBits")

	Shuffle = RoutineGenerator(func(s string) string {
		rand := GetRandFromSeed(int64(len(s)))
		arr := utils.GenerateArr(len(s))
		bArr := []byte(s)
		rand.Shuffle(len(arr), func(i, j int) {
			arr[i], arr[j] = arr[j], arr[i]
		})
		acc := make([]byte, len(s))
		for i := 0; i < len(arr); i++ {
			acc[i] = bArr[arr[i]]
		}
		return string(acc)

	}, "Shuffle")
)
