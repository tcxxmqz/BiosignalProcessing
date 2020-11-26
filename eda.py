from matplotlib.ticker import MultipleLocator
from numpy.core.multiarray import ndarray

import neurokit2 as nk
from biosppy.plotting import *


def plot_eda_qz(ts: ndarray = None,
                raw: ndarray = None,
                filtered: ndarray = None,
                onsets: ndarray = None,
                offsets: ndarray = None,
                peaks: ndarray = None,
                eda_phasic_diffandsmoothed: ndarray = None,
                path: str = None,
                show: bool = False,
                stimulus: bool = False):
    """Create a summary plot from the output of signals.eda.eda.

    Parameters
    ----------
    ts : array
        Signal time axis reference (seconds).
    raw : array
        Raw EDA signal.
    filtered : array
        Filtered EDA signal.
    onsets : array
        Indices of SCR pulse onsets.
    offsets : array
        Indices of SCR pulse offsets.
    peaks : array
        Indices of the SCR peaks.
    eda_phasic_diffandsmoothed : array (modified by qz).
        eda_phasic_diffandsmoothed.
    path : str, optional
        If provided, the plot will be saved to the specified file.
    show : bool, optional
        If True, show the plot immediately.
    stimulus : bool, optional
        If True, show the stimulus.
        绘制预测到的刺激发生时间, 以零点开始的刺激延时作为后续刺激的校准，默认不绘制。
    modified by qz at 2020-10-28

    """

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig = plt.figure()
    fig.suptitle('EDA信号处理及SCR检测\n' + path)

    # raw signal
    ax1 = fig.add_subplot(311)

    # ax1.plot(ts, raw, linewidth=MAJOR_LW, label='raw')
    ax1.plot(ts, raw, label='raw EDA')

    ax1.set_ylabel('Amplitude(uS)')
    ax1.legend(loc="upper left", fontsize=6)
    ax1.grid()

    # 设置x轴刻度
    xmjorLocator = MultipleLocator(1)
    ax1.xaxis.set_major_locator(xmjorLocator)

    # filtered signal with onsets, peaks
    ax2 = fig.add_subplot(312, sharex=ax1)

    ymin = np.min(filtered)
    ymax = np.max(filtered)
    alpha = 0.1 * (ymax - ymin)
    ymax += alpha
    ymin -= alpha

    ax2.plot(ts, filtered, label='EDA-Filtered')

    # 绘制onsets, peaks, offsets点到图像
    ax2.scatter(ts[onsets], filtered[onsets], marker='o', color='b', label='SCR-Onsets')
    # ax2.scatter(ts[peaks], filtered[peaks], marker='^', label='SCR-Peaks')
    ax2.scatter(ts[offsets], filtered[offsets], marker='x', color='green', label='SCR-Offsets')

    # SCR反应区域标记上颜色
    i: int

    for i in range(0, len(ts[onsets]) - 1):
        ax2.axvspan(xmin=ts[onsets][i], xmax=ts[offsets][i], facecolor='gray', alpha=0.4)
    ax2.axvspan(xmin=ts[onsets][-1], xmax=ts[offsets][-1], facecolor='gray', alpha=0.4, label='SCR')

    # 预测刺激开始的时间，用红色竖线表示
    if stimulus:
        stimulus_list = onsets - onsets[0]
        ax2.vlines(ts[stimulus_list], ymin, ymax,
                   color='r',
                   linewidth=MINOR_LW,
                   label='Stimulus')

    ax2.set_ylabel('Amplitude(uS)')
    ax2.legend(loc="upper left", fontsize=6)
    ax2.grid()

    # eda_phasic_diffandsmoothed
    ax3 = fig.add_subplot(313, sharex=ax1)
    ax3.plot(ts[:len(eda_phasic_diffandsmoothed)], eda_phasic_diffandsmoothed, label='EDA-processed')

    # ax3.hlines(0, 0, ts[-1], colors='r', linestyles='dashed')
    ax3.axhline(color='orange', ls='dashed')

    ax3.scatter(ts[onsets], eda_phasic_diffandsmoothed[onsets], marker='o', color='b', label='SCR-Onsets')
    ax3.scatter(ts[peaks], eda_phasic_diffandsmoothed[peaks], marker='^', color='orange', label='SCR-Peaks')
    ax3.scatter(ts[offsets], eda_phasic_diffandsmoothed[offsets], marker='x', color='green', label='SCR-Offsets')

    # SCR反应区域标记上颜色
    for i in range(0, len(ts[onsets]) - 1):
        ax3.axvspan(xmin=ts[onsets][i], xmax=ts[offsets][i], facecolor='gray', alpha=0.4)
    ax3.axvspan(xmin=ts[onsets][-1], xmax=ts[offsets][-1], facecolor='gray', alpha=0.4, label='SCR')

    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Amplitude(uS)')
    ax3.legend(loc="upper left", fontsize=3)
    ax3.grid()

    # make layout tight
    fig.tight_layout()

    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '.png'

        fig.savefig(path, dpi=300, bbox_inches='tight')

    # show
    if show:
        plt.show()
    else:
        # close
        plt.close(fig)


def plot_scr(ts: ndarray = None,
             filtered: ndarray = None,
             onsets: ndarray = None,
             offsets: ndarray = None,
             path: str = None,
             show: bool = False,
             stimulus: object = False):
    """绘制SCR到图像

        Parameters
        ----------
        ts : array
            Signal time axis reference (seconds).
        filtered : array
            Filtered EDA signal.
        onsets : array
            Indices of SCR pulse onsets.
        offsets : array
            Indices of SCR pulse offsets.
        path : str, optional
            If provided, the plot will be saved to the specified file.
        show : bool, optional
            If True, show the plot immediately.
        stimulus : bool, optional
            If True, show the stimulus.
            绘制预测到的刺激发生时间, 以零点开始的刺激延时作为后续刺激的校准，默认不绘制。
        modified by qz at 2020-10-28

        """

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig = plt.figure()
    fig.suptitle('EDA处理及SCR检测\n')

    # filtered signal with onsets, peaks, SCR
    ax1 = fig.add_subplot(311)

    # 给子图设置标题
    ax1.set_title(path)

    # 设置x轴刻度
    xmjorLocator = MultipleLocator(2)
    ax1.xaxis.set_major_locator(xmjorLocator)

    ymin = np.min(filtered)
    ymax = np.max(filtered)
    alpha = 0.1 * (ymax - ymin)
    ymax += alpha
    ymin -= alpha

    ax1.plot(ts, filtered, label='EDA-Filtered')

    # 绘制onsets, offsets点到图像
    ax1.scatter(ts[onsets], filtered[onsets], marker='o', color='b', label='SCR-Onsets')
    ax1.scatter(ts[offsets], filtered[offsets], marker='x', color='green', label='SCR-Offsets')

    # SCR反应区域标记上颜色
    for i in range(0, len(ts[onsets]) - 1):
        ax1.axvspan(xmin=ts[onsets][i], xmax=ts[offsets][i], facecolor='gray', alpha=0.4)
    ax1.axvspan(xmin=ts[onsets][-1], xmax=ts[offsets][-1], facecolor='gray', alpha=0.4, label='SCR')

    # 预测刺激开始的时间，用红色竖线表示
    if stimulus:
        stimulus_list = onsets - onsets[0]
        ax1.vlines(ts[stimulus_list], ymin, ymax,
                   color='r',
                   linewidth=MINOR_LW,
                   label='Stimulus')

    ax1.set_ylabel('Amplitude(uS)')
    ax1.legend(loc="upper left", fontsize=3)
    ax1.grid()

    # make layout tight
    fig.tight_layout()

    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '_scr.png'

        fig.savefig(path, dpi=300, bbox_inches='tight')

    # show
    if show:
        plt.show()
    else:
        # close
        plt.close(fig)


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
