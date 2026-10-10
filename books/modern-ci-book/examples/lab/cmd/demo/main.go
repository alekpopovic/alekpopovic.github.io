// SPDX-License-Identifier: MIT
package main

import (
	lab "example.com/modern-ci-book/lab"
	"fmt"
	"time"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}
func main() {
	order, err := lab.Compile([]lab.Node{{ID: "test"}, {ID: "package", Needs: []string{"test"}}, {ID: "deploy", Needs: []string{"package"}}}, 100)
	must(err)
	fmt.Println("compiled order:", order)
	l := lab.NewLedger()
	must(l.Add("test"))
	now := time.Date(2026, 10, 10, 0, 0, 0, 0, time.UTC)
	old, err := l.Claim("test", "runner-1", now, 30*time.Second)
	must(err)
	must(l.Start(old, now))
	l.Expire(now.Add(31 * time.Second))
	fmt.Println("after expiry:", l.State("test"))
	fmt.Println("blind retry refused:", l.Retry("test") != nil)
	must(l.ReconcileStopped(old, "failed"))
	must(l.Retry("test"))
	next, err := l.Claim("test", "runner-2", now.Add(time.Minute), 30*time.Second)
	must(err)
	must(l.Start(next, now.Add(time.Minute)))
	fmt.Println("stale result refused:", l.Complete(old, "succeeded", now.Add(time.Minute)) != nil)
	must(l.Complete(next, "succeeded", now.Add(time.Minute)))
	fmt.Println("current outcome:", l.State("test"))
	logs, err := lab.NewLogStore(1024, 4096)
	must(err)
	_, err = logs.Put(0, []byte("test passed\n"))
	must(err)
	duplicate, err := logs.Put(0, []byte("test passed\n"))
	must(err)
	fmt.Println("identical log retry:", duplicate, "next sequence:", logs.Next())
}
