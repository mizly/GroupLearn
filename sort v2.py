#data structure; paralell between user dict and profile's dict values
# user = {
#     "grade": int
#     "subjects": ["array", "of", "strings"]
#     "day_available": [
#         [True, False, True, False],
#         [False, True, False, True],
#         [True, False, True, False]
#     ] 2D array containing arrays of bools, representing hours available

def sort_compabitility(user, **profile): #user and profile are for the target and comparisons, respectively
    comp_score = {} #stores compatibilty scores for each profile

    for key in profile: #parses through all the profiles

        shared_subjects = 0 #for tracking subjects shared
        shared_times = 0

        if dif := abs( user["grade"] - profile[key]["grade"] ) > 2: #assign dif variable as difference in grade, also checks if it's greater than 2
            profile.pop(key) #removes people who are more than 2 grades apart
            continue

        for i in user["subjects"]: #should be parsing through subjects array of user
            try:
                profile[key]["subjects"].index(i) #we do a little try-catching
                shared_subjects += 1
            except:
                pass #.index() returns ValueError if not found, meaning it skips the increment part
        
        if shared_subjects == 0:
            profile.pop(key) #removes the people who don't share a subject
            continue

        for i in range(7): #hardcode lol, original was range(len( user["day_available"] ))
            for j in range(24): #range(len( user["day_available"][i] ))
                if user["day_available"][i][j] and profile[key]["day_available"][i][j]: #great addresses; checks for if both people have matching times
                    shared_times += 1
        
        if shared_times == 0:
            profile.pop(key) #removes the people who don't share a time slot
            continue

        comp_score[key] = 1000*dif - 100*shared_subjects - shared_times #assigns score to profile based on grade difference; the lower the better

    return comp_score #or something, in this state it's returning a dictionary with the same key but int values for compatibility scores