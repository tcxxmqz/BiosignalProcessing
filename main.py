from tools.eda import *
from tools.ecg import *
from tools.emg import *
from tools.fnirs import *

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
        file = filepath[k]
        for i in range(4):
            # EDA处理
            eda, eda_saveasfilename = eda_signal_cut_and_save(file, k+1, i+1, cut_time[k][i], show=False)
            eda_process(eda, i+1, eda_saveasfilename)
            # ECG处理
            ecg, ecg_saveasfilename = ecg_signal_cut_and_save(file, k+1, i+1, cut_time[k][i], show=False)
            ecg_process(ecg, i+1, ecg_saveasfilename)
            # EMG处理
            emg, emg_saveasfilename = emg_signal_cut_and_save(file, k+1, i+1, cut_time[k][i], show=False)
            emg_process(emg, i+1, emg_saveasfilename)

    fnirs_filepath = [r"C:\Python Files\BiosignalProcessing\data\1\exper1.csv",
                      r"C:\Python Files\BiosignalProcessing\data\2\exper2.csv",
                      r"C:\Python Files\BiosignalProcessing\data\3\exper3.csv",
                      r"C:\Python Files\BiosignalProcessing\data\4\exper4.csv",
                      r"C:\Python Files\BiosignalProcessing\data\5\exper5.csv"]
    fnirs_cut_time = [[447, 596, 724, 859],
                      [26, 166, 269, 347],
                      [218, 353, 515, 627],
                      [147, 340, 494, 567],
                      [38, 75, 213, 304]]
    for k in range(5):
        fnirs_file = fnirs_filepath[k]
        for i in range(4):
            fnirs, fnirs_saveasfilename = fnirs_signal_cut_and_save(fnirs_file, k + 1, i + 1, fnirs_cut_time[k][i],
                                                                    show_CHx="all")
            fnirs_CHx_process(fnirs, "all", fnirs_saveasfilename, show=True)
