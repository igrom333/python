import tkinter as tk
from tkinter import messagebox as mb

class ClickerGame:
    def __init__(self, root):
        self.root = root
        root.title("Clicker")
        root.geometry("450x650")
        root.configure(bg="#2c3e50")
        
        self.clicks, self.click_power, self.auto_clicks, self.rebirths = 0, 1, 0, 0
        self.upg_cost, self.auto_upg_cost, self.reb_cost = 10, 75, 1000

        # UI элементы
        self.lbl = tk.Label(root, text="Clicks: 0\nRebirths: 0", font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#2c3e50")
        self.lbl.pack(pady=10)

        tk.Button(root, text="CLICK ME!", font=("Arial", 14, "bold"), bg="#3498db", fg="white", pady=10, command=self.click).pack(pady=5)

        # Магазин
        sf = tk.LabelFrame(root, text=" Магазин ", fg="#ecf0f1", bg="#2c3e50")
        sf.pack(fill=tk.X, padx=20, pady=5)
        
        self.b_upg = tk.Button(sf, text=f"+1 к клику ({self.upg_cost})", bg="#2ecc71", fg="white", command=self.buy_upg)
        self.b_upg.pack(fill=tk.X, padx=5, pady=2)
        
        self.b_aupg = tk.Button(sf, text=f"Автоклик +1/с ({self.auto_upg_cost})", bg="#e67e22", fg="white", command=self.buy_aupg)
        self.b_aupg.pack(fill=tk.X, padx=5, pady=2)

        self.b_reb = tk.Button(root, text=f"Ребёрх (Цена: {self.reb_cost})", font=("Arial", 11, "bold"), bg="#d35400", fg="white", command=self.rebirth)
        self.b_reb.pack(fill=tk.X, padx=20, pady=5)

        # Скрытая зона кодов
        self.cf = tk.Frame(root, bg="#2c3e50")
        tk.Label(self.cf, text="🔒 Код:", fg="#ecf0f1", bg="#2c3e50").pack()
        self.ent = tk.Entry(self.cf, font=("Arial", 12), width=25)
        self.ent.pack(pady=2)
        tk.Button(self.cf, text="Активировать", bg="#9b59b6", fg="white", command=self.check_cd).pack(pady=2)

        self.huge_lbl = tk.Label(root, text="", font=("Arial", 9), fg="#f1c40f", bg="#2c3e50", wraplength=400)
        self.b_bnk = tk.Button(root, text="Отдать 1000 clcks", bg="#e74c3c", fg="white", command=lambda: self.sub_cls(1000, self.b_bnk))
        self.b_sny = tk.Button(root, text="КОГДА СОТКУ ВЕРНЁШЬ", bg="#e74c3c", fg="white", command=lambda: self.sub_cls(100, self.b_sny))

        self.auto_tick()

    def update_ui(self):
        self.lbl.config(text=f"Clicks: {self.clicks}\nRebirths: {self.rebirths}")

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
        cd = self.ent.get().strip()
        self.ent.delete(0, tk.END)
        self.huge_lbl.pack_forget()

        if cd == "дуска_падуска":
            self.huge_lbl.config(text="243942830948920174892371598708957093427598732573275089732057329475983275897328957923875832795732897543958347563409658734656984632587346879563428756650834658032\nclcks")
            self.huge_lbl.pack(pady=5)
        elif cd == "777":
            if self.clicks != "Infinity": self.clicks += 777
            self.update_ui()
        elif cd == "+88005553535":
            if self.clicks != "Infinity": self.clicks += 1000
            self.update_ui()
            self.b_bnk.pack(pady=2)
        elif cd == "саня_дай_сотку":
            if self.clicks != "Infinity": self.clicks += 100
            self.update_ui()
            self.b_sny.pack(pady=2)
        elif cd.startswith("admin>/g /"):
            v = cd.replace("admin>/g /", "").strip()
            self.clicks = "Infinity" if v.lower() == "infinity" else int(v)
            self.update_ui()
        elif cd.startswith("admin>/c /"):
            v = cd.replace("admin>/c /", "").strip()
            self.clicks = 0 if v == "-clcks" else max(0, self.clicks - int(v.replace("-", ""))) if self.clicks != "Infinity" else "Infinity"
            self.update_ui()
        elif cd.startswith("admin>/clr "):
            cp = cd.replace("admin>/clr ", "").strip()
            pal = {"0": "#000", "1": "#00A", "2": "#0A0", "3": "#0AA", "4": "#A00", "5": "#A0A", "6": "#A50", "7": "#AAA", "a": "#5F5", "b": "#5FF", "c": "#F55", "d": "#F5F", "e": "#FF5", "f": "#FFF"}
            if cp.lower() in pal:
                bg = pal[cp.lower()]
                fg = "#000" if cp.lower() in ["7", "f", "e", "b", "a"] else "#FFF"
                for w in [self.root, self.cf, self.lbl, self.huge_lbl]: w.configure(bg=bg)
                self.lbl.configure(fg=fg)

if __name__ == "__main__":
    r = tk.Tk()
    ClickerGame(r)
    r.mainloop()