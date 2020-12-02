import neurokit2 as nk
from tools.biodatacut import *
from numpy.core.multiarray import ndarray
from biosppy.plotting import *
import pandas as pd


def fnirs_signal_cut_and_save(file_path, subject, exp_time, start_time, show_CHx: str = None):
    """
    输入脑血流文件路径，返回剪切后的所有通道信号并保存，返回值类型是pandas的Dataframe表格，同时返回保存文件的路径。

    :param file_path:
    :param subject:
    :param exp_time:
    :param start_time:
    :param show_CHx:
    :return:
    """

    exp = [60, 40, 34, 30]

    save_as_filename: str = file_path[:-5] + "_" + str(subject) + "_" + str(exp_time) + "_fnirs.csv"

    stop_time = start_time + exp[exp_time - 1]

    fnirs_signal = biosignal_cut(file_path, start_time, stop_time, sampling_rate=5, channel="all",
                                 save_filepath=save_as_filename)

    if show_CHx is not None:

        if show_CHx == "all":
            sampling_rate = 5
            length = len(fnirs_signal.CH4)
            T = (length - 1) / sampling_rate
            ts = np.linspace(0, T, length, endpoint=True)
            fnirs_allCHx_plot(ts=ts, fnirs_signal=fnirs_signal, show=True)
        else:
            sampling_rate = 5
            length = len(fnirs_signal[show_CHx])
            T = (length - 1) / sampling_rate
            ts = np.linspace(0, T, length, endpoint=True)
            fnirs_CHx_plot(ts=ts, CHx_signal=fnirs_signal[show_CHx].astype('float32'), CH=show_CHx, show=True)

    return fnirs_signal, save_as_filename


def fnirs_CHx_process(raw_signal, CH: str, path=None, show=False):
    if CH == "all":
        CHx = ["CH4", "CH5", "CH6", "CH7", "CH8", "CH9", "CH10", "CH11", "CH12",
               "CH13", "CH14", "CH15", "CH16", "CH17", "CH18", "CH19"]
        cleaned_signal = pd.DataFrame()
        for ch in CHx:
            cleaned_signal[ch] = nk.signal_filter(raw_signal[ch].astype("float32"), sampling_rate=5, lowcut=0.02,
                                                  highcut=0.1, method="butterworth")

        sampling_rate = 5
        length = len(cleaned_signal["CH4"])
        T = (length - 1) / sampling_rate
        ts = np.linspace(0, T, length, endpoint=True)

        file_path = path[:-4] + "_all"

        fnirs_allCHx_plot(ts=ts, fnirs_signal=cleaned_signal, path=file_path, show=show)

    elif CH in ['CH5', 'CH8', 'CH11', 'CH14', 'CH17', 'CH4', 'CH7', 'CH10',
                'CH13', 'CH16', 'CH19', 'CH6', 'CH9', 'CH12', 'CH15', 'CH18']:
        CHx_signal_cleaned = nk.signal_filter(raw_signal[CH].astype("float32"), sampling_rate=5, lowcut=0.02, highcut=0.1,
                                              method="butterworth")

        sampling_rate = 5
        length = len(CHx_signal_cleaned)
        T = (length - 1) / sampling_rate
        ts = np.linspace(0, T, length, endpoint=True)

        file_path = path[:-4] + CH

        fnirs_CHx_plot(ts=ts, CHx_signal=CHx_signal_cleaned, CH=CH, path=file_path, show=show)
    else:
        print("fnirs_CHx_process()->请输入CH参数！！")


def fnirs_CHx_plot(ts: ndarray = None, CHx_signal: ndarray = None, CH: str = None,
                   path: str = None, show: bool = True):
    if CH is None:
        print("请输入处理通道CHx到函数fnirs_CHx_plot()!!")

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig = plt.figure()

    if path is not None:
        fig.suptitle('第' + CH + '通道大脑血红蛋白浓度\n' + path)
    else:
        fig.suptitle('第' + CH + '通道大脑血红蛋白浓度')

    ax1 = plt.subplot(311)
    ax1.plot(ts, CHx_signal, label='Total Hb')

    # 设置x, y轴刻度显示范围
    plt.xlim(-1, 60)

    # 设置x轴刻度
    xmjorLocator = MultipleLocator(2)
    ax1.xaxis.set_major_locator(xmjorLocator)

    ax1.tick_params(labelsize=8)

    ax1.set_xlabel('Time(s)')
    ax1.set_ylabel('m(mol/l)*mm')
    ax1.legend(loc='upper right', fontsize=5)
    ax1.grid()

    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '.png'

        fig.savefig(path, dpi=300, bbox_inches='tight')
        print("fnirs_CHx_plot()处理后的图像已经保存到文件路径{}".format(path))

    # show
    if show:
        plt.show()
    else:
        # close
        plt.close(fig)


def fnirs_allCHx_plot(ts: ndarray = None, fnirs_signal=None, path: str = None, show: bool = True):
    CH = ['CH5', 'CH8', 'CH11', 'CH14', 'CH17', 'CH4', 'CH7', 'CH10',
          'CH13', 'CH16', 'CH19', 'CH6', 'CH9', 'CH12', 'CH15', 'CH18']

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig, ax = plt.subplots(3, 6)
    fig.set_size_inches(12, 8)

    if path is not None:
        fig.suptitle('大脑血红蛋白浓度\n' + path)
    else:
        fig.suptitle('大脑血红蛋白浓度')

    for i in range(5):
        ax[0, i].set_title(CH[i], fontsize=7)
        ax[0, i].tick_params(labelsize=4)
        ax[0, i].plot(ts, fnirs_signal[CH[i]].astype('float32'), label='Total Hb')
        ax[0, i].legend(loc='upper right', fontsize=4)

    for i in range(6):
        ax[1, i].set_title(CH[i + 5], fontsize=7)
        ax[1, i].tick_params(labelsize=4)
        ax[1, i].plot(ts, fnirs_signal[CH[i + 5]].astype('float32'), label='Total Hb')
        ax[1, i].legend(loc='upper right', fontsize=4)

    for i in range(1, 6):
        ax[2, i].set_title(CH[i + 10], fontsize=7)
        ax[2, i].tick_params(labelsize=4)
        ax[2, i].plot(ts, fnirs_signal[CH[i + 10]].astype('float32'), label='Total Hb')
        ax[2, i].legend(loc='upper right', fontsize=4)

    ax[0, 5].tick_params(labelsize=0)
    ax[2, 0].tick_params(labelsize=0)

    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '.png'

        fig.savefig(path, dpi=300)
        print("fnirs_allCHx_plot()处理后的图像已经保存到文件路径{}".format(path))

    # show
    if show:
        plt.show()
    else:
        # close
        plt.close(fig)
