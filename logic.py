import numpy as np


def distance(shifted_m1_to_m2_to_0_x_p_plus_m2_cm, m2):
    dist = []
    for line_x_y_z in range(len(shifted_m1_to_m2_to_0_x_p_plus_m2_cm)):
        dist.append([np.linalg.norm(shifted_m1_to_m2_to_0_x_p_plus_m2_cm[line_x_y_z, :] - m2[line_x_y_z, :])])
    dist = np.array(dist)
    return dist


def create_matrix_a(m1, m2):
    result = []
    for x in range(len(m1[0])):
        temp_result = []
        for y in range(len(m2[0])):
            temp = m1[:, x] * m2[:, y]
            temp = temp.mean(dtype=np.float32)
            temp_result.append(temp)
        result.append(temp_result)
    result = np.array(result)
    return result


def shift_m_to_0(m, m2_cm):
    s_0 = m - m2_cm
    return s_0


def shift_m(m1, m2):
    return np.array(m2 - m1)


def center_of_mass(m):
    result = np.array([])
    for x in range(len(m[0])):
        result = np.append(result, m[:, x].mean())
    return result


def calc(m1, m2):
    # I1:K8 - M1
    # m1 = np.array([
    #     [3, 4, 5],
    #     [3, 4, 3],
    #     [3, 2, 5],
    #     [3, 2, 3],
    #     [1, 4, 5],
    #     [1, 4, 3],
    #     [1, 2, 5],
    #     [1, 2, 3]
    # ])
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

    # m1[:, 0] - first column (столбец)
    # m1[0, :] - first line (строка)
    # print(m1[:, 0])
    # print(m1[0, :])
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

    # print("M1:\n", m1)
    # print("M2:\n", m2)

    m1_cm = center_of_mass(m1)
    m2_cm = center_of_mass(m2)
    print("Center of mass M1:", m1_cm)
    print("Center of mass M2:", m2_cm)

    shift_m1_m2 = shift_m(m1_cm, m2_cm)
    print("Shift:", shift_m1_m2)

    shifted_m1_to_m2 = m1 + shift_m1_m2
    print("Shifted M1 to M2 (shifted_m1_to_m2):\n", shifted_m1_to_m2)

    shifted_m1_to_m2_to_0 = shift_m_to_0(shifted_m1_to_m2, m2_cm)
    print("shifted_m1_to_m2 shifted to 0:\n", shifted_m1_to_m2_to_0)
    print("M2 shifted to 0:\n", shift_m_to_0(m2, m2_cm))

    matrix_a = create_matrix_a(shift_m_to_0(shifted_m1_to_m2, m2_cm), shift_m_to_0(m2, m2_cm))
    print("Create matrix A:\n", matrix_a)

    u, s, vh = np.linalg.svd(matrix_a, full_matrices=False)
    print("SVD: \n", "U:\n", u, "\nS:\n", s, "\nVH:\n", vh)

    # p = u*vh
    p = np.dot(u, vh)
    print("p = U*VH:\n", p)

    shifted_m1_to_m2_to_0_x_p = np.dot(shifted_m1_to_m2_to_0, p)
    print("'shifted_m1_to_m2 shifted to 0'*p :\n", shifted_m1_to_m2_to_0_x_p)

    shifted_m1_to_m2_to_0_x_p_plus_m2_cm = shifted_m1_to_m2_to_0_x_p + m2_cm
    print("'shifted_m1_to_m2 shifted to 0'*p + m2_cm:\n", shifted_m1_to_m2_to_0_x_p_plus_m2_cm)

    d_dist = distance(shifted_m1_to_m2_to_0_x_p_plus_m2_cm, m2)
    print("shifted_m1_to_m2_to_0_x_p_plus_m2_cm - M2 Distance(d):\n", d_dist)

    d_dist_average = d_dist.mean()
    print("d average:\n", d_dist_average)

    d_dist_max = d_dist.max()
    print("d maximum:\n", d_dist_max)

    d_dist_min = d_dist.min()
    print("d minimum:\n", d_dist_min)
