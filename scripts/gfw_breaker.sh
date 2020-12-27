#!/bin/bash
#sslocal -c /etc/shadowsocks.json &
#测试shadowsocks 是否配置成功
#使用v2ray替代shadowsocks 是否配置成功
#/usr/bin/v2ray/v2ray -config /etc/v2ray/config.json
curl --socks5 127.0.0.1:1080 http://httpbin.org/ip
curl  127.0.0.1:1087 http://httpbin.org/ip
privoxy /etc/privoxy/config &
source ~/.bashrc
