import platform
import subprocess
import hashlib
import uuid
import tkinter as tk

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

def show_copyable_message_box(machine_code):
    """弹窗显示可复制的机器码"""
    root = tk.Tk()
    root.title("机器码生成结果")
    root.geometry("400x150")

    # 创建标签
    label = tk.Label(root, text="您的机器码:", font=("Arial", 12))
    label.pack(pady=10)

    # 创建 Text 小部件以显示机器码
    text = tk.Text(root, height=3, width=40, font=("Arial", 10))
    text.insert(tk.END, machine_code)
    text.pack(pady=5)
    text.config(state=tk.DISABLED)  # 禁用编辑功能，但仍允许选中和复制

    # 创建关闭按钮
    close_button = tk.Button(root, text="关闭", command=root.destroy)
    close_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    hardware_info = get_hardware_info()
    if hardware_info:
        machine_code = generate_machine_code(hardware_info)
        if machine_code:
            # 弹窗显示可复制的机器码
            show_copyable_message_box(machine_code)
        else:
            print("生成机器码失败。")
    else:
        print("无法获取硬件信息，生成机器码失败。")
