from locust import HttpUser, TaskSet, task


def login(l):
    l.client.post("auth/login/", {"username": "kuznetsov", "password": "1"})


def logout(l):
    l.client.post("auth/logout/", {"username":"kuznetsov", "password":"1python -m pip install locustio"})


def index(l):
    l.client.get("/")

# def profile(l):
#     l.client.get("auth/edit/")


def products(l):
    l.client.get("/products/")

def contacts(l):
    l.client.get("/contacts/")

def category(l):
    l.client.get("/products/category/1/")

def basket(l):
    l.client.get("/basket/")

def category(l):
    l.client.get("/products/category/1/")

def order(l):
    l.client.get("/order/")

def order_update(l):
    l.client.get("/order/update/1/")


@task
class UserBehavior(TaskSet):
    tasks = {index: 2, products: 5, contacts: 5, category: 5, basket: 5, order: 5, order_update: 5}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)
@task
class WebsiteUser(HttpUser):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 900