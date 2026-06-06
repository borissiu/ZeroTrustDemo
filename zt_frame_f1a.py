import zt_mcp_lifecycle_json as zt
import zt_connect_f1 as zt_mcp
import customtkinter as ctk
import requests

# urls = ['https://httpbin.org/cookies', 'https://docs.mcp.cloudflare.com/mcp', 'https://mcp.stayker.com/mcp', 'https://mcp.browserbase.com/mcp', 'https://mcp.context7.com/mcp', '', '', '', '']
urls = ['https://docs.mcp.cloudflare.com/mcp', 'https://mcp.stayker.com/mcp', 'https://mcp.browserbase.com/mcp', 'https://mcp.context7.com/mcp', '', '', '', '']
# urls = ['https://mcp.stayker.com/mcp', 'https://mcp.browserbase.com/mcp', '', '', '', '']
# urls = ['https://docs.mcp.cloudflare.com/mcp', 'https://mcp.stayker.com/mcp<script>alert(1)</script>', 'https://mcp.browserbase.com/mcp', 'https://mcp.context7.com/mcp', '', '', '', '']

app = ctk.CTk()
app.title("F5 Zero Trust Demo")
app.geometry("1728x1117+0+0")

# 1. Configure main app window weights
app.grid_columnconfigure(1, weight=1) # Main display gets all extra width
app.grid_rowconfigure(0, weight=1)

# -------------------------------------------------------------
# SIDEBAR NAVIGATION (Left Panel)
# -------------------------------------------------------------
sidebar_frame = ctk.CTkFrame(app, width=300, corner_radius=0)
sidebar_frame.grid(row=0, column=0, sticky="nsew")
sidebar_frame.grid_propagate(False)

side_title = ctk.CTkLabel(sidebar_frame, text="HTTP/API/MCP Inspector", font=ctk.CTkFont(size=22, weight="bold"))
side_title.pack(padx=15, pady=20)

side_title = ctk.CTkLabel(sidebar_frame, text="URLs", font=ctk.CTkFont(size=18, weight="bold"))
side_title.pack(padx=15, pady=0, side='top', anchor='w')

input_font = ctk.CTkFont(size=16)
warning_font = ctk.CTkFont(size=20)

# -------------------------------------------------------------
# SIDEBAR URLs
# -------------------------------------------------------------
url_entries = []
switch_buttons = []

for item in urls:
    url_frame = ctk.CTkFrame(sidebar_frame, width=300)
    url_frame.pack(padx=15, pady=0, fill="x")
    url_entry = ctk.CTkEntry(url_frame, width=300, height=10, border_width=1, font=input_font)
    url_entry.insert("0", item)
    url_entry.pack(side='left')
    url_entries.append(url_entry)
    switch_btn = ctk.CTkSwitch(url_frame, text='', width=10, button_color='grey', button_hover_color='red', progress_color='red', onvalue=item)
    switch_btn.pack(padx=5, pady=0)
    switch_buttons.append(switch_btn)

# -------------------------------------------------------------
# SIDEBAR Zero Trust Proxy Configuration
# -------------------------------------------------------------
side_title = ctk.CTkLabel(sidebar_frame, text="Zero Trust Proxy", font=ctk.CTkFont(size=18, weight="bold"))
side_title.pack(padx=15, pady=10, side='top', anchor='w')
side_proxy = ctk.CTkEntry(sidebar_frame, width=300, height=10, border_width=1, font=input_font)
side_proxy.pack(side="top", anchor="w", padx=15, pady=0)
side_proxy.insert("0", "f5hklab.ddns.net:8080")

# -------------------------------------------------------------
# SIDEBAR Authentication Configuration
# -------------------------------------------------------------
side_title = ctk.CTkLabel(sidebar_frame, text="Authentication", font=ctk.CTkFont(size=18, weight="bold"))
side_title.pack(padx=15, pady=10, side='top', anchor='w')

user_frame = ctk.CTkFrame(sidebar_frame)
user_frame.pack(padx=15, pady=0, side='top', anchor='w')
side_title = ctk.CTkLabel(user_frame, text="User: ", font=input_font)
side_title.pack(side='left')
side_username = ctk.CTkEntry(user_frame, width=150, border_width=1, font=input_font)
side_username.pack(side="right"
side_username.insert("0", "###Removed###")

passwd_frame = ctk.CTkFrame(sidebar_frame)
passwd_frame.pack(padx=15, pady=0, side='top', anchor='w')
side_title = ctk.CTkLabel(passwd_frame, text="Password: ", font=input_font)
side_title.pack(side='left')
side_password = ctk.CTkEntry(passwd_frame, width=150, border_width=1, show="*", font=input_font)
side_password.pack(side="right")
side_password.insert(0, "###Removed###")

# -------------------------------------------------------------
# SIDEBAR Real-Time Context Logs
# -------------------------------------------------------------
side_title = ctk.CTkLabel(sidebar_frame, text="Logs", font=ctk.CTkFont(size=18, weight="bold"))
side_title.pack(padx=15, pady=10, side='top', anchor='w')

console_box = ctk.CTkTextbox(sidebar_frame, fg_color="#1A1A1A", text_color="#A9B7C6", font=("Consolas", 12))
console_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
console_box.insert("0.0", "[INFO] Ready to go...\n[INFO] Click \"Connect\" or \"Via F5 Fwd-Proxy\" to start.\n")


# -------------------------------------------------------------
# -------------------------------------------------------------
# MAIN DISPLAY AREA (Right Panel)
# -------------------------------------------------------------
# -------------------------------------------------------------
main_display = ctk.CTkFrame(app, fg_color="transparent")
main_display.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

# Configure Main Display rows and columns
main_display.grid_columnconfigure(0, weight=1) # Workspace Column 1
main_display.grid_columnconfigure(1, weight=1) # Workspace Column 2
main_display.grid_rowconfigure(1, weight=0, minsize=60)  # Status Diagram row
main_display.grid_rowconfigure(3, weight=1)    # Dynamic row containing sub-frames stretches down

# --- Row 0: App Title Header ---
header_label = ctk.CTkLabel(main_display, text="Zero Trust Access for Users, Apps, and AI Agents", font=ctk.CTkFont(size=22, weight="bold"))
header_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 10))

# --- Row 1: Status Diagram ---
# status_diagram_frame = ctk.CTkFrame(main_display, fg_color="#1A1A1A", height=200, corner_radius=6)
status_diagram_frame = ctk.CTkFrame(main_display, corner_radius=6)
status_diagram_frame.grid(row=1, column=0, columnspan=2, sticky="ewns", pady=(0, 5))

btn_font = ctk.CTkFont(size=18, weight="bold")


cmd_buttons = []
def btn1():
    r = requests.get("https://httpbin.org/ip", timeout=10)
    print(r.json())
    console_box.insert("end", text="[Exec] App or Agent IP: " + str(r.json()['origin']) + "\n")

direct_connect_buttons = []
def btn2():
    for url in url_entries:
        url = url.get().strip()
        if url != "":
            console_box.insert("end", text="\nConnecting to: " + url + "\n")
            data = zt_mcp.connect_direct(url, side_username.get().strip(), side_password.get().strip(), 'direct')
            for tool in data['result']['tools']:
                console_box.insert("end", text=">>>> Tool Name: " + tool['name'] + "\n")
                print('>>>> ToolName: ' + tool['name'])
                btn = ctk.CTkButton(direct_connect_frame, text="Tool Name: " + tool['name'], font=ctk.CTkFont(size=16), height=30, anchor="w")
                btn.pack(anchor="w", padx=15, pady=5)
                direct_connect_buttons.append(btn)


viaF5_connect_buttons = []
def btn5():
    for url in url_entries:
        url = url.get().strip()
        if url != "":
            console_box.insert("end", text="\nVia F5 Fwd-Proxy: " + url + "\n")
            data = zt_mcp.connect_viaF5(url, side_username.get().strip(), side_password.get().strip(), side_proxy.get().strip())
            # proxy_session, data = zt_mcp.connect_viaF5(url, side_username.get().strip(), side_password.get().strip(), side_proxy.get().strip())
            if data != None:
                for tool in data['result']['tools']:
                    console_box.insert("end", text="ZT>> Tool Name: " + tool['name'] + "\n")
                    print('ZT>> ToolName: ' + tool['name'])
                    if tool['name'] != "Blocked by Zero Trust Policy!":
                        btn = ctk.CTkButton(viaF5_frame, text="Tool Name: " + tool['name'], font=ctk.CTkFont(size=16), height=30, anchor="w")
                    else:
                        btn = ctk.CTkButton(viaF5_frame, text=tool['name'], font=ctk.CTkFont(size=18), height=30, anchor="w", fg_color="#FF6347", hover_color="#FF6347")
                    btn.pack(anchor="w", padx=15, pady=5)
                    viaF5_connect_buttons.append(btn)
    # r = zt_mcp.proxy_disconnect(proxy_session, 'https://httpbin.org/ip')

def btn3():
    for name in direct_connect_buttons:
        name.destroy()
    for name in viaF5_connect_buttons:
        name.destroy()
    console_box.delete("0.0", "end")
    swg_policy_log.delete("0.0", "end")

def adjustPolicy():
    # cmd_buttons[4].configure(border_width=5)
    urls_policy = {}
    urls = [{'name': 'https://httpbin.org/cookies*', 'type': 'glob-match'}]
    for i in range(len(switch_buttons)):
        if switch_buttons[i].get() != 0:
            urls.append({'name': url_entries[i].get().strip(), "type": "glob-match"},)
    urls_policy['urls'] = urls
    r = zt_mcp.updatePolicy(urls_policy)

    r = zt_mcp.checkPolicy()
    output = ''
    for item in r:
        output += '- ' + item['name'] + "\n"
    swg_policy_log.delete("0.0", "end")  # Clear existing log
    swg_policy_log.insert("end", text="AuthN/AuthZ + Per Request Blocking: \n" + output + "\n")

cmd_btn2 = ctk.CTkButton(status_diagram_frame, text="Internal Systems", font=btn_font, height=10, border_width=0, border_color='Red', command=btn2)
cmd_btn2.grid(row=1, column=2, padx=10, pady=0)
cmd_buttons.append(cmd_btn2)

cmd_btn1 = ctk.CTkButton(status_diagram_frame, text="AI\nApp or Agent", font=btn_font, height=60, border_width=0, border_color='Red', command=btn1)
cmd_btn1.grid(row=3, column=1, padx=10, pady=0)
cmd_buttons.append(cmd_btn1)


cmd_btn2 = ctk.CTkButton(status_diagram_frame, text="Direct\nConnect", font=btn_font, height=60, border_width=5, border_color='Red', command=btn2)
cmd_btn2.grid(row=3, column=2, padx=10, pady=0)
cmd_buttons.append(cmd_btn2)

config_title = ctk.CTkLabel(status_diagram_frame, text="<< Internet >>", font=btn_font, height=60)
config_title.grid(row=3, column=3, padx=5, pady=0)
cmd_buttons.append(config_title)

cmd_btn3 = ctk.CTkButton(status_diagram_frame, text="External\nResources", font=btn_font, height=60, border_width=0, border_color='Red', command=btn3)
cmd_btn3.grid(row=3, column=4, padx=10, pady=0)
cmd_buttons.append(cmd_btn3)

cmd_btn = ctk.CTkButton(status_diagram_frame, text="", font=btn_font, height=60, width=0, border_width=0, border_color="#2ECC71")
cmd_btn.grid(row=3, column=5, padx=35, pady=0)
cmd_buttons.append(cmd_btn)


cmd_btn4 = ctk.CTkButton(status_diagram_frame, text="AI\nApp or Agent", font=btn_font, height=60, border_width=0, border_color="#2ECC71", command=btn1)
cmd_btn4.grid(row=3, column=6, padx=0, pady=0)
cmd_buttons.append(cmd_btn4)

# cmd_btn2 = ctk.CTkButton(status_diagram_frame, text="Int. Systems", font=btn_font, height=10, border_width=0, border_color='Red', command=btn2)
# cmd_btn2.grid(row=1, column=6, padx=10, pady=0)
# cmd_buttons.append(cmd_btn2)

cmd_btn5 = ctk.CTkButton(status_diagram_frame, text="F5 ZT Access", font=btn_font, height=60, border_width=5, border_color="#2ECC71", command=btn5)
cmd_btn5.grid(row=3, column=7, columnspan=1, padx=10, pady=0)
cmd_buttons.append(cmd_btn5)

cmd_btn5a = ctk.CTkButton(status_diagram_frame, text="Apply WAF", font=btn_font, height=10, border_width=2, border_color='White', command=btn2)
cmd_btn5a.grid(row=0, column=7, padx=0, pady=0)
cmd_buttons.append(cmd_btn5a)

cmd_btn5b = ctk.CTkButton(status_diagram_frame, text="Filter Tools", font=btn_font, height=10, border_width=2, border_color='White', command=btn2)
cmd_btn5b.grid(row=1, column=7, padx=0, pady=0)
# cmd_buttons.append(cmd_bt5b)

cmd_btn5c = ctk.CTkButton(status_diagram_frame, text="Adjust Policy", font=btn_font, height=10, border_width=2, border_color='White', command=adjustPolicy)
cmd_btn5c.grid(row=2, column=7, padx=0, pady=0)
cmd_buttons.append(cmd_btn5c)

config_title = ctk.CTkLabel(status_diagram_frame, text="<< Internet >>", font=btn_font, height=60)
config_title.grid(row=3, column=11, padx=5, pady=0)
cmd_buttons.append(config_title)

cmd_btn3 = ctk.CTkButton(status_diagram_frame, text="Trusted Ext.\nResources", font=btn_font, height=60, border_width=0, border_color="#2ECC71", command=btn3)
cmd_btn3.grid(row=3, column=12, padx=10, pady=0)
cmd_buttons.append(cmd_btn3)


# --- Row 2: Global Status Banner ---
swg_status_frame = ctk.CTkFrame(main_display, fg_color="#1E3A2F", height=100, corner_radius=0)
swg_status_frame.grid(row=2, column=0, columnspan=1, sticky="ew", pady=(0, 5))
swg_status_frame.pack_propagate(False)

# swg_status_frame_text = ctk.CTkLabel(swg_status_frame, text="● Authentication: Active  |  Per Request Policy: Active", text_color="#2ECC71", font=input_font)
swg_status_frame_text = ctk.CTkLabel(swg_status_frame, text="● Direct Connect  |  Warning : No Protection or Governance!!!", text_color="Red", font=warning_font)
swg_status_frame_text.pack(side="left", padx=15)

swg_policy_log = ctk.CTkTextbox(main_display, fg_color="#1E3A2F", height=100, corner_radius=0, text_color="#2ECC71", font=input_font)
swg_policy_log.grid(row=2, column=1, columnspan=2, sticky="ew", pady=(0, 5))
swg_policy_log.pack_propagate(False)

# --- Row 3: Two Functional Sub-Frames side-by-side ---
# Sub-Frame A: Policy Configuration Panel (Left side)
direct_connect_frame = ctk.CTkScrollableFrame(main_display)
direct_connect_frame.grid(row=3, column=0, padx=(0, 10), sticky="nsew")

def btn1a():
    for name in direct_connect_buttons:
        name.destroy()
config_title = ctk.CTkButton(direct_connect_frame, text="Tools / Resources / Prompts", fg_color='transparent', hover_color='lightgray', text_color='black', font=ctk.CTkFont(size=22, weight="bold"), command=btn1a)
config_title.pack(anchor="w", padx=10, pady=10)

# Sub-Frame B: Live Traffic Logs Console (Right side)
viaF5_frame = ctk.CTkScrollableFrame(main_display)
viaF5_frame.grid(row=3, column=1, padx=(0, 10), sticky="nsew")

def btn2a():
    for name in viaF5_connect_buttons:
        name.destroy()
config_title = ctk.CTkButton(viaF5_frame, text="With F5 Zero Trust Access Management", fg_color='transparent', hover_color='lightgray', text_color='black', font=ctk.CTkFont(size=22, weight="bold"), command=btn2a)
config_title.pack(anchor="w", padx=10, pady=10)
# config_title = ctk.CTkLabel(f5_frame, text="With F5 Zero Trust Access Management", font=ctk.CTkFont(size=22, weight="bold"))
# config_title.pack(anchor="w", padx=15, pady=15)

app.mainloop()
