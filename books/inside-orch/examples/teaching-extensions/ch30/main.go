// Book-only real local Git fixture; MemoryService effects only, no containers.
package main

import (
 "context"
 "encoding/json"
 "fmt"
 "os"
 "os/exec"
 "path/filepath"
 "time"
 "github.com/alekpopovic/orch/internal/cli"
 "github.com/alekpopovic/orch/internal/controlplane"
 "github.com/alekpopovic/orch/internal/gitops"
 "github.com/alekpopovic/orch/pkg/types"
)
func must(err error) { if err != nil { panic(err) } }
func git(dir string, args ...string) string {
 command := exec.Command("git", append([]string{"-C", dir, "-c", "core.hooksPath=/dev/null", "-c", "user.name=Inside Orch Fixture", "-c", "user.email=book-fixture@example.test"}, args...)...)
 output, err := command.CombinedOutput(); if err != nil { panic(fmt.Sprintf("git %v: %v: %s", args, err, output)) }; return string(output)
}
func main() {
 ctx := context.Background(); dir, err := os.MkdirTemp("", "inside-orch-atlas-git-"); must(err); defer os.RemoveAll(dir)
 git(dir,"init","-b","main"); file := filepath.Join(dir,"atlas.yaml")
 must(os.WriteFile(file,[]byte("name: atlas-api\nimage: nginx:1.27\nreplicas: 0\nresources:\n  cpu: 100m\n  memory: 64Mi\n"),0600))
 git(dir,"add","atlas.yaml"); git(dir,"commit","-m","add Atlas fixture")
 cp := controlplane.NewMemoryService(); unrelated,err := cp.CreateService(ctx,types.ServiceSpec{Name:"unrelated",Image:"nginx:1.27",Replicas:0});must(err)
 source,err := cp.CreateGitOpsSource(ctx,types.GitOpsSource{RepositoryURL:dir,Branch:"main",Path:".",SyncInterval:time.Minute,Prune:true});must(err)
 controller:=gitops.NewController(cp,nil,cli.ParseDeploy,nil);synced,err:=controller.Sync(ctx,source.ID);must(err)
 firstRevision:=synced.LastRevision;if len(firstRevision)!=40 {panic("missing actual commit")}
 services,err:=cp.ListServices(ctx);must(err);var atlas types.Service
 for _,v:=range services {if v.Spec.Name=="atlas-api" {atlas=v}}
 if atlas.ID=="" {panic("Atlas not applied")}
 _,err=cp.ScaleService(ctx,atlas.ID,2);must(err);states,err:=cp.GitOpsStatus(ctx);must(err)
 if len(states)!=1 || states[0].GitOps.Status!=types.GitOpsDrifted || states[0].Spec.Replicas!=2 {panic("warn altered drift")}
 state:=*states[0].GitOps;state.Policy=types.GitOpsAutoRevert;_,err=cp.MarkGitOpsManaged(ctx,atlas.ID,state);must(err)
 _,err=cp.ScaleService(ctx,atlas.ID,3);must(err);states,err=cp.GitOpsStatus(ctx);must(err)
 if states[0].Spec.Replicas!=0 || states[0].GitOps.Status!=types.GitOpsInSync {panic("auto revert failed")}
 must(os.Remove(file));git(dir,"add","-A");git(dir,"commit","-m","remove Atlas fixture")
 removed,err:=controller.Sync(ctx,source.ID);must(err);deleted,err:=cp.GetService(ctx,atlas.ID);must(err)
 untouched,err:=cp.GetService(ctx,unrelated.ID);must(err)
 if deleted.Status!=types.ServiceDeleted || untouched.Status!=types.ServiceActive {panic("prune boundary failed")}
 must(json.NewEncoder(os.Stdout).Encode(map[string]any{"first_revision":firstRevision,"removed_revision":removed.LastRevision,"warn_replicas":2,"auto_revert_replicas":0,"atlas_deleted":true,"unrelated_preserved":true,"scope":"local committed repository and real MemoryService; no Docker"}))
}
