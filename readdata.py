import pandas as pd

# Đường dẫn tới thư mục chứa dataset
path = 'C:/Users/Admin/.cache/kagglehub/datasets/odedgolden/movielens-1m-dataset/versions/1/'
path1 = 'C:/Users/Admin/.cache/kagglehub/datasets/tmdb/tmdb-movie-metadata/versions/1/'
# Đọc dữ liệu từ các file .dat của movielens-1m-dataset
# Sử dụng encoding='latin-1' để tránh lỗi khi đọc file
users = pd.read_csv(path+'users.dat',
    sep='::', engine='python',
    names=['UserID','Gender','Age','Occupation','Zip-code'],
    encoding='latin-1')

movies = pd.read_csv(path+'movies.dat',
    sep='::', engine='python',
    names=['MovieID','Title','Genres'],
    encoding='latin-1')

ratings = pd.read_csv(path+'ratings.dat',
    sep='::', engine='python',
    names=['UserID','MovieID','Rating','Timestamp'],
    encoding='latin-1')

# Đọc dữ liệu từ file tmdb-movie-metadata.csv


print("Users DataFrame:")
print(users.tail(100)) 
