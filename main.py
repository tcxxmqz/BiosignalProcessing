from typing import List

from biodatacut import *
from eda import *


def eda_signal_cut_and_save(file_path, subject, exp_time, start_time, channel=2, show=True):
    """
    切分皮电数据，输入文件路径，第几位受试者，第几次实验，实验开始截取数据的时间点，数据所在的通道；自动保存切分后的文件到输入文件所在的路径

    :param file_path: 原始文件路径
    :param subject: 受试者位次
    :param exp_time: 实验位次
    :param start_time: 开始切分时间点
    :param channel: eda信号所在通道
    :param show: 是否绘图
    :return: 分段后的信号
    """
    exp = [60, 40, 34, 30]

    # filepath = r"C:\PythonFiles\BiosignalProcessing\data\exper1.mat"

    save_as_filename = file_path[:-5] + "_" + str(subject) + "_" + str(exp_time) + "_eda.txt"

    stop_time = start_time + exp[exp_time - 1]

    eda_signal = biosignal_cut(file_path, start_time, stop_time, channel=channel, save_filepath=save_as_filename)

    if show is True:
        plt.plot(eda_signal)
        plt.show()

    return eda_signal, save_as_filename


if __name__ == "__main__":
    filepath = [r"C:\Python Files\BiosignalProcessing\data\1\exper1.mat",
                r"C:\Python Files\BiosignalProcessing\data\2\exper2.mat",
                r"C:\Python Files\BiosignalProcessing\data\3\exper3.mat",
                r"C:\Python Files\BiosignalProcessing\data\4\exper4.mat",
                r"C:\Python Files\BiosignalProcessing\data\5\exper5.mat"]
    cut_time = [[778, 924, 1019, 1189],
                [388, 579, 823, 901],
                [578, 714, 879, 989],
                [283, 475, 630, 739],
                [447, 483, 623, 712]]
    # for k in range(5):
    #     for i in range(4):
    #         file = filepath[k]
    #         eda, saveasfilename = eda_signal_cut_and_save(file, k + 1, i + 1, cut_time[k][i])
    #         eda_process(eda, saveasfilename)

file = filepath[0]
eda, saveasfilename = eda_signal_cut_and_save(file, 1, 2, cut_time[0][1])
eda_process(eda, saveasfilename)

