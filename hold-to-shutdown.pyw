import keyboard
import time, threading
import tkinter as tk
import tkinter.ttk as ttk
import shlex, subprocess
cnt = 0
isexit = False
root = tk.Tk()
root.title("Shutdown manager")
root.iconbitmap("app.ico")
root.geometry("300x50+960+0")
root.attributes("-toolwindow", True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0)
lttime = time.time()
pgb = ttk.Progressbar(root, orient="horizontal", length=278, mode="determinate")
pgb.pack()
pgb.place(x=12, y=12)
pgb["value"] = 0
def pend_shutdown():
    global cnt, isexit, lttime, t
    while not isexit:
        if keyboard.is_pressed("Ctrl+Shift+Enter"):
            for i in range(10):
                root.attributes("-alpha", 0.1*(i+1))
                time.sleep(0.001)
            time.sleep(1)
            cnt += 1
            prev = pgb["value"]
            for i in range(11):
                pgb["value"] = prev + (i + 1) * 3
                root.after(1)
                root.update()
            lttime = time.time()
            root.attributes("-alpha", 0)
            for i in range(10):
                root.attributes("-alpha", 1-0.1*(i+1))
                time.sleep(0.001)
        if lttime + 2 < time.time() and cnt > 0:
            for i in range(10):
                root.attributes("-alpha", 0.1*(i+1))
                time.sleep(0.001)
            lttime = time.time()
            cnt -= 1
            prev = pgb["value"]
            for i in range(11):
                pgb["value"] = prev - (i + 1) * 3
                root.after(1)
                root.update()
            for i in range(10):
                root.attributes("-alpha", 1-0.1*(i+1))
                time.sleep(0.001)
        if keyboard.is_pressed("Ctrl+Shift+Delete"):
            isexit = True
            break
        if cnt >= 3:
            subprocess.run(shlex.split("shutdown -s -t 0"))
            cnt = 0
            pgb["value"] = 0
    root.destroy()
t = threading.Thread(target=pend_shutdown)
t.start()

root.mainloop()
t.join()
exit()