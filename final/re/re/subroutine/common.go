package subroutine

import (
	"math/rand"
)

type Routine func(string) string

func RoutineGenerator(f Routine, name string) Routine {
	return func(s string) string {
		return f(s)
	}
}

func GetRandFromSeed(seed int64) *rand.Rand {
	return rand.New(rand.NewSource(seed))
}
