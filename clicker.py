import tkinter as tk
from tkinter import messagebox as mb

class ClickerGame:
    def __init__(self, root):
        self.root = root
        root.title("Clicker Game")
        root.geometry("450x650")
        
        self.clicks, self.click_power, self.auto_clicks, self.rebirths = 0, 1, 0, 0
        self.upg_cost, self.auto_upg_cost, self.reb_cost = 10, 75, 1000
        
        self.themes = {
            "dark": {"bg": "#2c3e50", "fg": "#ecf0f1", "btn": "#34495e", "accent": "#3498db"},
            "light": {"bg": "#f8f9fa", "fg": "#212529", "btn": "#e9ecef", "accent": "#0d6efd"}
        }
        self.cur_theme = "dark"

        self.m_frame = tk.Frame(root)
        self.g_frame = tk.Frame(root)

        # Главное меню (без изменений)
        self.m_title = tk.Label(self.m_frame, text="МЕГА КЛИКЕР", font=("Arial", 24, "bold"))
        self.m_title.pack(pady=50)
        tk.Button(self.m_frame, text="Играть", font=("Arial", 16), width=15, bg="#2ecc71", fg="white", command=self.show_game).pack(pady=10)
        tk.Button(self.m_frame, text="Выход", font=("Arial", 16), width=15, bg="#e74c3c", fg="white", command=root.quit).pack(pady=10)

        # Игровой экран
        self.nav = tk.Frame(self.g_frame)
        self.nav.pack(fill=tk.X, pady=5)
        self.b_back = tk.Button(self.nav, text="⬅ В главное меню", font=("Arial", 10), command=self.show_menu)
        self.b_back.pack(side=tk.LEFT, padx=10)
        
        # Кнопка "..." только для настроек внутри игры
        self.b_dots = tk.Button(self.nav, text="...", font=("Arial", 10, "bold"), bd=0, relief=tk.FLAT, command=self.open_settings)
        self.b_dots.pack(side=tk.RIGHT, padx=10)

        self.lbl = tk.Label(self.g_frame, text="clcks: 0\nRebirths: 0", font=("Arial", 16, "bold"))
        self.lbl.pack(pady=10)

        self.b_click = tk.Button(self.g_frame, text="CLICK ME!", font=("Arial", 14, "bold"), fg="white", pady=10, command=self.click)
        self.b_click.pack(pady=5)

        self.sf = tk.LabelFrame(self.g_frame, text=" Магазин ")
        self.sf.pack(fill=tk.X, padx=20, pady=5)
        self.b_upg = tk.Button(self.sf, text=f"+1 к клику ({self.upg_cost})", fg="white", command=self.buy_upg)
        self.b_upg.pack(fill=tk.X, padx=5, pady=2)
        self.b_aupg = tk.Button(self.sf, text=f"Автоклик +1/с ({self.auto_upg_cost})", fg="white", command=self.buy_aupg)
        self.b_aupg.pack(fill=tk.X, padx=5, pady=2)

        self.b_reb = tk.Button(self.g_frame, text=f"Ребёрх (Цена: {self.reb_cost})", font=("Arial", 11, "bold"), bg="#d35400", fg="white", command=self.rebirth)
        self.b_reb.pack(fill=tk.X, padx=20, pady=5)

        self.cf = tk.Frame(self.g_frame)
        self.c_title = tk.Label(self.cf, text="🔒 Введите команду через admin>:")
        self.c_title.pack()
        self.ent = tk.Entry(self.cf, font=("Arial", 12), width=35)
        self.ent.pack(pady=2)
        tk.Button(self.cf, text="Активировать", bg="#9b59b6", fg="white", command=self.check_cd).pack(pady=2)

        self.huge_lbl = tk.Label(self.g_frame, text="", font=("Arial", 9), fg="#f1c40f", wraplength=400)
        self.b_bnk = tk.Button(self.g_frame, text="Отдать 1000 clcks", bg="#e74c3c", fg="white", command=lambda: self.sub_cls(1000, self.b_bnk))
        self.b_sny = tk.Button(self.g_frame, text="КОГДА СОТКУ ВЕРНЁШЬ", bg="#e74c3c", fg="white", command=lambda: self.sub_cls(100, self.b_sny))

        self.show_menu()
        self.auto_tick()
        self.show_povestka()

    def open_settings(self):
        # Окно настроек по кнопке "..."
        st = tk.Toplevel(self.root)
        st.title("Настройки")
        st.geometry("250x150")
        st.configure(bg=self.themes[self.cur_theme]["bg"])
        st.grab_set()

        tk.Button(st, text="Сменить тему ☀️/🌙", command=lambda: [self.toggle_theme(), st.destroy()]).pack(pady=15, fill=tk.X, padx=20)
        tk.Button(st, text="Выйти из кликера", bg="#e74c3c", fg="white", command=self.root.quit).pack(pady=5, fill=tk.X, padx=20)

    def toggle_theme(self):
        self.cur_theme = "light" if self.cur_theme == "dark" else "dark"
        self.apply_theme(self.cur_theme)

    def show_povestka(self):
        pov = tk.Toplevel(self.root)
        pov.title("ВАЖЛИВЕ ПОВІДОМЛЕННЯ")
        pov.geometry(f"{self.root.winfo_screenwidth() // 4}x{self.root.winfo_screenheight() // 2}")
        pov.configure(bg="#7f8c8d")
        pov.attributes("-topmost", True)
        tk.Label(pov, text="ПОВІСТКА\n\nВам потрібно з'явитися до\nТЦК та СП для уточнення даних!\n\nГРА БЛОКОВАНА\nДО ЗАКРИТТЯ ЦЬОГО ВІКНА.", font=("Arial", 12, "bold"), fg="red", bg="#7f8c8d").pack(expand=True, fill=tk.BOTH)
        pov.grab_set()

    def show_menu(self):
        self.g_frame.pack_forget()
        self.m_frame.pack(fill=tk.BOTH, expand=True)
        self.apply_theme(self.cur_theme)

    def show_game(self):
        self.m_frame.pack_forget()
        self.g_frame.pack(fill=tk.BOTH, expand=True)
        if self.rebirths >= 1: self.cf.pack(pady=10)
        self.apply_theme(self.cur_theme)

    def apply_theme(self, name):
        t = self.themes[name]
        for f in [self.root, self.m_frame, self.g_frame, self.nav, self.sf, self.cf]: f.configure(bg=t["bg"])
        self.m_title.configure(bg=t["bg"], fg=t["fg"])
        self.lbl.configure(bg=t["bg"], fg=t["fg"])
        self.c_title.configure(bg=t["bg"], fg=t["fg"])
        self.sf.configure(fg=t["fg"])
        self.huge_lbl.configure(bg=t["bg"])
        self.b_back.configure(bg=t["btn"], fg=t["fg"])
        self.b_click.configure(bg=t["accent"])
        self.b_dots.configure(bg=t["bg"], fg=t["fg"], activebackground=t["bg"], activeforeground=t["fg"])

    def update_ui(self):
        self.lbl.config(text=f"clcks: {self.clicks}\nRebirths: {self.rebirths}")

    def click(self):
        if self.clicks != "Infinity": self.clicks += self.click_power
        self.update_ui()

    def buy_upg(self):
        if self.clicks == "Infinity" or self.clicks >= self.upg_cost:
            if self.clicks != "Infinity": self.clicks -= self.upg_cost
            self.click_power += 1
            self.upg_cost *= 2
            self.b_upg.config(text=f"+1 к клику ({self.upg_cost})")
            self.update_ui()

    def buy_aupg(self):
        if self.clicks == "Infinity" or self.clicks >= self.auto_upg_cost:
            if self.clicks != "Infinity": self.clicks -= self.auto_upg_cost
            self.auto_clicks += 1
            self.auto_upg_cost *= 4
            self.b_aupg.config(text=f"Автоклик +1/с ({self.auto_upg_cost})")
            self.update_ui()

    def rebirth(self):
        if self.clicks == "Infinity" or self.clicks >= self.reb_cost:
            if self.clicks != "Infinity": self.clicks = 0
            self.rebirths += 1
            self.reb_cost *= 2
            self.b_reb.config(text=f"Ребёрх (Цена: {self.reb_cost})")
            if self.rebirths >= 1: self.cf.pack(pady=10)
            self.update_ui()
            mb.showinfo("Ребёрх", "Поле кодов разблокировано!")

    def auto_tick(self):
        if self.auto_clicks > 0 and self.clicks != "Infinity":
            self.clicks += self.auto_clicks
            self.update_ui()
        self.root.after(1000, self.auto_tick)

    def sub_cls(self, amt, btn):
        if self.clicks != "Infinity": self.clicks = max(0, self.clicks - amt)
        self.update_ui()
        btn.pack_forget()

    def check_cd(self):
        text = self.ent.get().strip()
        self.ent.delete(0, tk.END)
        self.huge_lbl.pack_forget()

        if text.startswith("admin>/c /"):
            cd = text.replace("admin>/c /", "").strip()
            if cd == "дуска_падуска":
                self.huge_lbl.config(text="243942830948920174892371598708957093427598732573275089732057329475983275897328957923875832795732897543958347563409658734656984632587346879563428756650834658032\nclcks")
                self.huge_lbl.pack(pady=5)
            elif cd == "777":
                if self.clicks != "Infinity": self.clicks += 777
            elif cd == "+88005553535":
                if self.clicks != "Infinity": self.clicks += 1000
                self.b_bnk.pack(pady=2)
            elif cd == "саня_дай_сотку":
                if self.clicks != "Infinity": self.clicks += 100
                self.b_sny.pack(pady=2)
            elif cd == "+380": self.clicks = "Infinity"
            elif cd == "-clcks": self.clicks = 0
            elif cd.startswith("-") and cd.replace("-", "").isdigit():
                if self.clicks != "Infinity": self.clicks = max(0, self.clicks - int(cd.replace("-", "")))
            else: mb.showwarning("Ошибка", "Неизвестный код!")
            self.update_ui()
        elif text.startswith("admin>/g /"):
            v = text.replace("admin>/g /", "").strip()
            self.clicks = "Infinity" if v.lower() == "infinity" else int(v)
            self.update_ui()
        elif text.startswith("admin>/clr "):
            cp = text.replace("admin>/clr ", "").strip().lower()
            pal = {"0": "#000", "1": "#00A", "2": "#0A0", "3": "#0AA", "4": "#A00", "5": "#A0A", "6": "#A50", "7": "#AAA", "a": "#5F5", "b": "#5FF", "c": "#F55", "d": "#F5F", "e": "#FF5", "f": "#FFF"}
            if cp in pal:
                bg = pal[cp]
                fg = "#000" if cp in ["7", "f", "e", "b", "a"] else "#FFF"
                for w in [self.root, self.m_frame, self.g_frame, self.nav, self.sf, self.cf]: w.configure(bg=bg)
                self.lbl.configure(bg=bg, fg=fg)
                self.m_title.configure(bg=bg, fg=fg)
                self.c_title.configure(bg=bg, fg=fg)
        else: mb.showwarning("Ошибка", "Используйте префикс admin>!")

if __name__ == "__main__":
    r = tk.Tk()
    ClickerGame(r)
    r.mainloop()
