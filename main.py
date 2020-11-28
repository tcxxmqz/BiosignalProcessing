from eda import *
from ecg import *


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

    for k in range(5):
        for i in range(4):
            file = filepath[k]
            # EDA处理
            # eda, eda_saveasfilename = eda_signal_cut_and_save(file, k+1, i+1, cut_time[k][i], show=False)
            # eda_process(eda, i+1, eda_saveasfilename)
            # ECG处理
            ecg, ecg_saveasfilename = ecg_signal_cut_and_save(file, k+1, i+1, cut_time[k][i], show=False)
            ecg_process(ecg, i+1, ecg_saveasfilename)
