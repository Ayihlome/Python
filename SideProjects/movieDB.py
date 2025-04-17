#! /usr/bin/env python3
import requests
import os
from dotenv import load_dotenv
import argparse


# Load variables from .env into environment
load_dotenv()

# Get the API key from environment
api_key = os.getenv("TMDB_API_KEY")

# Additional information that will be used for each pull request
params = {
    "api_key": api_key,   # inserts API key for auth reasons
    "language": "en-US",
    }
headers = {"accept": "application/json"}  #tells the server to convert response into JSON




def NowPlaying():
    # API request
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    # Display movies 
    print("     \nNow Playing Movies\n" + "-"*50)
    for movie in data["results"]:
        title = movie.get("title", "N/A")
        release_date = movie.get("release_date", "N/A")
        overview = movie.get("overview", "No overview available.")
        vote_average = movie.get("vote_average", "N/A")
        
        print(f"  🎬 {title} ({release_date})")
        print(f"  ⭐ Rating: {vote_average}/10")
        print(f"  📖 Overview: {overview}\n")
        print("-" * 50)


def Popular():
    # API request
    try:
        url= "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
        response =requests.get(url=url, headers=headers, params=params)
        data = response.json()
    except Exception as e:
        print("Error: ", e)
    
    # Display movies
    print( "      \n Popular Movies: \n", "-"*40)
    for movie in data["results"]:
        title = movie.get("title", "N/A")
        rating = movie.get ("vote_average", "N/A")
        popularity = movie.get("popularity", "N/A")
        print(f"  🎬 {title}")
        print(f"  ⭐ Rating: {rating}/10")
        print(f"  📊 Popularity: {popularity}")
        print("-" * 40)


def TopRated():
    try:
        url = 'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=vote_average.desc&without_genres=99,10755&vote_count.gte=200'
        response = requests.get(url=url, headers=headers, params=params)
        data = response.json()
    except Exception as e:
        print("Error: ", e)
    
    rank = 1
    print("    \n Top Rated Movies \n", "-"*40)
    for movie in data['results']:
        title = movie.get("title", "N/A")
        rating = movie.get("vote_average", "N/A")
        overview = movie.get("overview", "N/A")
        print(f"        {rank}")
        print(f"  🎬 {title}")
        print(f"  ⭐ Ratting: {rating}/10 ")
        print(f"  📖 Overview: {overview}")
        print("-"*40)
        rank += 1


def Upcoming():
    try:
        url = 'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_release_type=2|3&release_date.gte={min_date}&release_date.lte={max_date}'
        response = requests.get(url=url, headers=headers, params=params)
        data = response.json()
    except Exception as e:
        print ("Error: ", e)
    
    
    print("    \n Upcoming Movies \n", "-"*40)
    for movie in data['results']:
        title = movie.get("title", "N/A")
        release_data= movie.get("release_date", "N/A")
        overview = movie.get("overview", "N/A")
        print(f"  🎬  {title}")
        print(f"  📅 Release Date: {release_data}")
        print(f"  📖 Overview: {overview}")
        print("-"*40)

# Main function

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for a movie lists.")
    
    # Positional arg (required)
    parser.add_argument("--playing", action="store_true" , help="Lists movies that are currently playing")
    parser.add_argument("--popular", action="store_true" , help="Lists movies that are popular")
    parser.add_argument("--upcoming", action="store_true", help="Lists movies that are yet to release")
    parser.add_argument("--top", action="store_true", help="Lists the top movies")
    # Parse args from command line
    args = parser.parse_args()

    # Call your function with args
    if args.playing:
        NowPlaying()
    elif args.popular:
        Popular()
    elif args.upcoming:
        Upcoming()
    elif args.top:
        TopRated()
    else:
        print("No valid argument passed. Use --help to see options.")


# print("Hii")