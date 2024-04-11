import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def calculate_and_plot_correlation(file_path, reference_col_index, savefig_path):
    print("calculate and plot the pearson correlation...")
    # 讀取CSV文件到DataFrame
    data = pd.read_csv(file_path, encoding='utf-8')
    
    print("Drop NaN row")
    data = data.dropna()
    print("Drop NaN Data",data.head())

    # 選擇作為參考列的列
    reference_column = data.iloc[:, reference_col_index].astype(int)
    print("The reference column is :" ,data.columns[reference_col_index])


    #轉換HomePlanet
    dummies = pd.get_dummies(data["HomePlanet"]).astype(int)
    data_with_dummies = pd.concat([data, dummies], axis = 1)
    print(data_with_dummies)


    # 將布林值列轉換為整數
    bool_columns = ['CryoSleep', 'VIP', 'Transported']  # 需要轉換的布林列表
    for col in bool_columns:
        if col in data.columns:
            data_with_dummies[col] = data_with_dummies[col].astype(int)

    print("Finished Data",data.head())

    # 計算其他列相對於參考列的Pearson相關性
    correlations = []
    columns_checked = []
    for column in data_with_dummies.columns:
        if column != data_with_dummies.columns[reference_col_index] and data_with_dummies[column].dtype in ['float64', 'int64', 'int32']:
            columns_checked.append(column)
            current_column = data_with_dummies[column].astype(float)  # 確保列是數值類型
            correlation = reference_column.corr(current_column)
            correlations.append(correlation)

    # 設置Pandas顯示選項，以顯示所有行
    pd.set_option('display.max_rows', None)

    # 將結果轉換為DataFrame
    correlation_data = pd.DataFrame({'Column': columns_checked, 'Correlation': correlations})

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Correlation', y='Column', data=correlation_data, palette='viridis')
    reference_col_name = data.columns[reference_col_index]
    plt.title('Pearson Correlation with Reference Column => {}'.format(reference_col_name))
    plt.xlabel('Pearson Correlation Coefficient')
    plt.ylabel('Column Name')
    plt.savefig(savefig_path)
    plt.show()

calculate_and_plot_correlation(r'C:\Users\alana\Dropbox\Datamining_class\train.csv', 13, r'C:\Users\alana\Dropbox\Datamining_class\result.png')
