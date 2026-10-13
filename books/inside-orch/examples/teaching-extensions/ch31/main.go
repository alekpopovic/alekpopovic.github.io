// Book-only timezone/parser experiment. No controller, jobs or Docker process.
package main
import (
 "encoding/json"
 "os"
 "time"
 "github.com/alekpopovic/orch/internal/cronjobs"
)
func main(){
 schedule,err:=cronjobs.Parse("0 9 * * *");if err!=nil {panic(err)}
 base:=time.Date(2026,10,13,0,0,0,0,time.UTC)
 utc:=schedule.Next(base)
 loc,err:=time.LoadLocation("Europe/Belgrade");if err!=nil {panic(err)}
 local:=schedule.Next(base.In(loc))
 if !utc.Equal(time.Date(2026,10,13,9,0,0,0,time.UTC)) || !local.UTC().Equal(time.Date(2026,10,13,7,0,0,0,time.UTC)) {panic("timezone arithmetic mismatch")}
 minute,err:=cronjobs.Parse("* * * * *");if err!=nil {panic(err)}
 due:=minute.Between(base,base.Add(3*time.Minute),2);if len(due)!=2 || !due[0].Equal(base.Add(time.Minute)) || !due[1].Equal(base.Add(2*time.Minute)) {panic("bounded earliest due mismatch")}
 if _,err:=cronjobs.Parse("0 0 9 * * *");err==nil {panic("six-field syntax accepted")}
 if err=json.NewEncoder(os.Stdout).Encode(map[string]any{"base_utc":base,"utc_next":utc,"belgrade_next_utc":local.UTC(),"bounded_due":due,"six_fields_rejected":true,"scope":"schedule parser with explicit clock values; no execution guarantee"});err!=nil {panic(err)}
}
