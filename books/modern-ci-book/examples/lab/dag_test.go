package lab

import (
	"reflect"
	"testing"
)

func TestCompileValid(t *testing.T) {
	got, e := Compile([]Node{{ID: "z", Needs: []string{"a", "b"}}, {ID: "b"}, {ID: "a"}}, 10)
	if e != nil || !reflect.DeepEqual(got, []string{"a", "b", "z"}) {
		t.Fatalf("%v %v", got, e)
	}
}
func TestCompileInvalid(t *testing.T) {
	cases := map[string][]Node{
		"empty": {}, "empty-id": {{ID: ""}}, "duplicate": {{ID: "a"}, {ID: "a"}},
		"unknown": {{ID: "a", Needs: []string{"missing"}}}, "self": {{ID: "a", Needs: []string{"a"}}},
		"duplicate-edge": {{ID: "a"}, {ID: "b", Needs: []string{"a", "a"}}},
		"cycle":          {{ID: "a", Needs: []string{"b"}}, {ID: "b", Needs: []string{"a"}}},
	}
	for n, nodes := range cases {
		t.Run(n, func(t *testing.T) {
			if _, e := Compile(nodes, 10); e == nil {
				t.Fatal("accepted invalid graph")
			}
		})
	}
}
func TestCompileLimit(t *testing.T) {
	if _, e := Compile([]Node{{ID: "a"}, {ID: "b"}}, 1); e == nil {
		t.Fatal("limit ignored")
	}
}
