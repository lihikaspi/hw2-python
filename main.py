import data
import clustering

def main():
    df = data.load_data('/home/student/hw2/london_sample_500.csv')
    new_df = data.add_new_columns(df)
    data.data_analysis(new_df)

    features = ['hum', 'cnt']
    transformed_data = clustering.transform_data(df, features)

    k_values = [2, 3, 5]
    for k in k_values:
        kmeans_result = clustering.kmeans(transformed_data, k)
        clustering.visualize_results(transformed_data, kmeans_result[0], kmeans_result[1], 'plots.pdf')

if __name__ == '__main__':
    main()