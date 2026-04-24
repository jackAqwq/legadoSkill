#!/usr/bin/env python3
import json
import re
import requests

# 测试API接口
api_url = "http://yuetingba.cn/api/app/docs-listen/3a209411-e60e-8455-b9a6-5ddcb012d138/ting-with-efi"
response = requests.get(api_url)
print("=== API响应测试 ===")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 测试书籍详情页
book_url = "http://yuetingba.cn/book/detail/3a209408-7fe6-16d4-62c1-5aa2563b7aa1/0"
response = requests.get(book_url)
print("\n=== 书籍详情页测试 ===")
print(f"状态码: {response.status_code}")

# 提取变量
html = response.text
bookId_match = re.search(r"var\s+bookId\s*=\s*'([^']+)", html)
assl_match = re.search(r"var\s+assl\s*=\s*'([^']+)", html)
es_match = re.search(r"var\s+es\s*=\s*'([^']+)", html)

print(f"\n提取的变量:")
print(f"bookId: {bookId_match.group(1) if bookId_match else '未找到'}")
print(f"assl长度: {len(assl_match.group(1)) if assl_match else '未找到'}")
print(f"es: {es_match.group(1) if es_match else '未找到'}")

# 检查变量提取是否成功
if bookId_match and assl_match and es_match:
    print("\n✅ 变量提取成功！")
else:
    print("\n❌ 变量提取失败！")

print("\n=== 测试完成 ===")
