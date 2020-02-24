import urllib.request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import mysql.connector


print("=====read url start=========")


try:
    with urllib.request.urlopen('http://www.premierleague.com/tables') as fp2:
        soupLeague = BeautifulSoup(fp2.read(),features="html.parser")

        teamList = soupLeague.findAll("tr", {"data-compseason":"274"})

except HTTPError as e:
    print(e)


print("=====mysql start=====")

try:
    cnx = mysql.connector.connect(host="localhost", user='root', password='root',  database='league')
    cursor = cnx.cursor()

    deleteQuery = "delete from england_league"
    cursor.execute(deleteQuery)
    cnx.commit()

    teamId = 0;
    for team in teamList:

        teamName = team.findAll("td")[2].find("a").findAll("span")[1].get_text()
        teamScore = team.findAll("td")[10].get_text()

#        print("teamName :",teamName,"!!!")
#        print("teamscore : ", teamScore)

        teamId += 1
        insertTeam = ( "insert into england_league VALUES ( %s, %s, %s, now() ) ;" )
        dataTeam = (teamId, teamName, teamScore)
        cursor.execute(insertTeam, dataTeam)

    cnx.commit()

    cursor.close()
    cnx.close()

except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))
