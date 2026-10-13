// Teaching fixture: execute upstream Cobra preflight against explicit version/node inputs.
package preflight

import (
	"bytes"
	"context"
	"encoding/json"
	"github.com/alekpopovic/orch/internal/cli"
	"github.com/alekpopovic/orch/internal/version"
	"github.com/alekpopovic/orch/pkg/types"
	"testing"
)

type fixture struct {
	*cli.APIClient
	nodes []types.Node
}

func (f fixture) GetVersion(context.Context) (types.VersionInfo, error) { return version.Info(), nil }
func (f fixture) ListNodes(context.Context) ([]types.Node, error)       { return f.nodes, nil }
func TestPreflightStructuredDecision(t *testing.T) {
	for _, tc := range []struct {
		agent, status string
		warnings      int
	}{{"0.2.0", "compatible", 0}, {"0.1.0", "blocked", 1}, {"0.4.0", "compatible", 1}} {
		t.Run(tc.agent, func(t *testing.T) {
			var out bytes.Buffer
			cmd := cli.NewRootCommand(cli.Options{Out: &out, Err: &bytes.Buffer{}, DefaultConfig: t.TempDir() + "/absent", NewClient: func(string) (cli.Client, error) {
				base, err := cli.NewAPIClient("http://fixture.invalid")
				if err != nil {
					return nil, err
				}
				return fixture{APIClient: base, nodes: []types.Node{{ID: "atlas-fixture", AgentVersion: tc.agent}}}, nil
			}})
			cmd.SetArgs([]string{"--server", "http://fixture.invalid", "cluster", "check-upgrade"})
			if err := cmd.ExecuteContext(context.Background()); err != nil {
				t.Fatal(err)
			}
			var result struct {
				Status   string   `json:"status"`
				Warnings []string `json:"warnings"`
			}
			if err := json.Unmarshal(out.Bytes(), &result); err != nil {
				t.Fatal(err)
			}
			if result.Status != tc.status || len(result.Warnings) != tc.warnings {
				t.Fatalf("unexpected structured decision %s", out.String())
			}
			t.Logf("agent=%s status=%s warnings=%d command_error=nil", tc.agent, result.Status, len(result.Warnings))
		})
	}
}
