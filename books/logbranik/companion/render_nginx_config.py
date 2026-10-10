"""Generate an isolated loopback Nginx configuration; does not invoke Nginx."""
import argparse
from pathlib import Path
from logbranik.protocol import require


def render(directory, tcp=False):
    directory=Path(directory).resolve()
    require(all(c.isalnum() or c in '/._-' for c in str(directory)), "use a simple path without spaces")
    directory.mkdir(parents=True,exist_ok=True)
    base=Path(__file__).parent/"production-design/examples/nginx"
    http=(base/"http.conf.example").read_text()
    site=(base/"site.conf.example").read_text()
    site=site.replace('/var/log/nginx/guard-access.json',str(directory/'guard-access.json'))
    if tcp:
        site=site.replace('http://unix:/run/nginx-guard/auth.sock:/v1/check','http://127.0.0.1:9101/v1/check')
    else:
        site=site.replace('/run/nginx-guard/auth.sock',str(directory/'auth.sock'))
    return ('worker_processes 1;\nerror_log '+str(directory/'error.log')+';\npid '+str(directory/'nginx.pid')+
            ';\nevents { worker_connections 1024; }\nhttp {\n'+http+'\n'+site+'\n}\n')


if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('--directory',default='lab-state')
    p.add_argument('--tcp-auth',action='store_true'); args=p.parse_args()
    root=Path(args.directory).resolve()
    config=render(root,args.tcp_auth)
    (root/'nginx.conf').write_text(config)
    print(root/'nginx.conf')
