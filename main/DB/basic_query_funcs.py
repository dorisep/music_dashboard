def query_artist(artist):
    command = (f"select * from albums where artist = '{artist}'")
    return command

# func for artist queries
def query_year(year):
    command = (f"select * from albums where album_year = '{year}'")
    return command

# func for artist queries
def query_genre(genre):
    command = (f"select * from albums where album_genre = '{genre}'")
    return command

queries_dict = {
    "ar_query": query_artist,
    "yr_query": query_year,
    "ge_query": query_genre
    }