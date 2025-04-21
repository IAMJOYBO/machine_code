import platform
import subprocess
import hashlib
import uuid
import tkinter as tk
import requests
import json

def get_hardware_info():
    """获取硬件信息"""
    system = platform.system()
    if system == "Windows":
        # 获取主板序列号（适用于 Windows）
        try:
            result = subprocess.run(
                'wmic baseboard get serialnumber',
                shell=True,
                capture_output=True,
                text=True
            )
            serial_number = result.stdout.strip().split("\n")[-1].strip()
            return serial_number if serial_number else None
        except Exception as e:
            print(f"获取主板序列号失败: {e}")
            return None
    elif system in ["Linux", "Darwin"]:
        # 获取 MAC 地址（适用于 Linux 和 macOS）
        mac_addr = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                            for elements in range(0, 2 * 6, 8)][::-1])
        return mac_addr
    else:
        print("不支持的操作系统")
        return None

def generate_machine_code(hardware_info):
    """根据硬件信息生成机器码"""
    if not hardware_info:
        print("无法获取硬件信息，无法生成机器码。")
        return None
    
    # 使用 SHA-256 哈希算法生成机器码
    machine_code = hashlib.sha256(hardware_info.encode()).hexdigest()
    return machine_code

def fetch_machine_codes_from_url(url):
    """从指定 URL 下载并解析机器码列表"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # 解析 JSON 数据为列表
            try:
                machine_codes = json.loads(response.text)
                if isinstance(machine_codes, list):
                    return [code.strip() for code in machine_codes if isinstance(code, str) and code.strip()]
                else:
                    print("JSON 数据格式错误，不是数组类型。")
                    return []
            except json.JSONDecodeError as e:
                print(f"解析 JSON 数据失败: {e}")
                return []
        else:
            print(f"无法下载 JSON 数据，状态码: {response.status_code}")
            return []
    except Exception as e:
        print(f"下载 JSON 数据失败: {e}")
        return []

def compare_machine_code(machine_code, machine_codes):
    """对比生成的机器码是否存在于列表中"""
    return machine_code in machine_codes

def show_result_message_box(title, message, details=None):
    """通用弹窗显示结果"""
    root = tk.Tk()
    root.title(title)
    root.geometry("500x300")

    # 显示消息
    label_message = tk.Label(root, text=message, font=("Arial", 14))
    label_message.pack(pady=10)

    # 显示详细信息（如果有）
    if details:
        text_widget = tk.Text(root, height=10, width=60, font=("Arial", 10))
        text_widget.insert(tk.END, details)
        text_widget.config(state=tk.DISABLED)  # 禁用编辑功能
        text_widget.pack(pady=5)

    # 关闭按钮
    close_button = tk.Button(root, text="关闭", command=root.destroy)
    close_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    # 获取硬件信息
    hardware_info = get_hardware_info()
    if not hardware_info:
        show_result_message_box("错误", "无法获取硬件信息，请检查系统设置。")
        exit()

    # 生成机器码
    machine_code = generate_machine_code(hardware_info)
    if not machine_code:
        show_result_message_box("错误", "无法生成机器码，请检查硬件信息。")
        exit()

    # 下载并解析 JSON 数据
    json_url = "https://github.3x25.com/https://raw.githubusercontent.com/IAMJOYBO/machine_code/main/machine_code.json"
    machine_codes = fetch_machine_codes_from_url(json_url)
    if not machine_codes:
        show_result_message_box("错误", "无法下载或解析 JSON 数据，请检查网络连接或文件格式。")
        exit()

    # 对比机器码
    is_valid = compare_machine_code(machine_code, machine_codes)

    # 弹窗显示结果
    if is_valid:
        show_result_message_box("验证结果", "机器码验证通过！", details=f"当前机器码: {machine_code}")
    else:
        show_result_message_box("验证结果", "机器码验证失败！", details=f"当前机器码: {machine_code}\n已注册的机器码:\n{'\n'.join(machine_codes)}")
