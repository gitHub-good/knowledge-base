# 🌿 Git 命令速查

> 提交规范与分支模型见 [Git 提交与分支规范](../../project-development/03-coding-standards/git-conventions.md#commit-spec)，本文只管"命令怎么敲"。

## ⚙️ 一、配置（每台机器一次）

```bash
git config --global user.name  "你的名字"
git config --global user.email "你的邮箱"
git config --global init.defaultBranch main          # 默认分支 main
git config --global pull.rebase true                 # pull 用 rebase，历史更干净
git config --global core.autocrlf input              # 换行符规范
git config --global alias.lg "log --oneline --graph --all --decorate"   # git lg 神器
```

## 🔄 二、日常四件套

```bash
git status                  # 看状态
git add -p                  # 逐块确认暂存（强烈推荐，防止误提交）
git commit -m "feat(xxx): 描述"
git lg                      # 看历史（自定义别名）
```

## 🌿 三、分支操作

```bash
git switch -c feature/REQ-001-部分退保   # 新建并切换分支（新语法）
git switch main                          # 切回 main
git branch -d 分支名                      # 删除已合并分支
git push origin --delete 分支名           # 删除远端分支
git branch -m 新名字                      # 重命名当前分支
```

## 🌐 四、远程同步

```bash
git fetch --all --prune      # 拉取全部远端更新并清理已删分支
git pull --rebase            # 拉取并变基（配合上面的默认配置）
git push -u origin 分支名    # 首次推送并建立追踪
```

## ⚠️ 五、撤销与回退（危险区，看清楚再敲）

```bash
# ── 工作区改动不要了 ──
git restore 文件              # 丢弃某文件未暂存的改动
git restore --staged 文件     # 取消暂存（改动保留）

# ── 提交错了（还没 push）──
git commit --amend            # 修补上一条提交（信息或漏文件）
git reset --soft HEAD~1       # 撤销提交，改动回到暂存区
git reset --hard HEAD~1       # 撤销提交，改动全丢（确认没用的再用）

# ── 已经 push 到共享分支 ──
git revert HEAD               # 生成一条反向提交，历史安全（唯一正确姿势）
git revert --no-commit A..B   # 反转一段区间
```

## 📦 六、暂存 stash（切分支前收尾）

```bash
git stash push -m "退保开发到一半"   # 存起来
git stash list                      # 看列表
git stash pop                       # 取回最近一条并删除记录
git stash apply stash@{2}           # 取回指定条（保留记录）
```

## 🔍 七、查找与定位

```bash
git log --grep="退保"                        # 按提交信息搜
git log -S "refundAmount" --oneline          # 搜变更了该字符串的提交
git blame 文件                               # 逐行追责（看这行谁改的、哪条提交）
git diff main..feature --stat                # 两分支差异概览
git show v2.2.0                              # 看 tag/提交详情
```

## 🏷️ 八、标签与发布

```bash
git tag -a v2.2.0 -m "release 2.2.0"   # 打附注标签（版本号用 SemVer）
git push origin v2.2.0                  # 推送标签
git tag -l "v2.*"                       # 列出匹配标签
```

## 🔀 九、 cherry-pick / rebase（跨分支搬提交）

```bash
git cherry-pick <commit>            # 把某条提交搬到当前分支
git cherry-pick A..B                # 搬一段（不含 A）
git rebase main                     # 当前分支变基到 main（PR 前保持干净）
git rebase --onto new base~3 base   # 高级搬移，少用
```

## 🆘 十、救命三招（误删/手滑之后）

```bash
git reflog                    # 所有 HEAD 移动记录——只要提交过，几乎都能找回
git reset --hard HEAD@{3}     # 回到 reflog 指向的状态
git fsck --lost-found         # 找 dangling 提交（reflog 也没有时的最后手段）
```

> 记住：**在 Git 里，提交过的东西几乎不会真丢**。慌了先 `git reflog`，别乱敲破坏性命令。

## ⚡ 十一、常见场景速决

| 场景 | 命令 |
| --- | --- |
| 提交里混进了大文件/密钥（未推送） | `git reset --soft HEAD~1`，改 `.gitignore` 后重新提交 |
| 密钥已推送到远端 | 立即作废密钥 → `git filter-repo` 清历史 → 强推 → 通知协作者 |
| 想看某文件的历史版本 | `git show HEAD~2:path/to/file` |
| 只想拉半个提交 | `git cherry-pick -n <commit>` 后手动取舍 |
| 合并冲突太多想放弃 | `git merge --abort` / `git rebase --abort` |
