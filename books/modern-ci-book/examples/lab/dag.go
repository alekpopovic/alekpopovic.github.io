// SPDX-License-Identifier: MIT
package lab

import (
	"fmt"
	"sort"
)

type Node struct {
	ID    string
	Needs []string
}

// Compile validates a bounded graph and returns deterministic topological order.
// This is a graph helper, not a YAML parser or an authorization engine.
func Compile(nodes []Node, limit int) ([]string, error) {
	if limit <= 0 || len(nodes) == 0 || len(nodes) > limit {
		return nil, fmt.Errorf("invalid graph size")
	}
	counts := make(map[string]int, len(nodes))
	children := make(map[string][]string)
	for _, n := range nodes {
		if n.ID == "" {
			return nil, fmt.Errorf("empty node id")
		}
		if _, exists := counts[n.ID]; exists {
			return nil, fmt.Errorf("duplicate node: %s", n.ID)
		}
		counts[n.ID] = 0
	}
	for _, n := range nodes {
		seen := map[string]bool{}
		for _, dep := range n.Needs {
			if dep == n.ID {
				return nil, fmt.Errorf("self dependency: %s", n.ID)
			}
			if _, ok := counts[dep]; !ok {
				return nil, fmt.Errorf("unknown dependency: %s", dep)
			}
			if seen[dep] {
				return nil, fmt.Errorf("duplicate dependency: %s", dep)
			}
			seen[dep] = true
			counts[n.ID]++
			children[dep] = append(children[dep], n.ID)
		}
	}
	var ready, order []string
	for id, n := range counts {
		if n == 0 {
			ready = append(ready, id)
		}
	}
	for len(ready) > 0 {
		sort.Strings(ready)
		id := ready[0]
		ready = ready[1:]
		order = append(order, id)
		for _, child := range children[id] {
			counts[child]--
			if counts[child] == 0 {
				ready = append(ready, child)
			}
		}
	}
	if len(order) != len(nodes) {
		return nil, fmt.Errorf("cycle detected")
	}
	return order, nil
}
