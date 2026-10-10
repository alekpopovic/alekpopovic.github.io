// SPDX-License-Identifier: MIT
package lab

import (
	"crypto/sha256"
	"fmt"
	"sync"
)

type segment struct {
	digest [32]byte
	data   []byte
}

// LogStore models one attempt stream. Authentication and durable storage are external.
type LogStore struct {
	mu                      sync.Mutex
	maxSegment, quota, used int
	segments                []segment
}

func NewLogStore(maxSegment, quota int) (*LogStore, error) {
	if maxSegment <= 0 || quota < maxSegment {
		return nil, fmt.Errorf("invalid limits")
	}
	return &LogStore{maxSegment: maxSegment, quota: quota}, nil
}

// Put returns duplicate=true for an identical retry. Gaps and conflicts are errors.
func (s *LogStore) Put(sequence int, data []byte) (duplicate bool, err error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if sequence < 0 || len(data) == 0 || len(data) > s.maxSegment {
		return false, fmt.Errorf("invalid segment")
	}
	digest := sha256.Sum256(data)
	if sequence < len(s.segments) {
		if s.segments[sequence].digest == digest {
			return true, nil
		}
		return false, fmt.Errorf("segment conflict")
	}
	if sequence != len(s.segments) {
		return false, fmt.Errorf("sequence gap")
	}
	if len(data) > s.quota-s.used {
		return false, fmt.Errorf("stream quota exceeded")
	}
	s.segments = append(s.segments, segment{digest: digest, data: append([]byte(nil), data...)})
	s.used += len(data)
	return false, nil
}
func (s *LogStore) Next() int { s.mu.Lock(); defer s.mu.Unlock(); return len(s.segments) }
