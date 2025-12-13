import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import socket
import csv
from datetime import datetime
import re
import urllib.request
import urllib.error
import base64

class ProxyCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proxy Checker Pro")
        self.root.geometry("1200x700")
        
        self.proxies = []
        self.checked_proxies = []
        self.is_checking = False
        
        self.setup_dark_theme()
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.checker_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.about_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.checker_tab, text='Checker')
        self.notebook.add(self.settings_tab, text='Settings')
        self.notebook.add(self.about_tab, text='About')
        
        self.setup_checker_tab()
        self.setup_settings_tab()
        self.setup_about_tab()
        
    def setup_dark_theme(self):
        style = ttk.Style()
        style.theme_use('default')
        
        bg_color = '#1a1a1a'
        fg_color = '#ffffff'
        select_bg = '#2d2d2d'
        button_bg = '#2d2d2d'
        
        self.root.configure(bg=bg_color)
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', background=button_bg, foreground=fg_color, borderwidth=1)
        style.map('TButton', background=[('active', '#3d3d3d')])
        style.configure('TCheckbutton', background=bg_color, foreground=fg_color)
        style.configure('TEntry', fieldbackground='#2d2d2d', foreground=fg_color)
        style.configure('TCombobox', fieldbackground='#2d2d2d', foreground=fg_color)
        style.configure('TNotebook', background=bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', background=button_bg, foreground=fg_color, padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', '#3d3d3d')])
        style.configure('Treeview', background='#2d2d2d', foreground=fg_color, fieldbackground='#2d2d2d', borderwidth=0)
        style.map('Treeview', background=[('selected', '#404040')])
        style.configure('Treeview.Heading', background='#3d3d3d', foreground=fg_color, borderwidth=1)
        style.map('Treeview.Heading', background=[('active', '#4d4d4d')])
        style.configure('TLabelframe', background=bg_color, foreground=fg_color)
        style.configure('TLabelframe.Label', background=bg_color, foreground=fg_color)
        
    def setup_checker_tab(self):
        top_frame = ttk.Frame(self.checker_tab)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        self.load_btn = ttk.Button(top_frame, text="Load Proxies", command=self.load_proxies)
        self.load_btn.pack(side='left', padx=5)
        
        self.remove_dup_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(top_frame, text="Remove Duplicates", 
                       variable=self.remove_dup_var).pack(side='left', padx=5)
        
        ttk.Label(top_frame, text="Proxy Type:").pack(side='left', padx=5)
        self.proxy_type_var = tk.StringVar(value="HTTP")
        type_combo = ttk.Combobox(top_frame, textvariable=self.proxy_type_var,
                                  values=["HTTP", "HTTPS", "SOCKS4", "SOCKS5"],
                                  width=10, state='readonly')
        type_combo.pack(side='left', padx=5)
        
        ttk.Label(top_frame, text="Input Format:").pack(side='left', padx=5)
        self.input_format_var = tk.StringVar(value="IP:PORT")
        format_combo = ttk.Combobox(top_frame, textvariable=self.input_format_var, 
                                    values=["IP:PORT", "IP:PORT:USER:PASS", "USER:PASS:IP:PORT", 
                                           "IP PORT", "HOST:PORT"], 
                                    width=18, state='readonly')
        format_combo.pack(side='left', padx=5)
        
        second_row = ttk.Frame(self.checker_tab)
        second_row.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(second_row, text="Output Format:").pack(side='left', padx=5)
        self.output_format_var = tk.StringVar(value="IP:PORT")
        output_combo = ttk.Combobox(second_row, textvariable=self.output_format_var,
                                    values=["IP:PORT", "IP PORT", "IP,PORT"],
                                    width=10, state='readonly')
        output_combo.pack(side='left', padx=5)
        
        ttk.Label(second_row, text="Sort:").pack(side='left', padx=5)
        self.sort_var = tk.StringVar(value="None")
        sort_combo = ttk.Combobox(second_row, textvariable=self.sort_var,
                                  values=["None", "IP", "Port", "Country", "Speed", "Status"],
                                  width=10, state='readonly')
        sort_combo.pack(side='left', padx=5)
        
        self.speed_check_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(second_row, text="Check Speed", 
                       variable=self.speed_check_var).pack(side='left', padx=5)
        
        mid_frame = ttk.Frame(self.checker_tab)
        mid_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(mid_frame, text="Timeout (s):").pack(side='left', padx=5)
        self.timeout_var = tk.StringVar(value="10")
        ttk.Entry(mid_frame, textvariable=self.timeout_var, width=10).pack(side='left', padx=5)
        
        self.check_btn = ttk.Button(mid_frame, text="Start Check", command=self.start_check)
        self.check_btn.pack(side='left', padx=5)
        
        self.stop_btn = ttk.Button(mid_frame, text="Stop Check", command=self.stop_check, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(mid_frame, textvariable=self.progress_var).pack(side='left', padx=5)
        
        save_frame = ttk.Frame(self.checker_tab)
        save_frame.pack(fill='x', padx=10, pady=5)
        
        self.save_csv_btn = ttk.Button(save_frame, text="Save as CSV", 
                                       command=lambda: self.save_results('csv'), state='disabled')
        self.save_csv_btn.pack(side='left', padx=5)
        
        self.save_txt_btn = ttk.Button(save_frame, text="Save as TXT",
                                       command=lambda: self.save_results('txt'), state='disabled')
        self.save_txt_btn.pack(side='left', padx=5)
        
        table_frame = ttk.Frame(self.checker_tab)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        v_scroll = ttk.Scrollbar(table_frame, orient='vertical')
        h_scroll = ttk.Scrollbar(table_frame, orient='horizontal')
        
        self.tree = ttk.Treeview(table_frame, columns=('IP', 'Port', 'Type', 'Country', 'Speed', 'Response', 'Status'),
                                 show='headings', yscrollcommand=v_scroll.set,
                                 xscrollcommand=h_scroll.set)
        
        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)
        
        self.tree.heading('IP', text='IP Address')
        self.tree.heading('Port', text='Port')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Country', text='Country')
        self.tree.heading('Speed', text='Speed (KB/s)')
        self.tree.heading('Response', text='Response Time')
        self.tree.heading('Status', text='Status')
        
        self.tree.column('IP', width=140)
        self.tree.column('Port', width=70)
        self.tree.column('Type', width=80)
        self.tree.column('Country', width=100)
        self.tree.column('Speed', width=100)
        self.tree.column('Response', width=110)
        self.tree.column('Status', width=90)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
    def setup_settings_tab(self):
        settings_frame = ttk.LabelFrame(self.settings_tab, text="Connection Settings", padding=20)
        settings_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(settings_frame, text="Test URL:").grid(row=0, column=0, sticky='w', pady=5)
        self.test_url = tk.StringVar(value="https://www.google.com")
        ttk.Entry(settings_frame, textvariable=self.test_url, width=40).grid(row=0, column=1, pady=5, sticky='w')
        
        ttk.Label(settings_frame, text="Speed Test URL:").grid(row=1, column=0, sticky='w', pady=5)
        self.speed_test_url = tk.StringVar(value="http://speedtest.ftp.otenet.gr/files/test100k.db")
        ttk.Entry(settings_frame, textvariable=self.speed_test_url, width=40).grid(row=1, column=1, pady=5, sticky='w')
        
        ttk.Label(settings_frame, text="Default Timeout (seconds):").grid(row=2, column=0, sticky='w', pady=5)
        self.default_timeout = tk.StringVar(value="10")
        ttk.Entry(settings_frame, textvariable=self.default_timeout, width=20).grid(row=2, column=1, pady=5, sticky='w')
        
        ttk.Label(settings_frame, text="Concurrent Checks:").grid(row=3, column=0, sticky='w', pady=5)
        self.threads_var = tk.StringVar(value="10")
        ttk.Entry(settings_frame, textvariable=self.threads_var, width=20).grid(row=3, column=1, pady=5, sticky='w')
        
        ttk.Label(settings_frame, text="Verification Method:").grid(row=4, column=0, sticky='w', pady=5)
        self.verify_method = tk.StringVar(value="HTTP Request")
        method_combo = ttk.Combobox(settings_frame, textvariable=self.verify_method,
                                    values=["HTTP Request", "Socket Connection"],
                                    width=20, state='readonly')
        method_combo.grid(row=4, column=1, pady=5, sticky='w')
        
    def setup_about_tab(self):
        canvas = tk.Canvas(self.about_tab, bg='#1a1a1a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.about_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        about_frame = ttk.Frame(scrollable_frame)
        about_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        title = tk.Label(about_frame, text="Proxy Checker Pro", font=('Arial', 24, 'bold'),
                        bg='#1a1a1a', fg='#00ff00')
        title.pack(pady=10)
        
        version = tk.Label(about_frame, text="Version 3.0 - Ultimate Edition",
                          bg='#1a1a1a', fg='#ffffff', font=('Arial', 12))
        version.pack(pady=5)
        
        description = tk.Label(about_frame, 
                              text="Professional Proxy Checker with Advanced Features\n\n"
                                   "Features:\n"
                                   "• Multiple proxy types (HTTP, HTTPS, SOCKS4, SOCKS5)\n"
                                   "• Multiple input formats support\n"
                                   "• Authentication support (user:pass)\n"
                                   "• Real HTTP request testing with custom URL\n"
                                   "• Speed testing for each proxy\n"
                                   "• Country detection\n"
                                   "• Remove duplicates automatically\n"
                                   "• Real-time checking with accurate results\n"
                                   "• Export to CSV, TXT\n",
                              justify='center', bg='#1a1a1a', fg='#cccccc', font=('Arial', 10))
        description.pack(pady=15)
        
        credits_frame = tk.LabelFrame(about_frame, text="👨‍💻 Developer Credits", bg='#1a1a1a', fg='#00ff00',
                                     font=('Arial', 15, 'bold'), borderwidth=3, relief='groove')
        credits_frame.pack(pady=20, padx=20, fill='x')
        
        credits_text = tk.Label(credits_frame,
                               text="Developed by\n\n"
                                    "📱 Telegram: @MLBOR\n\n"
                                    "💻 GitHub: github.com/NotAnyOneMe",
                               justify='center', bg='#1a1a1a', fg='#00ccff',
                               font=('Consolas', 14, 'bold'))
        credits_text.pack(pady=25)
        
        donate_frame = tk.LabelFrame(about_frame, text="💰 💎 SUPPORT DEVELOPMENT - CRYPTO DONATIONS 💎 💰", 
                                    bg='#1a1a1a', fg='#ffff00',
                                    font=('Arial', 16, 'bold'), borderwidth=5, relief='raised')
        donate_frame.pack(pady=20, padx=20, fill='x')
        
        donate_text = tk.Text(donate_frame, height=18, bg='#0a0a0a', fg='#00ff00',
                             font=('Consolas', 13, 'bold'), wrap='word', borderwidth=4, 
                             relief='sunken', padx=25, pady=25, spacing3=10)
        donate_text.pack(pady=25, padx=25, fill='x')
        
        donate_content = """═══════════════════════════════════════════════════════════════

🪙  TON (The Open Network):
UQD-XUfoicqCzV-RCI6RkEzTO0iNi92ahMUSQ8l27s42LcVf

═══════════════════════════════════════════════════════════════

💎  LTC (Litecoin):
ltc1qtl2tjdacrwk3r2qutl408quqwzeejv29jrvnnl

═══════════════════════════════════════════════════════════════

₿  BTC (Bitcoin):
bc1q6y0qx6xhla2w9utlqusyzpskn0mdvfgzwchg50

═══════════════════════════════════════════════════════════════

💠  ETH (Ethereum):
0xe3C42C6AF102fFDf6856DC2df3Ec7D009F4Eb31B

═══════════════════════════════════════════════════════════════

        Your donation helps keep this project alive! 🚀
        Every contribution is deeply appreciated! ❤️"""
        
        donate_text.insert('1.0', donate_content)
        donate_text.config(state='disabled')
        
        thank_you = tk.Label(about_frame, text="⭐ Thank you for your generous support! ⭐", 
                           bg='#1a1a1a', fg='#ff00ff', font=('Arial', 14, 'bold italic'))
        thank_you.pack(pady=20)
        
        footer = tk.Label(about_frame, text="Made with ❤️ by @MLBOR", 
                         bg='#1a1a1a', fg='#888888', font=('Arial', 10, 'italic'))
        footer.pack(pady=10)
        
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        
    def parse_proxy_line(self, line):
        line = line.strip()
        if not line:
            return None
        
        format_type = self.input_format_var.get()
        
        if format_type == "IP:PORT":
            match = re.search(r'(\d+\.\d+\.\d+\.\d+):(\d+)', line)
            if match:
                return {'ip': match.group(1), 'port': match.group(2), 'user': None, 'pass': None}
        
        elif format_type == "IP:PORT:USER:PASS":
            parts = line.split(':')
            if len(parts) >= 4:
                return {'ip': parts[0], 'port': parts[1], 'user': parts[2], 'pass': parts[3]}
            elif len(parts) == 2:
                return {'ip': parts[0], 'port': parts[1], 'user': None, 'pass': None}
        
        elif format_type == "USER:PASS:IP:PORT":
            parts = line.split(':')
            if len(parts) >= 4:
                return {'ip': parts[2], 'port': parts[3], 'user': parts[0], 'pass': parts[1]}
            elif len(parts) == 2:
                return {'ip': parts[0], 'port': parts[1], 'user': None, 'pass': None}
        
        elif format_type == "IP PORT":
            match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+(\d+)', line)
            if match:
                return {'ip': match.group(1), 'port': match.group(2), 'user': None, 'pass': None}
        
        elif format_type == "HOST:PORT":
            parts = line.split(':')
            if len(parts) >= 2:
                return {'ip': parts[0], 'port': parts[1], 'user': None, 'pass': None}
        
        return None
        
    def load_proxies(self):
        filename = filedialog.askopenfilename(
            title="Select Proxy File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            self.proxies = []
            for line in lines:
                proxy_data = self.parse_proxy_line(line)
                if proxy_data:
                    self.proxies.append(proxy_data)
            
            if self.remove_dup_var.get():
                seen = set()
                unique_proxies = []
                for p in self.proxies:
                    key = (p['ip'], p['port'])
                    if key not in seen:
                        seen.add(key)
                        unique_proxies.append(p)
                self.proxies = unique_proxies
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            proxy_type = self.proxy_type_var.get()
            for proxy in self.proxies:
                auth_info = f" ({proxy['user']})" if proxy['user'] else ""
                self.tree.insert('', 'end', values=(
                    proxy['ip'] + auth_info, 
                    proxy['port'], 
                    proxy_type,
                    'Unknown', 
                    '-', 
                    '-', 
                    'Not Checked'
                ))
            
            messagebox.showinfo("Success", f"Loaded {len(self.proxies)} proxies")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load proxies: {str(e)}")
    
    def get_country(self, ip):
        try:
            req = urllib.request.Request(f'http://ip-api.com/json/{ip}?fields=country',
                                        headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                import json
                data = json.loads(response.read().decode())
                return data.get('country', 'Unknown')
        except:
            return 'Unknown'
    
    def check_proxy_speed(self, proxy_ip, proxy_port, proxy_user, proxy_pass, timeout):
        try:
            proxy_url = f'http://{proxy_ip}:{proxy_port}'
            if proxy_user and proxy_pass:
                proxy_url = f'http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}'
            
            proxy_support = urllib.request.ProxyHandler({
                'http': proxy_url,
                'https': proxy_url
            })
            
            opener = urllib.request.build_opener(proxy_support)
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')]
            
            speed_url = self.speed_test_url.get()
            
            start_time = datetime.now()
            response = opener.open(speed_url, timeout=float(timeout))
            data = response.read()
            end_time = datetime.now()
            
            time_taken = (end_time - start_time).total_seconds()
            if time_taken > 0:
                data_size = len(data) / 1024
                speed = data_size / time_taken
                return f"{speed:.2f}"
            return "N/A"
        except:
            return "N/A"
    
    def check_proxy_http(self, proxy_data, timeout):
        try:
            proxy_ip = proxy_data['ip']
            proxy_port = proxy_data['port']
            proxy_user = proxy_data.get('user')
            proxy_pass = proxy_data.get('pass')
            
            proxy_url = f'http://{proxy_ip}:{proxy_port}'
            if proxy_user and proxy_pass:
                proxy_url = f'http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}'
            
            proxy_support = urllib.request.ProxyHandler({
                'http': proxy_url,
                'https': proxy_url
            })
            
            opener = urllib.request.build_opener(proxy_support)
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')]
            
            test_url = self.test_url.get()
            
            start_time = datetime.now()
            response = opener.open(test_url, timeout=float(timeout))
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds()
            
            if response.getcode() in [200, 301, 302]:
                return ('Working', f"{response_time:.2f}s")
            else:
                return ('Failed', '-')
        except urllib.error.HTTPError as e:
            if e.code in [200, 301, 302]:
                return ('Working', '-')
            return ('Failed', f'HTTP {e.code}')
        except urllib.error.URLError as e:
            return ('Failed', 'Connection Error')
        except socket.timeout:
            return ('Failed', 'Timeout')
        except Exception as e:
            return ('Failed', str(e)[:20])
    
    def check_proxy_socket(self, proxy_data, timeout):
        try:
            proxy_ip = proxy_data['ip']
            proxy_port = proxy_data['port']
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(float(timeout))
            
            start_time = datetime.now()
            result = sock.connect_ex((proxy_ip, int(proxy_port)))
            end_time = datetime.now()
            
            sock.close()
            
            response_time = (end_time - start_time).total_seconds()
            
            if result == 0:
                return ('Working', f"{response_time:.2f}s")
            else:
                return ('Failed', f'Error {result}')
        except socket.timeout:
            return ('Failed', 'Timeout')
        except socket.error as e:
            return ('Failed', 'Connection Error')
        except Exception as e:
            return ('Failed', str(e)[:20])
    
    def check_worker(self, proxies, timeout):
        for idx, proxy_data in proxies:
            if not self.is_checking:
                break
            
            ip = proxy_data['ip']
            port = proxy_data['port']
            user = proxy_data.get('user')
            
            country = self.get_country(ip)
            
            status, time = ('Failed', '-')
            
            try:
                if self.verify_method.get() == "HTTP Request":
                    status, time = self.check_proxy_http(proxy_data, timeout)
                else:
                    status, time = self.check_proxy_socket(proxy_data, timeout)
            except Exception as e:
                status, time = ('Failed', str(e)[:20])
            
            speed = "N/A"
            if status == 'Working' and self.speed_check_var.get():
                try:
                    speed = self.check_proxy_speed(ip, port, user, proxy_data.get('pass'), timeout)
                except:
                    speed = "N/A"
            
            proxy_type = self.proxy_type_var.get()
            auth_info = f" ({user})" if user else ""
            
            self.root.after(0, self.update_tree_item, idx, ip + auth_info, port, proxy_type, country, speed, time, status)
            self.checked_proxies.append((ip, port, proxy_type, country, speed, time, status))
    
    def update_tree_item(self, idx, ip, port, ptype, country, speed, time, status):
        items = self.tree.get_children()
        if idx < len(items):
            item = items[idx]
            self.tree.item(item, values=(ip, port, ptype, country, speed, time, status))
            
            if status == 'Working':
                self.tree.item(item, tags=('working',))
            else:
                self.tree.item(item, tags=('failed',))
        
        self.tree.tag_configure('working', foreground='#00ff00')
        self.tree.tag_configure('failed', foreground='#ff0000')
        
        self.progress_var.set(f"Checked: {len(self.checked_proxies)}/{len(self.proxies)}")
    
    def start_check(self):
        if not self.proxies:
            messagebox.showwarning("Warning", "Please load proxies first")
            return
        
        self.is_checking = True
        self.checked_proxies = []
        self.check_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.load_btn.config(state='disabled')
        self.save_csv_btn.config(state='disabled')
        self.save_txt_btn.config(state='disabled')
        
        timeout = self.timeout_var.get()
        
        thread = threading.Thread(target=self.check_all_proxies, args=(timeout,))
        thread.daemon = True
        thread.start()
    
    def stop_check(self):
        self.is_checking = False
        self.stop_btn.config(state='disabled')
        self.progress_var.set("Stopped by user")
        self.finish_check()
    
    def check_all_proxies(self, timeout):
        indexed_proxies = [(i, proxy) for i, proxy in enumerate(self.proxies)]
        self.check_worker(indexed_proxies, timeout)
        
        self.root.after(0, self.finish_check)
    
    def finish_check(self):
        self.is_checking = False
        self.check_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.load_btn.config(state='normal')
        self.save_csv_btn.config(state='normal')
        self.save_txt_btn.config(state='normal')
        if self.progress_var.get() != "Stopped by user":
            self.progress_var.set(f"Completed: {len(self.checked_proxies)} proxies checked")
        
        self.apply_sort()
    
    def apply_sort(self):
        sort_by = self.sort_var.get()
        if sort_by == "None":
            return
        
        items = [(self.tree.set(item, 'IP'), 
                 self.tree.set(item, 'Port'),
                 self.tree.set(item, 'Type'),
                 self.tree.set(item, 'Country'),
                 self.tree.set(item, 'Speed'),
                 self.tree.set(item, 'Response'),
                 self.tree.set(item, 'Status')) for item in self.tree.get_children()]
        
        if sort_by == "IP":
            items.sort(key=lambda x: [int(i) for i in x[0].split('.')[0].split()[0].split('.')])
        elif sort_by == "Port":
            items.sort(key=lambda x: int(x[1]) if x[1].isdigit() else 0)
        elif sort_by == "Country":
            items.sort(key=lambda x: x[3])
        elif sort_by == "Speed":
            items.sort(key=lambda x: float(x[4]) if x[4] not in ['N/A', '-'] else 0, reverse=True)
        elif sort_by == "Status":
            items.sort(key=lambda x: x[6])
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for item in items:
            self.tree.insert('', 'end', values=item)
    
    def save_results(self, format_type):
        if not self.checked_proxies:
            messagebox.showwarning("Warning", "No results to save")
            return
        
        if format_type == 'csv':
            filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                   filetypes=[("CSV Files", "*.csv")])
            if filename:
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['IP', 'Port', 'Type', 'Country', 'Speed (KB/s)', 'Response Time', 'Status'])
                    writer.writerows(self.checked_proxies)
                messagebox.showinfo("Success", "Saved as CSV")
        
        elif format_type == 'txt':
            filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text Files", "*.txt")])
            if filename:
                with open(filename, 'w') as f:
                    separator = self.output_format_var.get().replace('IP', '').replace('PORT', '').strip()
                    if not separator:
                        separator = ':'
                    
                    for ip, port, ptype, country, speed, timeout, status in self.checked_proxies:
                        if status == 'Working':
                            f.write(f"{ip}{separator}{port}\n")
                messagebox.showinfo("Success", "Saved as TXT (working proxies only)")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProxyCheckerApp(root)
    root.mainloop()
