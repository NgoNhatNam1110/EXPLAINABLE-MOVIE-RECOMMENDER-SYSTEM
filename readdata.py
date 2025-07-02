import pandas as pd

# Đường dẫn tới thư mục chứa dataset
path = 'C:/Users/Admin/.cache/kagglehub/datasets/odedgolden/movielens-1m-dataset/versions/1/'
path1 = 'C:/Users/Admin/.cache/kagglehub/datasets/tmdb/tmdb-movie-metadata/versions/2/'
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

ratings_before = ratings.copy()

# Đọc dữ liệu từ file tmdb-movie-metadata.csv
tmdb_movies = pd.read_csv(path1+'tmdb_5000_movies.csv')
tmdb_credits = pd.read_csv(path1+'tmdb_5000_credits.csv')

# Loại bỏ các hàng trùng lặp trong dữ liệu ratings
ratings = ratings.drop_duplicates()

# Đếm số lượng phim và người dùng trong ratings
movie_counts = ratings['MovieID'].value_counts()
user_counts = ratings['UserID'].value_counts()

# Lọc ra các phim và người dùng có ít nhất 20 đánh giá
ratings = ratings[ratings['MovieID'].isin(movie_counts[movie_counts >= 20].index)]
ratings = ratings[ratings['UserID'].isin(user_counts[user_counts >= 20].index)]

#  Tính ra những rating đã bị lọc
filtered_out = ratings_before.loc[~ratings_before.index.isin(ratings.index)]

print(f"Number of filtered out ratings: {filtered_out.shape[0]}")
print(filtered_out['UserID'].nunique())
print(filtered_out['MovieID'].nunique())

# Ghi DataFrame ratings (sau khi lọc) vào file CSV mới
ratings.to_csv('filtered_ratings.csv', index=False)

# Ghi DataFrame filtered_out (các rating đã bị lọc) vào file CSV mới
filtered_out.to_csv('removed_ratings.csv', index=False)
