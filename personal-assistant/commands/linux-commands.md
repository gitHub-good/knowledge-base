# 🐧 Linux 命令速查

> 按使用场景组织：找到场景 → 复制命令。Git Bash（Windows）下除 systemd 外均可用。

## 📁 一、文件与目录

```bash
ls -lah                    # 人性化大小 + 隐藏文件 + 权限
du -sh * | sort -rh        # 当前目录各子项大小排序（找占空间大户）
df -h                      # 磁盘整体使用率
find . -name "*.log" -mtime +7           # 找 7 天前的日志
find . -size +100M -type f               # 找大于 100M 的文件
tree -L 2 -I 'node_modules|target'       # 目录树（忽略指定目录）
cp -av src/ dst/           # 归档式复制（保留属性、显示过程）
rsync -avz --progress src/ user@host:/path/   # 增量同步到远端
```

## ⚔️ 二、文本三剑客（grep / sed / awk）

```bash
# grep：搜内容
grep -rn "ERROR" logs/ --include="*.log"       # 递归搜、带行号、限定文件
grep -c "ERROR" app.log                        # 只数次数
grep -A 5 -B 5 "NullPointerException" app.log  # 连同前后 5 行上下文
grep -v "health check" app.log                 # 反向：排除健康检查噪音

# sed：批量改
sed -i 's/localhost/10.0.0.1/g' config.yaml   # 就地全局替换（-i 改文件）
sed -n '100,120p' big.log                     # 只看 100~120 行

# awk：按列处理
ps aux | awk '{print $2, $11}'                # 只留 PID 和命令列
awk -F',' '{sum+=$3} END {print sum/NR}' data.csv   # 求第 3 列均值
tail -n 1000 access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head   # Top IP
```

## 📜 三、查看大文件 / 日志

```bash
tail -f app.log                          # 实时滚动（最常用）
tail -f app.log | grep --line-buffered ERROR    # 实时 + 过滤
less +F app.log                          # less 版滚动（Ctrl+C 后可翻页搜索）
head -n 50 / tail -n 50                  # 看头/尾
wc -l app.log                            # 行数
zcat app.log.gz | grep ERROR             # 不解压直接搜 gzip 日志
```

## 🖥️ 四、进程与端口

```bash
ps aux | grep java                # 找进程
lsof -i:8080                      # 谁占了 8080 端口
kill -15 <pid>                    # 优雅退出（先给机会收尾）
kill -9 <pid>                     # 强杀（最后手段）
top / htop                        # 实时资源（htop 更直观）
nohup java -jar app.jar > app.log 2>&1 &     # 后台运行并收集全部输出
```

## 🌐 五、网络连通性

```bash
curl -v -w "\nDNS:%{time_namelookup} 连接:%{time_connect} 总耗时:%{time_total}\n" https://api.example.com/health
# ↑ 一次请求看全过程耗时，接口慢时先跑这条定位在哪一段
curl -X POST http://localhost:8080/api/v1/refund \
     -H "Content-Type: application/json" -H "Authorization: Bearer xxx" \
     -d '{"orderId":"R001","amount":500}'
ping -c 4 host
traceroute host                   # 路由路径
ss -tlnp                          # 本机监听端口（替代 netstat）
```

## 🔑 六、权限与用户

```bash
chmod 755 deploy.sh       # rwxr-xr-x（脚本常见）
chmod 600 id_rsa          # 私钥必须是 600，否则 ssh 拒用
chown user:group file
sudo -i                   # 提权进 root shell
```

## 🗜️ 七、压缩与解压

```bash
tar -czf backup.tar.gz dir/         # 打包+gzip
tar -xzf backup.tar.gz              # 解开
tar -xzf backup.tar.gz -C /target   # 解到指定目录
zip -r dir.zip dir/  /  unzip dir.zip -d /target
```

## 🔧 八、systemd 服务（仅真实 Linux / 服务器）

```bash
systemctl status  nginx
systemctl restart nginx
journalctl -u nginx -f --since "1 hour ago"   # 看服务日志
```

## ⚡ 九、组合拳场景

| 场景 | 命令 |
| --- | --- |
| 磁盘满了急排查 | `df -h` → `du -sh /* 2>/dev/null \| sort -rh \| head` 逐层下钻 |
| 日志里数 ERROR 趋势 | `grep ERROR app.log \| awk '{print substr($0,1,13)}' \| sort \| uniq -c` |
| 找出最占 CPU 的进程 | `ps aux --sort=-%cpu \| head -6` |
| 批量改文件后缀 | `for f in *.txt; do mv "$f" "${f%.txt}.md"; done` |
| 对两台机器的目录 | `rsync -avcn src/ dst/`（-n 干跑，只报差异不真拷） |
