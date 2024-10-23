# import schemdraw
# import schemdraw.elements as elm
# import tkinter as tk
# import tksvg

# d = schemdraw.Drawing(canvas='svg', show=False)
# d += elm.Resistor().down().label('R=100', loc='bottom')
# d += elm.Resistor().left()
# image = d.get_imagedata('svg')

# print(image)
# window = tk.Tk()
# svg_image = tksvg.SvgImage(data=image)
# label = tk.Label(window, image=svg_image)
# label.pack()
# window.mainloop()

import schemdraw
import schemdraw.elements as elm
import tksvg

import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x640")

schemdraw.svgconfig.svg2 = False
#elm.style(elm.STYLE_IEC)

def draw_resistor_divider(v_in: list[str], v_out: list[str], r_values: list[str]) -> bytes:
    d = schemdraw.Drawing(canvas='svg', show=False)
    d.config(unit=2)
    d += elm.Line().idot().label(v_in[0])
    for i in range(len(r_values)-1):
        d += elm.Resistor().dot().down().label(r_values[i], loc='top')
        d.push()
        d += elm.Line().dot(open=True).label([v_out[i]]).right()
        d.pop()
    d += elm.Resistor().down().label(r_values[-1], loc='top')
    d += elm.Line().dot().left()
    return d.get_imagedata('svg')

image = draw_resistor_divider(['1v'], ['500m', '300m'], ['100k', '200k', '200k'])

svg_image = tksvg.SvgImage(data=image)

#def button_function():
#    print("button pressed")

# Use CTkButton instead of tkinter Button
#button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
#button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

schem = customtkinter.CTkLabel(master=app, text="", image=svg_image)
schem.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
app.mainloop()
