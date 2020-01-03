#!/bin/bash
sslocal -c /etc/shadowsocks.json &
#测试shadowsocks 是否配置成功
curl --socks5 127.0.0.1:10001 http://httpbin.org/ip
privoxy /etc/privoxy/config &
source ~/.bashrc
