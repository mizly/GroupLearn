import math

# I have no clue how the logged in user works, so I'll just assume it's also a dictionary
user_dict = {}

# dictionary of profiles is profile_dict with   "profile":profile   pair
profile_dict = {}

# a copy is made to make changes on it separately
match_dict = profile_dict.copy()

# dictionary of a person's attributes (no specific person) is a_dict with   user:int/str attribute   pair
a_dict = {}

# program prioritizes the right grade over the right time, though of course it will fall back to the right time if none for the right grade exist
user_score = {}

def sort_compabitility():
    for key in match_dict: #parses through all the profiles
        if dif := abs( user_dict["grade"] - match_dict[key]["grade"] ) > 2: #match_dict[key]["grade"] should be analogous to the person's a_dict["grade"]
            match_dict.pop(key) #removes people who are more than 2 grades apart
            continue
            
        user_score[key] = 10*dif #assigns score to profile based on grade difference; the lower the better
        
        has_subject = False #measures whether the profile shares subjects with the user

        for i in user_dict["subjects"]: #should be parsing through subjects array of user
            try:
                match_dict[key]["subjects"].index(i) #we do a little try-catching
                has_subject = True
            except:
                pass #.index() returns ValueError if not found, meaning it skips the has_subject = True part
        
        if not(has_subject):
            match_dict.pop(key) #removes the people who don't share a subject
            continue

        #time to worry about timing!
        #it's just the same code as the last section

        has_time = False #yup

        for i in range(7): #hardcode lol, original was range(len( user_dict["day_available"] ))
            for j in range(24): #range(len( user_dict["day_available"][i] ))
                if user_dict["day_available"][i][j] and match_dict[key]["day_available"][i][j]: #great addresses; checks for if both people have matching times
                    has_time = True
        
        if not(has_time):
            match_dict.pop(key) #removes the people who don't share a time slot
            continue

    return match_dict #or something, Idk how you want this 

