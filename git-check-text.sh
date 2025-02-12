#!/bin/bash

# 设置 API URL 和 API Key
API_URL="http://2.56.166.37/v1/files/upload"
API_KEY="app-83PtGwvm0uEafWYiSfSOAqPF"
USER="abc-123"

# 获取 Git 提交中的新增文件
added_files=$(git diff --cached --name-only --diff-filter=A)

# 遍历新增的文件
for file in $added_files; do
    # 只检查 Markdown 文件
    if [[ $file == *.md ]]; then
        echo "正在处理文件：$file"

        # 上传文件到 API 进行分析
        response=$(curl -s -X POST "$API_URL" \
            --header "Authorization: Bearer $API_KEY" \
            --form "file=@$file;type=text/markdown" \
            --form "user=$USER")

        # 输出 API 返回结果
        echo "API 返回结果：$response"
    fi
done