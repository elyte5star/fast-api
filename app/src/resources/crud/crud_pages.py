from resources.utils.base_functions import Utilities
from .crud_bookings import Bookings, CreateBooking
from .crud_products import Products, GetProductDetailsRequest, GetSortRequest
from .crud_users import Users
from resources.auth.crud_auth import Auth
from starlette.templating import Jinja2Templates
from dateutil.parser import parse
from newsapi import NewsApiClient
from fastapi.responses import RedirectResponse


class PageHandler(Utilities):
    def __init__(self, cf):
        super().__init__(cf)
        self.user_handler = Users(cf)
        self.product_handler = Products(cf)
        self.book_handler = Bookings(cf)
        self.auth_handler = Auth(cf)
        self.news_api = NewsApiClient(api_key=cf.news_api_key)
        self.templates = Jinja2Templates(directory="./resources/templates")
        self.templates.env.filters["datetime_format"] = self.datetime_format

    def datetime_format(self, value):
        dt = parse(value)
        return str(dt.date()) + " " + str(dt.time().replace(microsecond=0))

    async def _news(self, data: dict = {}):
        list_articles = self.news_api.get_top_headlines()["articles"]
        newlist = sorted(
            list_articles, key=lambda x: x["title"], reverse=False
        )
        data["headlines"] = newlist

        return self.templates.TemplateResponse("news.html", data)

    async def _game(self, data: dict = {}):
        return self.templates.TemplateResponse("game.html", data)

    async def _map(self, data: dict = {}):
        return self.templates.TemplateResponse("map.html", data)

    async def _login(self, data: dict = {}):
        data["google_id"] = self.cf.google_client_id
        return self.templates.TemplateResponse("login.html", data)

    async def _admin(self, data: dict = {}):
        request = data["request"]
        if request.session.get("user")["username"] == self.cf.username:
            data["user_info"] = request.session.get("user")
            return self.templates.TemplateResponse("admin.html", data)
        self.log.warning("Admin rights needed!!")
        return RedirectResponse(url="/login")

    async def _sort_items_(self, data: dict = {}):
        data["result"] = await self.product_handler._sort_items(
            GetSortRequest(key=data["sort_key"])
        )
        return self.templates.TemplateResponse("sorted.html", data)

    async def index_page(self, data: dict = {}):
        res = await self.product_handler._get_products()
        data["products"] = res.products
        return self.templates.TemplateResponse("index.html", data)

    async def _one_product(self, data: dict = {}):
        res = await self.product_handler._get_product(
            GetProductDetailsRequest(pid=data["pid"])
        )
        data["product"] = res.product
        return self.templates.TemplateResponse("product.html", data)

    async def _create_booking(self, data: dict = {}):
        user_info = None
        if "user" in data["request"].session:
            user_info = data["request"].session.get("user")
            result = await self.book_handler._create_booking(
                CreateBooking(
                    discount=user_info["discount"],
                    userid=user_info["userid"],
                    pid=data["pid"],
                    volume=data["volume"],
                    unit_price=data["unit_price"],
                )
            )
            data["order"] = result
            data["userinfo"] = user_info
            return self.templates.TemplateResponse("order.html", data)
        data["msg"] = "Please log in!"
        return await self._one_product(data)
