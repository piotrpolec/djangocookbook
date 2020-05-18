class Country:

    def __init__(self, name, cords):
        self.name = name
        self.cords = cords

    def get_name(self):
        return self.name

    def get_first_cord(self):
        return self.cords[0]

    def get_second_cord(self):
        return self.cords[1]


class CountryList:
    def __init__(self):
        self.country_list = []

    def add_country(self, country):
        self.country_list.append(country)

    def delete_country(self, country):
        if country in self.country_list:
            self.country_list.remove(country)

    def edit_country(self, country):
        if country in self.country_list:
            self.delete_country(country)

        self.add_country(country)

    def get_country_list(self):
        return self.country_list

    def find_country_by_name(self, country_name):
        for country in self.country_list:
            if country.get_name() == country_name:
                return country
        return None

