// Source-derived offline inventory. Run only from a disposable copy of the pinned
// orch module: its internal package rule forbids importing from the Jekyll root.
package main

import (
 "encoding/json"
 "io"
 "os"
 "strings"
 "github.com/alekpopovic/orch/internal/cli"
 "github.com/alekpopovic/orch/internal/config"
 "github.com/alekpopovic/orch/pkg/types"
 "github.com/spf13/cobra"
 "github.com/spf13/pflag"
)

type flagInfo struct {Name string `json:"name"`; Shorthand string `json:"shorthand"`;Type string `json:"type"`;Default string `json:"default"`;Usage string `json:"usage"`}
type commandInfo struct {Path string `json:"path"`;Use string `json:"use"`;Short string `json:"short"`;Executable bool `json:"executable"`;ArgsValidator bool `json:"args_validator"`;AcceptedProbeCounts []int `json:"accepted_probe_counts"`;Local []flagInfo `json:"local_flags"`;Persistent []flagInfo `json:"persistent_flags"`;Inherited []flagInfo `json:"inherited_flags"`}
func flags(fs *pflag.FlagSet) []flagInfo {result:=[]flagInfo{};fs.VisitAll(func(f *pflag.Flag){result=append(result,flagInfo{f.Name,f.Shorthand,f.Value.Type(),f.DefValue,f.Usage})});return result}
func main(){
 root:=cli.NewRootCommand(cli.Options{Out:io.Discard,Err:io.Discard,DefaultConfig:"REFERENCE_CONFIG.yml"})
 commands:=[]commandInfo{}
 var walk func(*cobra.Command)
 walk=func(c *cobra.Command){c.InheritedFlags();probes:=[]int{};for n:=0;n<=6;n++{args:=make([]string,n);for i:=range args{args[i]="probe"};if c.Args==nil||c.Args(c,args)==nil{probes=append(probes,n)}};commands=append(commands,commandInfo{c.CommandPath(),c.Use,c.Short,c.Run!=nil||c.RunE!=nil,c.Args!=nil,probes,flags(c.LocalNonPersistentFlags()),flags(c.PersistentFlags()),flags(c.InheritedFlags())});for _,child:=range c.Commands(){walk(child)}}
 walk(root)
 server:=config.LoadServer().Redacted();agent:=config.LoadAgent().Redacted()
 // Exact validators are invoked without any API client or runtime construction.
 task:=[]types.TaskStatus{types.TaskPending,types.TaskAssigned,types.TaskPulling,types.TaskCreated,types.TaskStarting,types.TaskRunning,types.TaskHealthy,types.TaskUnhealthy,types.TaskStopping,types.TaskStopped,types.TaskRemoved,types.TaskFailed}
 node:=[]types.NodeStatus{types.NodeReady,types.NodeDraining,types.NodeOffline,types.NodeUnknown};service:=[]types.ServiceStatus{types.ServiceActive,types.ServiceDeleting,types.ServiceDeleted};deployment:=[]types.DeploymentStatus{types.DeploymentPending,types.DeploymentRunning,types.DeploymentPaused,types.DeploymentSucceeded,types.DeploymentFailed,types.DeploymentRollingBack,types.DeploymentRolledBack}
 matrices:=map[string]map[string][]string{}
 matrices["task_actual"]=map[string][]string{};matrices["task_desired"]=map[string][]string{};matrices["node"]=map[string][]string{};matrices["service"]=map[string][]string{};matrices["deployment"]=map[string][]string{}
 for _,a:=range task{for _,z:=range task{if types.ValidateTaskTransition(a,z)==nil{matrices["task_actual"][string(a)]=append(matrices["task_actual"][string(a)],string(z))};if types.ValidateTaskDesiredTransition(a,z)==nil{matrices["task_desired"][string(a)]=append(matrices["task_desired"][string(a)],string(z))}}}
 for _,a:=range node{for _,z:=range node{if types.ValidateNodeTransition(a,z)==nil{matrices["node"][string(a)]=append(matrices["node"][string(a)],string(z))}}}
 for _,a:=range service{for _,z:=range service{if types.ValidateServiceTransition(a,z)==nil{matrices["service"][string(a)]=append(matrices["service"][string(a)],string(z))}}}
 for _,a:=range deployment{for _,z:=range deployment{if types.ValidateDeploymentTransition(a,z)==nil{matrices["deployment"][string(a)]=append(matrices["deployment"][string(a)],string(z))}}}
 report:=map[string]any{"commands":commands,"server_redacted_defaults":server,"agent_redacted_defaults":agent,"transition_matrices":matrices,"automatic_nodes_excluded":[]string{"help","completion"},"scope":"Offline constructors and lifecycle validators only; no server connection, runtime construction or deployment."}
 report["agent_report_checks"]=map[string]bool{"healthy_duplicate":types.AgentCanReportTaskStatus(types.Task{ActualStatus:types.TaskHealthy,DesiredStatus:types.TaskRunning},types.TaskHealthy),"healthy_after_stop":types.AgentCanReportTaskStatus(types.Task{ActualStatus:types.TaskHealthy,DesiredStatus:types.TaskStopped},types.TaskHealthy),"failed_removed_running_intent":types.AgentCanReportTaskStatus(types.Task{ActualStatus:types.TaskFailed,DesiredStatus:types.TaskRunning},types.TaskRemoved),"failed_removed_cleanup_intent":types.AgentCanReportTaskStatus(types.Task{ActualStatus:types.TaskFailed,DesiredStatus:types.TaskStopped},types.TaskRemoved)}
 if p:=os.Getenv("REFERENCE_CONFIG");strings.TrimSpace(p)!=""{if err:=os.Setenv("ORCH_SERVER_URL","http://127.0.0.1:18080");err!=nil{panic(err)};cfg,err:=config.LoadCLI(p,config.CLIOverrides{ServerURL:"http://127.0.0.1:18082"});report["cli_precedence"]=cfg;if err!=nil{panic(err)}}
 if err:=json.NewEncoder(os.Stdout).Encode(report);err!=nil{panic(err)}
}
