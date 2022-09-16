from html_scrape import HtmlScrape
from team import Team

class Controller:
    def __init__(self):
        self.html = HtmlScrape()
        self.html.connect()

    def start(self):
        self.a_hrefs = self.html.extract_teams()
        
    def extract_team(self):
        array_teams = []
        self.teams = [a_href for a_href in self.a_hrefs if '/squadre/' in str(a_href)]        
        for team in self.teams: 
            array_teams.append(Team(team.contents[0], team.get("href")))

        
        """self.teams = [a_href.contents[0] for a_href in self.a_hrefs if '/squadre/' in str(a_href)] #filtro i nomi delle squadre
        self.teams.sort()

        links = [l.get("href") for l in self.a_hrefs]
        self.links = [l for l in links if '/squadre/' in l]  
        """

controller = Controller()
controller.start()
controller.extract_team()