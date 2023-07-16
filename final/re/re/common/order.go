package common

type OrderedString struct {
	Str   string `json:"str" bson:"str"`
	Index int    `json:"index" bson:"index"`
}
