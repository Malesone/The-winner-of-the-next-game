str = "h_team	Risultato	h_goals	a_team	a_goals	h_total_shots	h_shots_on_target	h_goals_on_penalty	h_total_penalties	h_completed_passings	h_total_passings	h_corners	h_percentage_possession	h_fouls	h_yellow_cards	h_red_cards	a_total_shots	a_shots_on_target	a_goals_on_penalty	a_total_penalties	a_corners	a_yellow_cards	a_red_cards	a_fouls	a_completed_passings	a_total_passings	a_percentage_possession"

strings = str.split("	")
count = 0
for string in strings: 
    string = "| " + string + " |  |"
    strings[count] = string
    count+=1
    print(string)