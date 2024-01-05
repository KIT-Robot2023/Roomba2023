#include <iostream>
#include <fstream>
#include <sstream>

class CsvLogger {
public:
    CsvLogger(const std::string& filename) : filename_(filename) {
        // ヘッダを書き込む
        outputFile_.open(filename_, std::ios::out | std::ios::app);
        if (outputFile_.is_open()) {
            outputFile_ << "Data1,Data2,Data3\n";
            outputFile_.close();
        } else {
            std::cerr << "ファイルの作成に失敗しました" << std::endl;
        }
    }

    ~CsvLogger() {
        // デストラクタでファイルを閉じる
        if (outputFile_.is_open()) {
            outputFile_.close();
        }
    }

    void logData(double data1, double data2, double data3) {
        std::stringstream ss;

        // ファイルにデータを書き込む
        outputFile_.open(filename_, std::ios::out | std::ios::app);
        if (outputFile_.is_open()) {
            outputFile_ <<  data1 << "," << data2 << "," << data3 << "\n";
            outputFile_.close();
        } else {
            std::cerr << "ファイルへの書き込みに失敗しました" << std::endl;
        }
    }

private:
    std::string filename_;
    std::ofstream outputFile_;
};