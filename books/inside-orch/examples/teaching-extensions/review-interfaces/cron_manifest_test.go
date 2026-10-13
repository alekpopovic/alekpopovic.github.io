// Original review fixture: execute unchanged Cobra manifest construction without HTTP.
package interfaces

import (
	"bytes"
	"context"
	"github.com/alekpopovic/orch/internal/cli"
	"github.com/alekpopovic/orch/pkg/types"
	"os"
	"testing"
)

type captureCron struct {
	*cli.APIClient
	t      *testing.T
	called bool
}

func (c *captureCron) CreateCronJob(_ context.Context, s types.CronJobSpec) (types.CronJob, error) {
	c.called = true
	if s.Name != "atlas-report-schedule" || s.Schedule != "0 9 * * 1-5" || s.Timezone != "UTC" || s.ConcurrencyPolicy != types.ConcurrencyForbid || s.JobTemplate.ResourceRequirements.Requests.CPU != 100 || s.JobTemplate.ResourceRequirements.Limits.Memory != 1<<20 || len(s.JobTemplate.Command) != 3 {
		c.t.Fatalf("wrong parsed contract: %+v", s)
	}
	return types.CronJob{ID: "fixture", Spec: s}, nil
}
func TestBookPublishedCronManifest(t *testing.T) {
	b, e := os.ReadFile(os.Getenv("ORCH_BOOK_CRON_MANIFEST"))
	if e != nil {
		t.Fatal(e)
	}
	path := t.TempDir() + "/cron.yaml"
	if e = os.WriteFile(path, b, 0600); e != nil {
		t.Fatal(e)
	}
	base, e := cli.NewAPIClient("http://fixture.invalid")
	if e != nil {
		t.Fatal(e)
	}
	client := &captureCron{APIClient: base, t: t}
	cmd := cli.NewRootCommand(cli.Options{Out: &bytes.Buffer{}, Err: &bytes.Buffer{}, DefaultConfig: t.TempDir() + "/absent", NewClient: func(string) (cli.Client, error) { return client, nil }})
	cmd.SetArgs([]string{"--server", "http://fixture.invalid", "cronjob", "apply", path})
	if e = cmd.ExecuteContext(context.Background()); e != nil {
		t.Fatal(e)
	}
	if !client.called {
		t.Fatal("manifest did not reach client boundary")
	}
	t.Log("Actual published YAML reached unchanged CLI CronJobClient with quantity conversions; no server, job execution or Docker")
}
