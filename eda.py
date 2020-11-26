import neurokit2 as nk
from biosppy.plotting import *


def eda_prossing(raw_signal, path=None):
    """
    皮电信号处理，输入未处理的皮电信号，输出scr监测后的图像。

    :param raw_signal: 未处理的皮电信号
    :param path: 文件保存的地址
    :return: 无
    """

    # 降采样
    downsize_rate = 100
    down_size = 2000 / downsize_rate
    # raw_signal = np.loadtxt(filepath)
    raw_signal = raw_signal[::int(down_size)]
    sampling_rate = int(2000 / down_size)
    # plt.plot(raw_signal)
    # plt.show()

    # 带通滤波与平滑处理
    eda_cleaned = nk.eda_clean(raw_signal, sampling_rate=sampling_rate, method="biosppy")

    # 相位成分提取
    # eda = nk.eda_phasic(eda_cleaned, sampling_rate=sampling_rate, method='median')
    # eda_phasic = eda["EDA_Phasic"].values
    # plt.plot(eda_phasic)
    # plt.show()

    # 微分与卷积处理
    info = nk.eda_findpeaks(eda_cleaned, sampling_rate=sampling_rate, method="qz")
    features = [info["SCR_Onsets"], info["SCR_Offsets"], info['SCR_Peaks'], info['eda_phasic_diffandsmoothed']]

    # 时间轴
    length = len(eda_cleaned)
    T = (length - 1) / sampling_rate
    ts = np.linspace(0, T, length, endpoint=True)

    # 绘图
    # bplt.plot_eda_qz(ts=ts, raw=raw_signal, filtered=eda_cleaned, onsets=features[0],
    #                  offsets=features[1], peaks=features[2], eda_phasic_diffandsmoothed=features[3], show=True,
    #                  path=filepath, stimulus=False)

    # 保存文件名

    # scr监测与绘图输出保存
    if path is not None:
        plot_scr(ts=ts, filtered=eda_cleaned, onsets=features[0], offsets=features[1], show=True, path=path)
    else:
        plot_scr(ts=ts, filtered=eda_cleaned, onsets=features[0], offsets=features[1], show=True)
