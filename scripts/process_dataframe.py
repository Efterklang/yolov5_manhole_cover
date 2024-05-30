import pandas as pd
import argparse


class CSVFilter:
    def __init__(self, input_file, output_file, labels_to_remove):
        self.input_file = input_file
        self.output_file = output_file
        self.labels_to_remove = labels_to_remove

    def read_csv(self):
        """读取CSV文件到DataFrame"""
        return pd.read_csv(self.input_file)

    def filter_rows(self, df):
        """过滤DataFrame中的行"""
        return df[~df["label"].isin(self.labels_to_remove)]

    def write_csv(self, df):
        """将过滤后的DataFrame写入CSV文件"""
        df.to_csv(self.output_file, index=False)

    def process(self):
        """处理CSV文件的主要流程"""
        df = self.read_csv()
        filtered_df = self.filter_rows(df)
        self.write_csv(filtered_df)


def main():
    parser = argparse.ArgumentParser(
        description="Filter rows from a CSV based on label."
    )
    parser.add_argument("input_file", type=str, help="Input CSV file")
    parser.add_argument("output_file", type=str, help="Output CSV file")
    parser.add_argument("labels", nargs="+", help="List of labels to remove")
    args = parser.parse_args()

    # 创建CSVFilter对象
    filter = CSVFilter(args.input_file, args.output_file, args.labels)

    # 执行处理流程
    filter.process()


if __name__ == "__main__":
    main()
