class SeasonTablesManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if SeasonTablesManager.__instance is None:
            SeasonTablesManager.__instance = object.__new__(cls)

            return SeasonTablesManager.__instance

    def __init__(self):
        # Get all season table states from the database

        # An object containing as attributes all team names with values a list of
        # SeasonTable objects.
        # Ex. : {"Man United" : [{SeasonTable}, {SeasonTable}, {SeasonTable}, ...],
        #        "Man City" : [{SeasonTable}, {SeasonTable}, {SeasonTable}, ...],
        #        ... }
        self.season_tables = self.get_season_tables_from_db(self)

    def get_season_tables_from_db(self):
        result = {}

        season_tables = SeasonTables.objects.all()

        for table_state in season_tables:
            if table_state


        return result

    def get_table_state(self, team, date, season):
        # An object containing as attribute the team name with value a list of SeasonTable
        # object. Ex. : {"Man United" : [{SeasonTable}, {SeasonTable}, {SeasonTable}, ...]
        table_state = {}






gSeasonTablesMgr = SeasonTablesManager()