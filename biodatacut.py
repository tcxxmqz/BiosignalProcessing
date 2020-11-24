from scipy.io import loadmat
import numpy as np


def biosignal_cut(read_mat_file, start_time, stop_time, sampling_rate=2000, channel=0, save_filepath=None):
    """
    信号切分函数，输入原始大段生理信号数据，切分时间段，输出对应信号分段

    :param read_mat_file: biopac导出的mat格式文件路径，注意格式
    :param start_time: 开始切分的时间点，单位秒
    :param stop_time: 停止切分时间点，单位秒
    :param sampling_rate: 数据的采样频率，单位hz
    :param channel: 数据在mat格式文件中的列，一般有三列，从0开始数
    :param save_filepath: 切分后数据保存位置
    :return: array，切分后的数据分段
    """

    # 加载文件
    signal_data = loadmat(read_mat_file)["data"][:, channel]
    # signal_data = loadmat(mat_file)["data"]

    # 起始位置计算
    start_time_cut = start_time * sampling_rate
    stop_time_cut = stop_time * sampling_rate

    # 数据切分
    signal_data_cut = signal_data[start_time_cut: stop_time_cut]

    # 数据保存到文件
    if save_filepath is not None:
        with open(save_filepath, "w+") as file:
            np.savetxt(file, signal_data_cut)
        print("第{}通道中，{}-{}秒数据已经保存到文件路径{}".format(channel, start_time, stop_time, save_filepath))

        return signal_data_cut
