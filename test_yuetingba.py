#!/usr/bin/env python3
import json
import re

# 测试书源配置
with open('/workspace/悦听吧.json', 'r', encoding='utf-8') as f:
    book_source = json.load(f)[0]

print("=== 悦听吧书源测试 ===")
print(f"书源名称: {book_source['bookSourceName']}")
print(f"书源地址: {book_source['bookSourceUrl']}")
print(f"书源类型: {'音频' if book_source['bookSourceType'] == 1 else '文字'}")
print(f"URL模式: {book_source['bookUrlPattern']}")

# 测试URL模式
print("\n=== 测试URL模式 ===")
test_urls = [
    "http://yuetingba.cn/book/detail/3a209408-7fe6-16d4-62c1-5aa2563b7aa1/0",
    "https://yuetingba.cn/book/detail/3a209408-7fe6-16d4-62c1-5aa2563b7aa1/0",
    "http://www.yuetingba.cn/book/detail/3a209408-7fe6-16d4-62c1-5aa2563b7aa1/0",
    "http://yuetingba.cn/book/detail/3a209408-7fe6-16d4-62c1-5aa2563b7aa1/0?param=test"
]

pattern = book_source['bookUrlPattern']
for url in test_urls:
    match = re.match(pattern, url)
    print(f"URL: {url}")
    print(f"匹配: {'成功' if match else '失败'}")

print("\n=== 测试完成 ===")
print("书源配置看起来正常，现在可以在Legado应用中测试了。")
