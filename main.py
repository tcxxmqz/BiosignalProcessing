from biodatacut import *
import matplotlib.pyplot as plt
from edaprossing import *


def eda_signal_cut_and_save(filepath, subject, exp_time, start_time, channel=2, show=True):
    """
    切分皮电数据，输入文件路径，第几位受试者，第几次实验，实验开始截取数据的时间点，数据所在的通道；自动保存切分后的文件到输入文件所在的路径

    :param filepath: 原始文件路径
    :param subject: 受试者位次
    :param exp_time: 实验位次
    :param start_time: 开始切分时间点
    :param channel: eda信号所在通道
    :return: 分段后的信号
    """
    exp = [60, 40, 34, 30]

    # filepath = r"C:\PythonFiles\BiosignalProcessing\data\exper1.mat"

    saveasfilename = filepath[:-4] + "_" + str(subject) + "_" + str(exp_time) + "_eda.txt"

    stop_time = start_time + exp[exp_time - 1]

    eda_signal = biosignal_cut(filepath, start_time, stop_time, channel=channel, save_filepath=saveasfilename)

    if show is True:
        plt.plot(eda_signal)
        plt.show()

    return eda_signal, saveasfilename


if __name__ == "__main__":
    filepath = r"D:\11.21实验\1\Untitled1.mat"
    eda, saveasfilename = eda_signal_cut_and_save(filepath, 1, 1, 778)
    eda_prossing(eda, saveasfilename)

    # eda_signal_cut_and_save(filepath, 1, 1, 778)
    # eda_signal_cut_and_save(filepath, 1, 2, 924)
    # eda_signal_cut_and_save(filepath, 1, 3, 1019)
    # eda_signal_cut_and_save(filepath, 1, 4, 1189)

    # eda_signal_cut_and_save(filepath, 2, 1, 388)
    # eda_signal_cut_and_save(filepath, 2, 2, 579)
    # eda_signal_cut_and_save(filepath, 2, 3, 823)
    # eda_signal_cut_and_save(filepath, 2, 4, 901)

    # eda_signal_cut_and_save(filepath, 3, 1, 578)
    # eda_signal_cut_and_save(filepath, 3, 2, 714)
    # eda_signal_cut_and_save(filepath, 3, 3, 876)
    # eda_signal_cut_and_save(filepath, 3, 4, 989)

    # eda_signal_cut_and_save(filepath, 4, 1, 283)
    # eda_signal_cut_and_save(filepath, 4, 2, 475)
    # eda_signal_cut_and_save(filepath, 4, 3, 630)
    # eda_signal_cut_and_save(filepath, 4, 4, 739)

    # eda_signal_cut_and_save(filepath, 5, 1, 447)
    # eda_signal_cut_and_save(filepath, 5, 2, 483)
    # eda_signal_cut_and_save(filepath, 5, 3, 623)
    # eda_signal_cut_and_save(filepath, 5, 4, 712)
