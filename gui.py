from io import StringIO
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog

import numpy as np

import logic


def p_o(arr):
    return np.array2string(arr).replace('[', ' ').replace(']', ' ').replace('. ', ' ')


def to_np_arr(txt):
    x = []
    for line in txt.splitlines():
        y = [float(value) for value in line.split()]
        x.append(y)
    x = [x for x in x if x != []]
    x = np.array(x, dtype=float)
    return x


def calculate_btn_clicked():
    out_txt.delete(1.0, END)
    m1 = to_np_arr(m1_txt.get(1.0, END))
    m2 = to_np_arr(m2_txt.get(1.0, END))
    m1_cm = logic.center_of_mass(m1)
    m2_cm = logic.center_of_mass(m2)

    out_txt.insert(INSERT, "Center of mass M1: ")
    out_txt.insert(INSERT, p_o(m1_cm))
    out_txt.insert(INSERT, "\nCenter of mass M2: ")
    out_txt.insert(INSERT, p_o(m2_cm))

    shift_m1_m2 = logic.shift_m(m1_cm, m2_cm)
    out_txt.insert(INSERT, "\nShift: ")
    out_txt.insert(INSERT, p_o(shift_m1_m2))

    shifted_m1_to_m2 = m1 + shift_m1_m2
    # shifted_m1_to_m2 = np.sum(m1, shift_m1_m2)
    out_txt.insert(INSERT, "\nShifted M1 to M2 (shifted_m1_to_m2):\n")
    # out_txt.insert(INSERT, shifted_m1_to_m2.tolist())
    out_txt.insert(INSERT, p_o(shifted_m1_to_m2))

    shifted_m1_to_m2_to_0 = logic.shift_m_to_0(shifted_m1_to_m2, m2_cm)
    out_txt.insert(INSERT, "\nshifted_m1_to_m2 shifted to 0:\n")
    out_txt.insert(INSERT, p_o(shifted_m1_to_m2_to_0))
    out_txt.insert(INSERT, "\nM2 shifted to 0:\n")
    out_txt.insert(INSERT, p_o(logic.shift_m_to_0(m2, m2_cm)))

    matrix_a = logic.create_matrix_a(logic.shift_m_to_0(shifted_m1_to_m2, m2_cm), logic.shift_m_to_0(m2, m2_cm))
    out_txt.insert(INSERT, "\nCreate matrix A:\n")
    out_txt.insert(INSERT, p_o(matrix_a))

    u, s, vh = np.linalg.svd(matrix_a, full_matrices=False)
    out_txt.insert(INSERT, "\nSVD: \nU:\n", )
    out_txt.insert(INSERT, p_o(u))
    out_txt.insert(INSERT, "\nS:\n")
    out_txt.insert(INSERT, p_o(s))
    out_txt.insert(INSERT, "\nVH:\n")
    out_txt.insert(INSERT, p_o(vh))

    # p = u*vh
    p = np.dot(u, vh)
    out_txt.insert(INSERT, "\np = U*VH:\n")
    out_txt.insert(INSERT, p_o(p))

    shifted_m1_to_m2_to_0_x_p = np.dot(shifted_m1_to_m2_to_0, p)
    out_txt.insert(INSERT, "\n'shifted_m1_to_m2 shifted to 0'*p :\n")
    out_txt.insert(INSERT, p_o(shifted_m1_to_m2_to_0_x_p))

    shifted_m1_to_m2_to_0_x_p_plus_m2_cm = shifted_m1_to_m2_to_0_x_p + m2_cm
    out_txt.insert(INSERT, "\n'shifted_m1_to_m2 shifted to 0'*p + m2_cm:\n")
    out_txt.insert(INSERT, p_o(shifted_m1_to_m2_to_0_x_p_plus_m2_cm))

    d_dist = logic.distance(shifted_m1_to_m2_to_0_x_p_plus_m2_cm, m2)
    out_txt.insert(INSERT, "\nshifted_m1_to_m2_to_0_x_p_plus_m2_cm - M2 Distance(d):\n")
    out_txt.insert(INSERT, p_o(d_dist))

    d_dist_average = d_dist.mean()
    out_txt.insert(INSERT, "\nd average:\n")
    out_txt.insert(INSERT, p_o(d_dist_average))

    d_dist_max = d_dist.max()
    out_txt.insert(INSERT, "\nd maximum:\n")
    out_txt.insert(INSERT, p_o(d_dist_max))

    d_dist_min = d_dist.min()
    out_txt.insert(INSERT, "\nd minimum:\n")
    out_txt.insert(INSERT, p_o(d_dist_min))


def m1_load_btn_clicked():
    window.filename = filedialog.askopenfilename(initialdir="/", title="Select file")
    file = open(window.filename, "r")
    # global m1
    # x = []
    # for line in file.readlines():
    #     y = [value for value in line.split()]
    #     x.append(y)
    # file.close()
    # m1 = np.array(x)
    # m1 = m1.astype(np.float)
    m1_txt.delete(1.0, END)
    m1_txt.insert(INSERT, file.read())
    file.close()


def m2_load_btn_clicked():
    window.filename = filedialog.askopenfilename(initialdir="/", title="Select file")
    file = open(window.filename, "r")
    # global m2
    # x = []
    # for line in file.readlines():
    #     y = [value for value in line.split()]
    #     x.append(y)
    # file.close()
    # m2 = np.array(x)
    # m2 = m2.astype(np.float)
    m2_txt.delete(1.0, END)
    m2_txt.insert(INSERT, file.read())
    file.close()


def main():
    np.set_printoptions(threshold=np.inf)
    # np.set_printoptions(threshold=None)
    # temp constants
    # global m1
    # m1 = np.array([
    #     [3, 4.37, 4.37],
    #     [3, 3.37, 2.63],
    #     [3, 2.63, 5.37],
    #     [3, 1.63, 3.63],
    #     [1, 4.37, 4.37],
    #     [1, 3.37, 2.63],
    #     [1, 2.63, 5.37],
    #     [1, 1.63, 3.63]
    # ])
    #
    # global m2
    # m2 = np.array([
    #     [4.1, 5.1, 6.1],
    #     [4.1, 5.1, 2.1],
    #     [4.1, 1.1, 6.1],
    #     [4.1, 1.1, 2.1],
    #     [0.1, 5.1, 6.1],
    #     [0.1, 5.1, 2.1],
    #     [0.1, 1.1, 6.1],
    #     [0.1, 1.1, 2.1]
    # ])

    global window
    window = Tk()
    window.title("")
    window.geometry('1000x950')
    window.resizable(width=False, height=False)

    # m1
    m1_load_btn = Button(window, text="Load M1...", command=m1_load_btn_clicked)
    m1_load_btn.grid(column=0, row=0)

    m1_lbl = Label(window, text="M1:")
    m1_lbl.grid(column=0, row=1)

    global m1_txt
    m1_txt = scrolledtext.ScrolledText(window, width=65, height=10)
    m1_txt.grid(column=0, row=2)
    m1_start = """3.   4.37 4.37
3.   3.37 2.63
3.   2.63 5.37
3.   1.63 3.63
1.   4.37 4.37
1.   3.37 2.63
1.   2.63 5.37
1.   1.63 3.63"""
    m1_txt.insert(INSERT, m1_start)

    # m2
    m2_load_btn = Button(window, text="Load M2...", command=m2_load_btn_clicked)
    m2_load_btn.grid(column=1, row=0)

    m2_lbl = Label(window, text="M2:")
    m2_lbl.grid(column=1, row=1)

    global m2_txt
    m2_txt = scrolledtext.ScrolledText(window, width=65, height=10)
    m2_txt.grid(column=1, row=2)
    m2_start = """4.1 5.1 6.1
4.1 5.1 2.1
4.1 1.1 6.1
4.1 1.1 2.1
0.1 5.1 6.1
0.1 5.1 2.1
0.1 1.1 6.1
0.1 1.1 2.1"""
    m2_txt.insert(INSERT, m2_start)

    # Calc Output
    global out_txt
    out_txt = scrolledtext.ScrolledText(window, width=135, height=45)
    out_txt.grid(columnspan=2, row=4)

    # Calculate
    calculate_btn = Button(window, text="Calculate", command=calculate_btn_clicked)
    calculate_btn.grid(columnspan=2, row=3)

    window.mainloop()


if __name__ == '__main__':
    main()
