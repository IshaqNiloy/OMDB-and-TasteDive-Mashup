
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

import requests_with_caching
import sys
sys.setExecutionLimit(35000)

def get_movies_from_tastedive(name):
    baseurl = "https://tastedive.com/api/similar"
    params_diction = {}
    params_diction["q"] = name
    params_diction["type"] = "movies"
    params_diction["limit"] = 5
    response_object = requests_with_caching.get(baseurl, params = params_diction)
    #print(response_object.url)
    return response_object.json()

def extract_movie_titles(py_d):
    movie_title_list = []
    movie_title_list = [d["Name"] for d in py_d['Similar']["Results"]]
    #print(movie_title_list)
    return movie_title_list

def get_related_titles(movie_title_list):
    related_movie_titles_list = []
    for movie in movie_title_list:
        related_movie_titles_list += extract_movie_titles(get_movies_from_tastedive(movie))
        
    related_movie_titles_list = list(set(related_movie_titles_list))#To remove the duplicate ones
    
    return related_movie_titles_list

def get_movie_data(movie_title):
    baseurl = "http://www.omdbapi.com/"
    param_diction = {}
    param_diction["t"] = movie_title
    param_diction["r"] = "json"
    
    response_object = requests_with_caching.get(baseurl, params = param_diction)
    
    return response_object.json()

def get_movie_rating(py_d):
    rotten_tomato_ratings = 0
    
    for dic in py_d["Ratings"]:
        if dic["Source"] == "Rotten Tomatoes":
            rotten_tomato_ratings = int(dic["Value"][:-1])
            break;
            
    return rotten_tomato_ratings

def get_sorted_recommendations(movie_title_list):
    sorted_movies_titles = sorted(get_related_titles(movie_title_list), key = lambda value : get_movie_rating(get_movie_data(value)), reverse = True)
    #print(sorted_movies_titles)
    return sorted_movies_titles

get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

