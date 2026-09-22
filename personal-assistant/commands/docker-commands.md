# 🐳 Docker 命令速查

> 口诀：**镜像是类，容器是实例**。所有 `docker 容器命令` 都可用 `docker container` 显式写法。

## 📦 一、镜像

```bash
docker pull nginx:1.27-alpine        # 拉镜像（优先 alpine/slim 版，小而安全）
docker images                        # 本地镜像列表
docker rmi nginx:1.27-alpine         # 删镜像
docker build -t myapp:2.2.0 .        # 构建（版本号用 SemVer：主.次.修订）
docker tag myapp:2.2.0 registry.cn-hangzhou.aliyuncs.com/ns/myapp:2.2.0
docker push registry.../myapp:2.2.0
docker save -o app.tar myapp:2.2.0   # 导出
docker load -i app.tar               # 导入（离线迁移）
docker history myapp:2.2.0           # 看镜像分层（排查镜像为什么大）
```

## 🔄 二、容器日常

```bash
docker run -d --name myapp \
  -p 8080:8080 \                     # 端口：宿主机:容器
  -e TZ=Asia/Shanghai \              # 环境变量（配置注入，不写死在镜像里）
  -v /data/app/logs:/app/logs \      # 挂载卷（数据与日志持久化）
  --restart unless-stopped \
  myapp:2.2.0

docker ps                # 运行中的容器（-a 含已退出）
docker logs -f --tail 200 myapp        # 滚动看日志
docker exec -it myapp sh               # 进容器（alpine 用 sh，debian 用 bash）
docker stats --no-stream              # 实时资源占用快照
docker inspect myapp | jq '.[0].NetworkSettings.IPAddress'
```

## ♻️ 三、容器生命周期

```bash
docker stop myapp && docker rm myapp    # 停 + 删（--rm 参数可让容器退出即自删）
docker restart myapp
docker cp myapp:/app/logs/error.log ./  # 容器内外拷文件
```

## 🧹 四、清理（磁盘告急四连）

```bash
docker system df                       # 先看：镜像/容器/卷各占多少
docker container prune                 # 清已停止容器
docker image prune -a                  # 清未被使用的镜像
docker volume prune                    # 清悬空卷（确认没数据再清！）
docker system prune -a --volumes       # 一键清空（危险，确认环境再用）
```

## 🧩 五、Docker Compose（多容器编排首选）

```yaml
# docker-compose.yml
services:
  app:
    image: myapp:2.2.0
    ports: ["8080:8080"]
    environment:
      TZ: Asia/Shanghai
      DB_URL: jdbc:postgresql://db:5432/app   # 服务名即主机名
    volumes: ["./logs:/app/logs"]
    depends_on: [db, redis]
    restart: unless-stopped
  db:
    image: postgres:16
    environment: { POSTGRES_PASSWORD: "${DB_PWD}" }   # 密码走 .env，不入库
    volumes: ["pgdata:/var/lib/postgresql/data"]
  redis:
    image: redis:7-alpine
volumes: { pgdata: {} }
```

```bash
docker compose up -d            # 起全套
docker compose logs -f app      # 盯某个服务日志
docker compose ps
docker compose down             # 停全套（-v 连卷一起删，危险）
docker compose up -d --build    # 改完代码重建重启
```

## 🔍 六、排查场景

| 现象 | 排查命令 |
| --- | --- |
| 容器起来就退 | `docker logs <c>`；`docker run` 去掉 `-d` 前台跑看报错 |
| 端口通不了 | `docker ps` 看端口映射 → `docker exec` 进容器 `curl localhost:8080` 分辨是容器内还是映射问题 |
| 容器内没网络/域名解析失败 | `docker network ls`；`docker inspect` 看 Networks；自定义网络内才能用服务名互通 |
| 磁盘被 Docker 吃满 | 见"清理四连"，配合 `docker system df -v` 找大户 |
| 时区差 8 小时 | run 加 `-e TZ=Asia/Shanghai`（或挂 `/etc/localtime`） |
| 镜像越滚越大 | 用多阶段构建（`FROM ... as build` → `FROM runtime` 只拷产物）+ `.dockerignore` 排除 node_modules 等 |

## 📌 七、约定（与项目开发板块的衔接）

- 镜像标签 = 应用版本号（SemVer：主.次.修订）；**禁止裸 `latest` 上生产**——回滚需要明确的版本。
- `Dockerfile` 与 `.dockerignore` 入库走 PR 评审（[05 代码评审](../../project-development/05-code-review/index.md)）。
- 敏感配置全部走环境变量/`.env`（`.env` 已在 [.gitignore](../../.gitignore) 中，永不入库）。
