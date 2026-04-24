#!/usr/bin/env python3
import json
import re

# 读取原始文件内容
with open('/workspace/悦听吧.json', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复转义字符问题
# 处理正则表达式中的\s等转义字符
fixed_content = re.sub(r'(\/\/[^\n]*|\/\*[\s\S]*?\*\/)', lambda m: m.group(0), content)

# 尝试解析修复后的内容
try:
    data = json.loads(fixed_content)
    print("JSON解析成功！")
    # 写回修复后的内容
    with open('/workspace/悦听吧_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("修复后的文件已保存为 /workspace/悦听吧_fixed.json")
except Exception as e:
    print(f"JSON解析失败: {e}")
    # 尝试更简单的方法，直接替换所有可能的转义问题
    # 处理所有反斜杠
    simple_fixed = content.replace('\\', '\\\\')
    # 处理引号
    simple_fixed = simple_fixed.replace('"', '\\"')
    # 尝试重新构建JSON
    try:
        # 找到数组的开始和结束
        start = simple_fixed.find('[')
        end = simple_fixed.rfind(']') + 1
        if start != -1 and end != -1:
            array_content = simple_fixed[start:end]
            data = json.loads(array_content)
            print("简单修复后JSON解析成功！")
            with open('/workspace/悦听吧_fixed.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("修复后的文件已保存为 /workspace/悦听吧_fixed.json")
    except Exception as e2:
        print(f"简单修复也失败: {e2}")
