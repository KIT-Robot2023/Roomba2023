#include <iostream>
#include <fstream>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <chrono>
#include <thread>

class CsvLogger {
public:
    CsvLogger(const std::string& filename) : filename_(filename) {
        // ヘッダを書き込む
        outputFile_.open(filename_, std::ios::out | std::ios::app);
        if (outputFile_.is_open()) {
            outputFile_ << "Timestamp,Data1,Data2,Data3\n";
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
        // 現在の日時を取得
        auto currentTime = std::chrono::system_clock::now();
        std::time_t now = std::chrono::system_clock::to_time_t(currentTime);

        // 日時とデータをCSVファイルに書き込む
        std::tm* localTime = std::localtime(&now);
        std::stringstream ss;
        ss << std::put_time(localTime, "%Y-%m-%d %H:%M:%S");
        std::string timestamp = ss.str();

        // ファイルにデータを書き込む
        outputFile_.open(filename_, std::ios::out | std::ios::app);
        if (outputFile_.is_open()) {
            outputFile_ << timestamp << "," << data1 << "," << data2 << "," << data3 << "\n";
            outputFile_.close();
        } else {
            std::cerr << "ファイルへの書き込みに失敗しました" << std::endl;
        }
    }

private:
    std::string filename_;
    std::ofstream outputFile_;
};