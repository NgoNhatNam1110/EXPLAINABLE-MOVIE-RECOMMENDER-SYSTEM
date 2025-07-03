import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.model_selection import train_test_split

# Bước 1. Đọc dữ liệu từ các file của 2 Dataset MOVIELENS và TMDB
users = pd.read_csv('users.dat', sep='::', engine='python',
    names=['UserID','Gender','Age','Occupation','Zip-code'], encoding='latin-1')
movies = pd.read_csv('movies.dat', sep='::', engine='python',
    names=['MovieID','Title','Genres'], encoding='latin-1')
ratings = pd.read_csv('ratings.dat', sep='::', engine='python',
    names=['UserID','MovieID','Rating','Timestamp'], encoding='latin-1')
tmdb_movies = pd.read_csv('tmdb_5000_movies.csv')
tmdb_credits = pd.read_csv('tmdb_5000_credits.csv')


# Bước 2. Lọc USER và MOVIE có ít nhất 20 ratings
ratings = ratings.drop_duplicates()
movie_counts = ratings['MovieID'].value_counts()
user_counts = ratings['UserID'].value_counts()

ratings_before = ratings.copy()
# Lọc ra các movie và user có ít nhất 20 ratings
ratings = ratings[ratings['MovieID'].isin(movie_counts[movie_counts >= 20].index)]
ratings = ratings[ratings['UserID'].isin(user_counts[user_counts >= 20].index)]
# Lưu lại các movie và user bị loại
filtered_out = ratings_before.loc[~ratings_before.index.isin(ratings.index)]
# Ghi DataFrame RATING (sau khi lọc) vào file CSV mới
ratings.to_csv('filtered_ratings.csv', index=False)

# Ghi DataFrame FILTERED_OUT (các rating đã bị lọc) vào file CSV mới
filtered_out.to_csv('removed_ratings.csv', index=False)

# Bước 3. Chuẩn hóa TITLE và YEAR
def extract_title_year(title):
    match = re.match(r"^(.*?)[\s]*\((\d{4})\)$", title)
    if match:
        return match.group(1).strip(), int(match.group(2))
    else:
        return title, np.nan
movies[['Title_clean', 'Year']] = movies['Title'].apply(
    lambda x: pd.Series(extract_title_year(x.lower().strip()))
)
# Chuẩn hóa tiêu đề
tmdb_movies['title_clean'] = tmdb_movies['title'].str.lower().str.strip()
# Chuẩn hóa năm phát hành
tmdb_movies['release_year'] = pd.to_datetime(tmdb_movies['release_date'], errors='coerce').dt.year 


# Bước 4. Chuẩn hóa GENRES tách thành list
def split_genres(genre_str):
    if isinstance(genre_str, str):
        return [g.strip().lower() for g in genre_str.split('|')]
    else:
        return []
movies['Genres'] = movies['Genres'].apply(split_genres)

# Bước 5. Ghép METADATA TMDB vào MOVIELENS (theo TITLE_CLEAN(sau khi chuẩn hóa)) & YEAR)
def get_tmdb_metadata(row):
    year = row['Year']
    title = row['Title_clean']
    matched = tmdb_movies[
        (tmdb_movies['release_year'] == year) & (tmdb_movies['title_clean'] == title)
    ]
    if matched.shape[0]:
        return {
            'popularity': matched.iloc[0]['popularity'],
            'vote_average': matched.iloc[0]['vote_average'],
            'runtime': matched.iloc[0]['runtime']
        }
    else:
        return None

movies['tmdb_matched'] = movies.apply(get_tmdb_metadata, axis=1)

# Bước 6. Gộp RATINGS + Movies đã có metadata + users thành bảng FINAL

data = ratings.merge(movies, on='MovieID', how='inner')
data = data.merge(users, on='UserID', how='inner')


# Bước 7. One-hot encoding cột Genres trên bảng DATA



# test

print(data.shape[0])
# print(data.head(10))
