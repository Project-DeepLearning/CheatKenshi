from pymem import *
from pymem.process import *
from customtkinter import *
import tkinter as tk
import sys


class MemoryHacking(object):
    def __init__(self, name):
        try:
            self.process = pymem.Pymem(name)
            module = module_from_name(self.process.process_handle, name)
            self.module = module.lpBaseOfDll
        except pymem.exception.ProcessNotFound:
            sys.exit(0)

    def PointerAddress(self, module, offset, offsets):
        address = self.process.read_int(self.module + offset)
        for value in offsets:
            if value != offsets[-1]:
                address = self.process.read_int(address + value)
        return address + offsets[-1]

    def ReadValue(self, offset, offsets):
        self.pointer = self.PointerAddress(self.module, offset, offsets)
        return self.process.read_int(self.pointer)

    def WriteValue(self, offset, offsets, value):
        self.pointer = self.PointerAddress(self.module, offset, offsets)
        self.process.write_int(self.pointer, value)


GameBomber = MemoryHacking("kenshi_GOG_x64.exe")
money = GameBomber.ReadValue(offset=0x01AC3EC8, offsets=[0xF0, 0x3C0, 0x78, 0x8, 0x48, 0x80, 0x88])

def execute():
    money = GameBomber.ReadValue(offset=0x01AC3EC8, offsets=[0xF0, 0x3C0, 0x78, 0x8, 0x48, 0x80, 0x88])
    GameBomber.WriteValue(offset=0x01AC3EC8, offsets=[0xF0, 0x3C0, 0x78, 0x8, 0x48, 0x80, 0x88], value=money + 10000)
    money = GameBomber.ReadValue(offset=0x01AC3EC8, offsets=[0xF0, 0x3C0, 0x78, 0x8, 0x48, 0x80, 0x88])
    label_value.config(text = "{:,.0f} $".format(money))
    main.update()

main = CTk()
main.title(" ")
main.geometry("280x200")
main.overrideredirect(False)
main.resizable(width=False, height=False)
main.call("wm", "attributes", ".", "-alpha", "0.7")
main.call("wm", "attributes", ".", "-topmost", "false")


frame_background = CTkFrame(master=main, width=280, height=20, corner_radius=0)
frame_background.configure(fg_color="gray17", bg="gray17")
frame_background.pack(side="top", fill="both")
frame_background.columnconfigure(0, weight=1)
frame_background.columnconfigure(1, weight=3)

label_additem = CTkLabel(frame_background, text="Add item:", text_font=("SimSun-ExtB", 12))
label_additem.configure(bg_color="gray17", fg_color="gray17", text_color="#FFFFFF")
label_additem.grid(row=0, column=0, padx=1, pady=10)

button_money = CTkButton(frame_background, text="+10000 $", text_font=("SimSun-ExtB", 12), border_width=1, corner_radius=3)
button_money.configure(bg_color="gray17", fg_color="lime", border_color="#000000", hover_color="yellow")
button_money.config(command=execute)
button_money.grid(row=0, column=1, padx=1, pady=10)

label_money = CTkLabel(frame_background, text="Money:", text_font=("SimSun-ExtB", 12))
label_money.configure(bg_color="gray17", fg_color="gray17", text_color="#FFFFFF")
label_money.grid(row=1, column=0, padx=1, pady=10, sticky="NW")

label_value = CTkLabel(frame_background, text="{:,.0f} $".format(money), text_font=("SimSun-ExtB", 12))
label_value.configure(bg_color="gray17", fg_color="gray17", text_color="#FFFFFF")
label_value.grid(row=1, column=1, padx=1, pady=10, sticky="NW")

label_name = CTkLabel(main, text=" MOD by DUKE ", text_font=("SimSun-ExtB", 12))
label_name.configure(bg_color="gray17", fg_color="gray17", text_color="#FFFFFF")
label_name.pack(fill=None,  padx=1, pady=10)

label_title = CTkLabel(main, text=" Kenshi MOD v1.0 ", text_font=("SimSun-ExtB", 12))
label_title.configure(bg_color="gray17", fg_color="gray17", text_color="#FFFFFF")
label_title.pack(fill=None,  padx=1, pady=1)


main.mainloop()
