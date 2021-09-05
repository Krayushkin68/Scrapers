import pandas as pd
import numpy as np
import time
import os


def vec_length(a, b):
    return np.sqrt(np.sum((a - b) ** 2))


def vec_scalar_mult(a_1, a_2, b_1, b_2):
    return (a_1[0]-a_2[0]) * (b_1[0]-b_2[0]) + (a_1[1]-a_2[1]) * (b_1[1]-b_2[1]) + (a_1[2]-a_2[2]) * (b_1[2]-b_2[2])


def calculate(npa, idx_cur_o, idx_next_o, delta_1, delta_2, params,  delta_par):
    cur_o = npa[idx_cur_o]
    cur_o_coords = np.array(cur_o[2:], dtype=float)

    first_c = npa[idx_cur_o + delta_1]
    first_c_coords = np.array(first_c[2:], dtype=float)

    next_o = npa[idx_next_o]
    next_o_coords = np.array(next_o[2:], dtype=float)

    second_c = npa[idx_next_o + delta_2]
    second_c_coords = np.array(second_c[2:], dtype=float)

    if params[0] == 'length':
        par_coords = []
        for num, i in enumerate(delta_par):
            if idx_cur_o + i > len(npa):
                par = None
            else:
                par = np.array(npa[idx_cur_o + i][2:], dtype=float)
            par_coords.append(par)

    distance = vec_length(cur_o_coords, next_o_coords)
    scalar_multiply = vec_scalar_mult(cur_o_coords, first_c_coords, next_o_coords, second_c_coords)
    multiply_of_length = vec_length(cur_o_coords, first_c_coords) * vec_length(next_o_coords, second_c_coords)
    cos = scalar_multiply / multiply_of_length
    angle = np.arccos(cos)/np.pi*180

    par_results = []
    if params[0] == 'length':
        par_results.append(distance)
        for i in par_coords:
            if i is None:
                par_res = '-'
            else:
                par_res = vec_length(cur_o_coords, i)
            par_results.append(par_res)

    ret_list = [idx_cur_o + 1, distance, scalar_multiply, multiply_of_length, cos, angle] + par_results
    return ret_list


def calculate_meome(npa, idx_cur_o, delta, params_delta):
    cur_o = npa[idx_cur_o]
    cur_o_coords = np.array(cur_o[2:], dtype=float)

    if idx_cur_o + delta[0] > len(npa):
        skip_len = True
    else:
        skip_len = False
        len_p = npa[idx_cur_o + delta[0]]
        len_p_coords = np.array(len_p[2:], dtype=float)

    if idx_cur_o + params_delta[0] > len(npa):
        skip_params = True
    else:
        skip_params = False
        par1_p1 = npa[idx_cur_o + params_delta[0]]
        par1_p1_coords = np.array(par1_p1[2:], dtype=float)
        par1_p2 = npa[idx_cur_o + params_delta[1]]
        par1_p2_coords = np.array(par1_p2[2:], dtype=float)
        par2_p1 = npa[idx_cur_o + params_delta[2]]
        par2_p1_coords = np.array(par2_p1[2:], dtype=float)
        par2_p2 = npa[idx_cur_o + params_delta[3]]
        par2_p2_coords = np.array(par2_p2[2:], dtype=float)

    angle1_p2 = npa[idx_cur_o + delta[1][0]]
    angle1_p2_coords = np.array(angle1_p2[2:], dtype=float)
    angle1_p3 = npa[idx_cur_o + delta[1][1]]
    angle1_p3_coords = np.array(angle1_p3[2:], dtype=float)
    angle1_p4 = npa[idx_cur_o + delta[1][2]]
    angle1_p4_coords = np.array(angle1_p4[2:], dtype=float)

    angle2_p2 = npa[idx_cur_o + delta[2][0]]
    angle2_p2_coords = np.array(angle2_p2[2:], dtype=float)
    angle2_p3 = npa[idx_cur_o + delta[2][1]]
    angle2_p3_coords = np.array(angle2_p3[2:], dtype=float)
    angle2_p4 = npa[idx_cur_o + delta[2][2]]
    angle2_p4_coords = np.array(angle2_p4[2:], dtype=float)

    if not skip_len:
        distance = vec_length(cur_o_coords, len_p_coords)
    else:
        distance = '-'

    scalar_multiply_1 = vec_scalar_mult(cur_o_coords, angle1_p2_coords, angle1_p3_coords, angle1_p4_coords)
    multiply_of_length_1 = vec_length(cur_o_coords, angle1_p2_coords) * vec_length(angle1_p3_coords, angle1_p4_coords)
    cos_1 = scalar_multiply_1 / multiply_of_length_1
    angle_1 = np.arccos(cos_1) / np.pi * 180

    scalar_multiply_2 = vec_scalar_mult(cur_o_coords, angle2_p2_coords, angle2_p3_coords, angle2_p4_coords)
    multiply_of_length_2 = vec_length(cur_o_coords, angle2_p2_coords) * vec_length(angle2_p3_coords, angle2_p4_coords)
    cos_2 = scalar_multiply_2 / multiply_of_length_2
    angle_2 = np.arccos(cos_2) / np.pi * 180

    if angle_1 > angle_2:
        angle = angle_1
        scalar_multiply = scalar_multiply_1
        multiply_of_length = multiply_of_length_1
        cos = cos_1
    else:
        angle = angle_2
        scalar_multiply = scalar_multiply_2
        multiply_of_length = multiply_of_length_2
        cos = cos_2
    if not skip_params:
        par1 = vec_length(par1_p1_coords, par1_p2_coords)
        par2 = vec_length(par2_p1_coords, par2_p2_coords)
    else:
        par1 = ''
        par2 = ''

    ret_list = [idx_cur_o + 1, distance, scalar_multiply, multiply_of_length, cos, angle, par1, par2]
    return ret_list


def search_near(npa, cur_o_idx, c_idx, cur_delta):
    cur_o = npa[cur_o_idx]
    cur_o_coords = np.array(cur_o[2:], dtype=float)

    skip_list = [cur_o_idx + i for i in cur_delta]

    # префильтр по расстояниям
    par = 5

    c_list = c_idx[np.where(((abs(abs(npa[c_idx][:, 2].astype(np.float32))-abs(cur_o_coords[0])) < par)) &
                            (abs(abs(npa[c_idx][:, 3].astype(np.float32))-abs(cur_o_coords[1])) < par) &
                            (abs(abs(npa[c_idx][:, 4].astype(np.float32))-abs(cur_o_coords[2])) < par))]

    len_list = []
    for c in c_list[:]:
        if c not in skip_list:
            c_p = npa[c]
            c_p_coords = np.array(c_p[2:], dtype=float)
            length = vec_length(cur_o_coords, c_p_coords)
            len_list.append([c+1, length])

    len_list.sort(key=lambda x: x[1])
    ret_list_ind = [i[0] for i in len_list[:5]]
    ret_list_len = [i[1] for i in len_list[:5]]

    if len(ret_list_ind) < 5:
        while len(ret_list_ind) != 5:
            ret_list_ind.append('-')
            ret_list_len.append('-')

    return ret_list_ind+ret_list_len


def calculate_one_page(npa, page_num, delta, params, delta_params):
    o_idx = np.where(npa[:, 1] == 'O')[0]
    every_first_o_idx = o_idx[0::4]
    every_third_o_idx = o_idx[2::4]

    first_delta_1 = delta[0]
    first_delta_2 = delta[1]
    third_delta_1 = delta[2]
    third_delta_2 = delta[3]

    calculated_results_angles = []
    calculated_results_par = []

    for _ in range(params[1]+1):
        calculated_results_par.append([])

    for el_num, el in enumerate(o_idx):
        if el in every_first_o_idx:
            idx_cur_o = el
            idx_next_o = o_idx[el_num + 1]
            delta_1 = first_delta_1
            delta_2 = first_delta_2
            calc_res = calculate(npa, idx_cur_o, idx_next_o, delta_1, delta_2, params, delta_params[:params[1]])
            calculated_results_angles.append(calc_res[5])
            for num, i in enumerate(calc_res[6:]):
                calculated_results_par[num].append(i)
        elif el in every_third_o_idx:
            idx_cur_o = el
            idx_next_o = o_idx[el_num + 1]
            delta_1 = third_delta_1
            delta_2 = third_delta_2
            calc_res = calculate(npa, idx_cur_o, idx_next_o, delta_1, delta_2, params, delta_params[params[1]:])
            calculated_results_angles.append(calc_res[5])
            for num, i in enumerate(calc_res[6:]):
                calculated_results_par[num].append(i)

    df_angles = pd.DataFrame(calculated_results_angles, columns=[page_num])

    dfs = [df_angles]
    for i in calculated_results_par:
        df_par = pd.DataFrame(i, columns=[page_num])
        dfs.append(df_par)

    return dfs


def calculate_one_page_meome(npa, page_num, o1_delta, o2_delta, o1_params_delta, o2_params_delta):
    o_idx = np.where(npa[:, 1] == 'O')[0]
    every_first_o_idx = o_idx[0::2]
    every_second_o_idx = o_idx[1::2]
    calculated_results_angles = []
    calculated_results_length = []
    calculated_results_par1 = []
    calculated_results_par2 = []
    for el_num, el in enumerate(o_idx):
        if el in every_first_o_idx:
            idx_cur_o = el
            delta = o1_delta
            params_delta = o1_params_delta
            calc_res = calculate_meome(npa, idx_cur_o, delta, params_delta)
            calculated_results_angles.append(calc_res[5])
            calculated_results_length.append(calc_res[1])
            calculated_results_par1.append(calc_res[-2])
            calculated_results_par2.append(calc_res[-1])
        elif el in every_second_o_idx:
            idx_cur_o = el
            delta = o2_delta
            params_delta = o2_params_delta
            calc_res = calculate_meome(npa, idx_cur_o, delta, params_delta)
            calculated_results_angles.append(calc_res[5])
            calculated_results_length.append(calc_res[1])
            calculated_results_par1.append(calc_res[-2])
            calculated_results_par2.append(calc_res[-1])

    df_angles = pd.DataFrame(calculated_results_angles, columns=[page_num])
    df_length = pd.DataFrame(calculated_results_length, columns=[page_num])
    df_par1 = pd.DataFrame(calculated_results_par1, columns=[page_num])
    df_par2 = pd.DataFrame(calculated_results_par2, columns=[page_num])
    return [df_angles, df_length, df_par1, df_par2]


def search_near_page(npa, page_num, delta):
    o_idx = np.where(npa[:, 1] == 'O')[0]
    c_idx = np.where(npa[:, 1] == 'C')[0]

    every_first_o_idx = o_idx[0::4]
    every_second_o_idx = o_idx[1::4]
    every_third_o_idx = o_idx[2::4]
    every_fourth_o_idx = o_idx[3::4]

    search_results1 = []
    search_results2 = []
    search_results3 = []
    search_results4 = []
    search_results5 = []
    search_results6 = []
    search_results7 = []
    search_results8 = []
    search_results9 = []
    search_results10 = []
    for el_num, el in enumerate(o_idx):
        print(f'O {el_num} search in page {page_num}')
        if el in every_first_o_idx:
            cur_o_idx = el
            cur_delta = delta[0]
            search_res = search_near(npa, cur_o_idx, c_idx, cur_delta)
            search_results1.append(search_res[0])
            search_results2.append(search_res[1])
            search_results3.append(search_res[2])
            search_results4.append(search_res[3])
            search_results5.append(search_res[4])
            search_results6.append(search_res[5])
            search_results7.append(search_res[6])
            search_results8.append(search_res[7])
            search_results9.append(search_res[8])
            search_results10.append(search_res[9])
        elif el in every_second_o_idx:
            cur_o_idx = el
            cur_delta = delta[1]
            search_res = search_near(npa, cur_o_idx, c_idx, cur_delta)
            search_results1.append(search_res[0])
            search_results2.append(search_res[1])
            search_results3.append(search_res[2])
            search_results4.append(search_res[3])
            search_results5.append(search_res[4])
            search_results6.append(search_res[5])
            search_results7.append(search_res[6])
            search_results8.append(search_res[7])
            search_results9.append(search_res[8])
            search_results10.append(search_res[9])
        elif el in every_third_o_idx:
            cur_o_idx = el
            cur_delta = delta[2]
            search_res = search_near(npa, cur_o_idx, c_idx, cur_delta)
            search_results1.append(search_res[0])
            search_results2.append(search_res[1])
            search_results3.append(search_res[2])
            search_results4.append(search_res[3])
            search_results5.append(search_res[4])
            search_results6.append(search_res[5])
            search_results7.append(search_res[6])
            search_results8.append(search_res[7])
            search_results9.append(search_res[8])
            search_results10.append(search_res[9])
        elif el in every_fourth_o_idx:
            cur_o_idx = el
            cur_delta = delta[3]
            search_res = search_near(npa, cur_o_idx, c_idx, cur_delta)
            search_results1.append(search_res[0])
            search_results2.append(search_res[1])
            search_results3.append(search_res[2])
            search_results4.append(search_res[3])
            search_results5.append(search_res[4])
            search_results6.append(search_res[5])
            search_results7.append(search_res[6])
            search_results8.append(search_res[7])
            search_results9.append(search_res[8])
            search_results10.append(search_res[9])

    df_near_1 = pd.DataFrame(search_results1, columns=[page_num])
    df_near_2 = pd.DataFrame(search_results2, columns=[page_num])
    df_near_3 = pd.DataFrame(search_results3, columns=[page_num])
    df_near_4 = pd.DataFrame(search_results4, columns=[page_num])
    df_near_5 = pd.DataFrame(search_results5, columns=[page_num])
    df_near_6 = pd.DataFrame(search_results6, columns=[page_num])
    df_near_7 = pd.DataFrame(search_results7, columns=[page_num])
    df_near_8 = pd.DataFrame(search_results8, columns=[page_num])
    df_near_9 = pd.DataFrame(search_results9, columns=[page_num])
    df_near_10 = pd.DataFrame(search_results10, columns=[page_num])
    return [df_near_1, df_near_2, df_near_3, df_near_4, df_near_5, df_near_6, df_near_7, df_near_8, df_near_9, df_near_10]


def process_data(fname, data_type, **kwargs):
    with open(fname) as f:
        result = []
        number = 0
        while True:
            rline = f.readline()
            if rline.startswith('HETATM'):
                tmp = rline.split()
                for num, t in enumerate(tmp):
                    if len(t) > 10 and len(t) < 30:
                        ind = t.rfind('-')
                        el1 = t[:ind]
                        el2 = t[ind:]
                        tmp = tmp[:num] + [el1, el2] + tmp[num+1:]
                    elif len(t) > 30:
                        print('x3 -100 error')
                result.append(tmp[1:6])
            elif rline.strip() == 'END':
                number += 1
                npa = np.array(result)
                # ---------------------------------------- OBu and OMe ------------------------------------------
                if data_type in [1, 2]:
                    delta = kwargs.get('delta')
                    params = kwargs.get('params')
                    delta_params = kwargs.get('delta_params')
                    if number == 1:
                        idx_data = np.where(npa[:, 1] == 'O')[0][::2] + 1
                        res_df_angles = pd.DataFrame(idx_data, columns=['idx'])
                        dfs_par = []
                        for i in range(params[1]+1):
                            res_df_par = pd.DataFrame(idx_data, columns=['idx'])
                            dfs_par.append(res_df_par)
                    # ---------- process page --------
                    result_calc = calculate_one_page(npa, number, delta, params, delta_params)
                    res_df_angles = pd.concat([res_df_angles, result_calc[0]], axis=1)
                    for num, i in enumerate(result_calc[1:]):
                        dfs_par[num] = pd.concat([dfs_par[num], i], axis=1)
                    print(f'{number} page calculated')
                # ---------------------------------------- MeOMe -------------------------------------------------
                elif data_type == 3:
                    if number == 1:
                        idx_data = np.where(npa[:, 1] == 'O')[0][:] + 1
                        res_df_angles = pd.DataFrame(idx_data, columns=['idx'])
                        res_df_length = pd.DataFrame(idx_data, columns=['idx'])
                        res_df_par1 = pd.DataFrame(idx_data, columns=['idx'])
                        res_df_par2 = pd.DataFrame(idx_data, columns=['idx'])
                    o1_delta = kwargs.get('o1_deltas')
                    o2_delta = kwargs.get('o2_deltas')
                    o1_params_delta = kwargs.get('o1_params_deltas')
                    o2_params_delta = kwargs.get('o2_params_deltas')
                    result_calc = calculate_one_page_meome(npa, number, o1_delta, o2_delta,
                                                           o1_params_delta, o2_params_delta)
                    res_df_angles = pd.concat([res_df_angles, result_calc[0]], axis=1)
                    res_df_length = pd.concat([res_df_length, result_calc[1]], axis=1)
                    res_df_par1 = pd.concat([res_df_par1, result_calc[2]], axis=1)
                    res_df_par2 = pd.concat([res_df_par2, result_calc[3]], axis=1)
                    print(f'{number} page calculated')
                # ---------------------------------------- Nears -------------------------------------------------
                elif data_type in [4, 5, 6]:
                    if number == 1:
                        idx_data = np.where(npa[:, 1] == 'O')[0][:] + 1
                        res_df_nears1 = pd.DataFrame(idx_data, columns=['idx'])
                        res_df_nears2 = pd.DataFrame(idx_data, columns=['idx'])
                        res_df_nears3 = pd.DataFrame(idx_data, columns=['idx'])
                        res_df_nears4 = pd.DataFrame(idx_data, columns=['idx'])
                        res_df_nears5 = pd.DataFrame(idx_data, columns=['idx'])
                        res_df_nears6 = pd.DataFrame(idx_data, columns=['idx'])
                        res_df_nears7 = pd.DataFrame(idx_data, columns=['idx'])
                        res_df_nears8 = pd.DataFrame(idx_data, columns=['idx'])
                        res_df_nears9 = pd.DataFrame(idx_data, columns=['idx'])
                        res_df_nears10 = pd.DataFrame(idx_data, columns=['idx'])
                    delta = kwargs.get('deltas')
                    result_calc = search_near_page(npa, number, delta)
                    res_df_nears1 = pd.concat([res_df_nears1, result_calc[0]], axis=1)
                    res_df_nears2 = pd.concat([res_df_nears2, result_calc[1]], axis=1)
                    res_df_nears3 = pd.concat([res_df_nears3, result_calc[2]], axis=1)
                    res_df_nears4 = pd.concat([res_df_nears4, result_calc[3]], axis=1)
                    res_df_nears5 = pd.concat([res_df_nears5, result_calc[4]], axis=1)
                    res_df_nears6 = pd.concat([res_df_nears6, result_calc[5]], axis=1)
                    res_df_nears7 = pd.concat([res_df_nears7, result_calc[6]], axis=1)
                    res_df_nears8 = pd.concat([res_df_nears8, result_calc[7]], axis=1)
                    res_df_nears9 = pd.concat([res_df_nears9, result_calc[8]], axis=1)
                    res_df_nears10 = pd.concat([res_df_nears10, result_calc[9]], axis=1)
                    print(f'{number} page searched')
                # -----------------------------------------------------------------------------------------
                result.clear()
                del npa
                # --- This is for exit on selected page -------
                # break
                # if number == 30:
                #     break
            elif rline == '':
                break
    if data_type in [1, 2]:
        return res_df_angles, dfs_par
    elif data_type == 3:
        return [res_df_angles, res_df_length, res_df_par1, res_df_par2]
    elif data_type in [4, 5, 6]:
        return [res_df_nears1, res_df_nears2, res_df_nears3, res_df_nears4, res_df_nears5, res_df_nears6, res_df_nears7,
                res_df_nears8, res_df_nears9, res_df_nears10]


def process_obu_or_ome(filename, data_type, extra_params):
    # Здесь задаются отступы для Bu, Me и для рассчитываемых параметров
    # ------- for Bu ----------------------
    if data_type == 1:
        # 7 - отступ от первой О до атома, который будет вторым концом ее вектора
        # -9 - отступ от следущей О до атома, который будет вторым концом ее вектора
        # соответственно между ними будет считаться угол
        # По аналогии:
        # 4 - отступ от третей О до атома, который будет вторым концом ее вектора
        # -6 - отступ от следущей О до атома, который будет вторым концом ее вектора
        # соответственно между ними будет считаться угол
        deltas = [7, -9, 4, -6]
        if not extra_params:
            parameters = ['length', 2]
            # 42 - отступ от первой О до атома, до которого нужно посчитать расстояние (параметр 1)
            # 38 - отступ от первой О до атома, до которого нужно посчитать расстояние (параметр 2)
            deltas_params = [42, 38, 24, 21]
        else:
            # здесь просто в правильном порядке встроятся дополнительные параметры
            parameters = ['length', 2+extra_params[0]]
            deltas_params = [42, 38] + extra_params[1:extra_params[0]+1] + [24, 21] + extra_params[extra_params[0]+1:]
    # ------- for Me ----------------------
    if data_type == 2:
        if not extra_params:
            # 7 - отступ от первой О до атома, который будет вторым концом ее вектора
            # -9 - отступ от следущей О до атома, который будет вторым концом ее вектора
            # соответственно между ними будет считаться угол
            # По аналогии:
            # 1 - отступ от третей О до атома, который будет вторым концом ее вектора
            # -3 - отступ от следущей О до атома, который будет вторым концом ее вектора
            # соответственно между ними будет считаться угол
            deltas = [7, -9, 1, -3]
            parameters = ['length', 0]
            deltas_params = []
        else:
            deltas = [7, -9, 1, -3]
            parameters = ['length', extra_params[0]]
            deltas_params = extra_params[1:]
    # ------------------------------------------------------

    # --------- Проверка параметров ------------------------
    if len(deltas) != 4:
        print('Must be 4 main deltas for calculating angles (example for Bu: 7 -9 4 -6:\n7 and -9 - first O deltas\n'
              '4 and -6 - third O deltas)')
        exit(0)
    if len(deltas_params) != parameters[1] * 2:
        print(f'Must be {parameters[1] * 2} parameters deltas for calculating {parameters[1]} parameters'
              f' (example for 2 params: 42 38 24 21\n42 - first O first param delta\n38 - first O second param delta\n'
              f'24 - third O first param delta\n21 - third O second param delta)')
        exit(0)
    # ----------------------------------------------------------
    try:
        process_results = process_data(filename, data_type, delta=deltas, params=parameters, delta_params=deltas_params)
    except Exception:
        print('Error while calculating data...\nCheck input parameters,'
              ' maybe extra parameters deltas gives out of range')
        exit(0)

    print('Writing to excel...')
    try:
        process_results[0].to_excel(filename[:-4] + '_angle.xlsx')
        process_results[1][0].to_excel(filename[:-4] + '_length.xlsx')
        for num, i in enumerate(process_results[1][1:]):
            i.to_excel(filename[:-4] + f'_par{num}.xlsx')
    except Exception:
        print('Error while writing to excel...\nTry again')
        exit(0)
    print(f'Angles, length and {len(process_results[1])-1} params written to excel')


def process_meome(filename, data_type):
    # Здесь задаются отступы для MeOMe и для рассчитываемых параметров
    # 80 - отступ от первой О до атома, до которого ищется расстояние
    # [-8, -15, -14] - отступы для нахождения углов:
    # -8 - отступ для первой О, будет вторым концом для вектора, начало которого в О
    # -15, -14 - начало и конец второго вектора, соответственно между этими векторами будет считаться угол
    # [-8, -10, -14] - аналогично для рассчета второго угла
    # -8 - отступ для первой О, будет вторым концом для вектора, начало которого в О
    # -10, -14 - начало и конец второго вектора, соответственно между этими векторами будет считаться угол
    o1_deltas = [80, [-8, -15, -14], [-8, -10, -14]]
    # по аналогии с о1_deltas
    o2_deltas = [68, [-3, -13, -10], [-3, -16, -10]]
    # Отступы для рассчета параметров
    # Параметр1
    # 7 - отступ от О для атома, который будет началом вектора
    # -5 - отступ для атома, который будет концом вектора
    # Параметр 2
    # 7 - отступ от О для атома, который будет началом вектора
    # -7 - отступ от О для атома, который будет концом вектора
    # Также задаются отступы для второй О
    o1_params_deltas = [7, -5, 7, -7]
    o2_params_deltas = [1, -12, 1, -28]

    try:
        process_results = process_data(filename, data_type, o1_deltas=o1_deltas, o2_deltas=o2_deltas,
                                       o1_params_deltas=o1_params_deltas, o2_params_deltas=o2_params_deltas)
    except Exception:
        print('Error while calculating data...\nCheck input parameters')
        exit(0)

    print('Writing to excel...')
    try:
        process_results[0].to_excel(filename[:-4] + '_angle.xlsx')
        process_results[1].to_excel(filename[:-4] + '_length.xlsx')
        process_results[2].to_excel(filename[:-4] + '_par1.xlsx')
        process_results[3].to_excel(filename[:-4] + '_par2.xlsx')
    except Exception:
        print('Error while writing to excel...\nTry again')
        exit(0)
    print(f'Angles, length and 2 params written to excel')


def process_near(filename, data_type):
    # Здесь задаются отступы для Bu, Me и MeOMe. Пример формирования в файле near.txt
    # каждый внутренний список задается отступы для исключения атомов С для соответствующих О (от О-1 до О-4)
    bu_deltas = [[-14, -8, 7, 13], [-15, -9, 7, 12], [-14, -6, 4, 10], [-12, -6, 1, 4]]
    me_deltas = [[-8, -14, 7, 13], [-15, -9, 7], [-14, -6, 1, 4], [-6, -3, 1]]
    # Т.к. в МеОМе всего 2 О дублируем О-1 в О-3, а О-2 в О-4
    meome_deltas = [[-8, -14, 7], [-10, -3, 1], [-8, -14, 7], [-10, -3, 1]]
    if data_type == 4:
        deltas = bu_deltas
    if data_type == 5:
        deltas = me_deltas
    if data_type == 6:
        deltas = meome_deltas

    try:
        res = process_data(filename, data_type, deltas=deltas)
    except Exception:
        print('Error while calculating data...\nCheck input parameters')
        exit(0)

    print('Writing to excel...')
    try:
        for num, i in enumerate(res):
            if num < 5:
                i.to_excel(filename[:-4] + f'_near_id_{num+1}.xlsx')
            else:
                i.to_excel(filename[:-4] + f'_near_len_{num - 4}.xlsx')
    except Exception:
        print('Error while writing to excel...\nTry again')
        exit(0)
    print('Writing done')


if __name__ == '__main__':
    # Есть три основные функции: process_obu_or_ome, process_meome и process_near, в начале каждой из них задаются
    # отступы для рассчета длин, углов и доп. параметров
    start_time = time.time()

    filename = input('Введите название файла:\n')
    while not os.path.exists(filename):
        filename = input('Введите название файла:\n')

    data_type = input('Выберите тип данных:\n1 - OBu, 2 - OMe, 3 - MeOMe, '
                          '4 - Bu_near, 5 - Me_near, 6 - MeOMe_near\n')
    while data_type not in ['1', '2', '3', '4', '5', '6']:
        data_type = input('Выберите тип данных:\n1 - OBu, 2 - OMe, 3 - MeOMe, '
                          '4 - Bu_near, 5 - Me_near, 6 - MeOMe_near\n')
    data_type = int(data_type)

    if data_type in [1, 2]:
        extra = input('Рассчитать дополнительные параметры?\n1 - да, 0 - нет\n')
        while extra not in ['0', '1']:
            extra = input('Рассчитать дополнительные параметры?\n1 - да, 0 - нет\n')
        if extra == '1':
            extra_params = input('Введите количество параметров и отступы для них в формате:\n'
                                 '<кол-во> <отступ_параметр_1_для_О1>  <отступ_параметр_2_для_О1>'
                                 ' <отступ_параметр_1_для_О_3>  <отступ_параметр_2_для_О_3> и так далее\n'
                                 '(пример ввода для 2 параметров:2 -11 22 -33 44\n'
                                 '-11 - отступ для первого параметра первого О\n'
                                 ' 22 - отступ для второго параметра первого О\n'
                                 '-33 - отступ для первого параметра третьего О\n'
                                 ' 44 - отступ для второго параметра третьего О)\n')
            extra_params = [int(i) for i in extra_params.split()]
        else:
            extra_params = None
        process_obu_or_ome(filename, data_type, extra_params)
    elif data_type == 3:
        process_meome(filename, data_type)
    elif data_type in [4, 5, 6]:
        process_near(filename, data_type)
    print(f'{time.time() - start_time} seconds')
    input("Press Enter to exit...")
