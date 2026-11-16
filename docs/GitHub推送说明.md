# 如何把本包放到 GitHub（建议你自己操作）

## 建议
- 建 **private** 仓库（私有），只放本包内容；
- 不要放任何生产口令/API Key/SSH 私钥（本包已不含）；
- 如果想让线上 Gemini 读，给它仓库的只读链接即可，不要给账号密码。

## 步骤（本机已 init 好 git 仓库，可直接推）
1. 在 GitHub 新建私有仓库（不要勾选自动生成 README）；
2. 在本目录执行：
   ```bash
   git remote add origin https://github.com/<你的账号>/<仓库名>.git
   git branch -M main
   git push -u origin main
   ```
3. 如果命令行要凭据，用 GitHub 的 Personal Access Token（细粒度、只给该仓库 contents 写权限、设短有效期）；**不要把 token 发给任何人/写进文件**。
4. 推完把仓库链接给 Gemini（private 需要给访问权限）。

## 如果不想自己推
- 本包已在本机生成 zip（见上级目录 handoff_github.zip），可直接上传；
- 不要把本机路径/生产凭据发给外部。
