# from pprint import pprint


class BaseApiResponse:
    def __init__(self):
        self.errors = []
        self.data = None

    def add_error(self, err):
        self.errors.append(err)

    def make(self):
        payload = {
            "errors": self.errors,
        }

        if self.data:
            payload["data"] = self.data

        return payload


class UserApiResponse(BaseApiResponse):
    def __init__(self):
        super().__init__()
        self.user = None

    def set_user(self, user, *args, **kwargs):
        self.user = user.to_json(*args, **kwargs)

    def make(self):
        return {
            "errors": self.errors,
            "user": self.user
        }


class TeamApiResponse(BaseApiResponse):
    def __init__(self):
        super().__init__()
        self.team = None

    def set_team(self, team, *args, **kwargs):
        self.team = team.to_json(*args, **kwargs)

    def make(self):
        return {
            "errors": self.errors,
            "team": self.team
        }


class ListTeamsApiResponse(BaseApiResponse):
    def __init__(self):
        super().__init__()
        self.teams = None

    def set_teams(self, teams, *args, **kwargs):
        self.teams = [team.to_json(*args, **kwargs) for team in teams]

    def make(self):
        return {
            "errors": self.errors,
            "teams": self.teams
        }


class VpnAccessApiResponse(BaseApiResponse):
    def __init__(self):
        super().__init__()
        self.config = None

    def make(self):
        return {
            "errors": self.errors,
            "config": self.config
        }


class ListUsersApiResponse(BaseApiResponse):
    def __init__(self):
        super().__init__()
        self.users = []

    def set_users(self, users, *args, **kwargs):
        self.users = [user.to_json(*args, **kwargs) for user in users]

    def make(self):
        return {
            "errors": self.errors,
            "users": self.users
        }


class ListProvidersApiResponse(BaseApiResponse):
    def __init__(self):
        super().__init__()
        self.providers = None

    def set_providers(self, providers, *args, **kwargs):
        self.providers = [pv.to_json(*args, **kwargs) for pv in providers]

    def make(self):
        return {
            "errors": self.errors,
            "providers": self.providers
        }


class ListBoxesTemplatesApiResponse(BaseApiResponse):
    def __init__(self):
        super().__init__()
        self.templates = []

    def make(self):
        return {
            "errors": self.errors,
            "templates": self.templates
        }


class ListRealmsApiResponse(BaseApiResponse):
    def __init__(self):
        super().__init__()
        self.realms = []

    def make(self):
        return {
            "errors": self.errors,
            "realms": self.realms
        }


class ListBoxesApiResponse(BaseApiResponse):
    def __init__(self):
        super().__init__()
        self.boxes = []

    def set_boxes(self, boxes, **kwargs):
        self.boxes = [box.to_json(**kwargs) for box in boxes]

    def make(self):
        return {
            "errors": self.errors,
            "boxes": self.boxes
        }


class ListCategoriesApiResponse(BaseApiResponse):
    def __init__(self):
        super().__init__()
        self.categories = []

    def set_categories(self, categories, **kwargs):
        self.categories = [cat.to_json(**kwargs) for cat in categories]

    def make(self):
        return {
            "errors": self.errors,
            "categories": self.categories
        }
