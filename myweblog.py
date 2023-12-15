import json
from datetime import datetime
from time_logger_decorator import logger





class User:
    id = 0
    users = {}
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.is_registerd = None
        self.is_logged = None

    def register(self):
        if self.username not in self.users:
            User.id += 1
            self.users[self.username] = [self.password,self.id]
            self.is_registerd = True
            print("register was successful!")
        else:
            print("this username exist!")

    def login(self):
        if self.username in self.users:
            if self.password in self.users[self.username]:
                self.is_loggd = True
                print("login was successful!")
            else:
                print("password is wrong!")
        else:
            print("username was not found!")

class Post:
    def __init__(self,title=None,content=None):
        self.title = title
        self.content = content
        self.author = None
        self.create_at = self.get_time()
        self.update_at = None

    @staticmethod
    def get_id():
        while True:
            username = input("please enter your username to find your id: ")
            user_info = User.users.get(username)
            if user_info:
                author_information_list = [username, user_info[1]]
                return author_information_list
            else:
                print("Username not found. Please enter a valid username.")

    @staticmethod
    def get_time():
        return datetime.now()

    def set_author(self):
        p1 = Post()
        self.author = p1.get_id()

    def set_update_time(self):
        self.update_at = datetime.now()


class Blog(Post):
    posts = {}

    @logger
    def create_post(self):
        self.set_author()
        authors_information = self.author
        post = {
            "title": self.title,
            "content": self.content,
            "author": authors_information,
            "create time": str(self.create_at),
            "update time": str(self.update_at)
        }
        self.posts[self.title] = post
        with open("post_data.json", "w") as post_detail:
            json.dump(self.posts, post_detail, indent=1)

    @logger
    def delete_item(self,key_to_delete):
        with open("post_data.json", "r") as file:
            data = json.load(file)

        if key_to_delete in data:
            del data[key_to_delete]
            with open("post_data.json", "w") as file:
                json.dump(data, file, indent=2)
            yield f"The element with key '{key_to_delete}' has been deleted."
        else:
            yield f"The element with key '{key_to_delete}' was not found in the JSON file."

    @staticmethod
    @logger
    def find_elements_by_author(author_name):
        with open("post_data.json","r") as posts_json:
            post_data = json.load(posts_json)
        results = []
        for key, value in post_data.items():
            if isinstance(value, dict) and "author" in value and isinstance(value["author"], list) and len(
                    value["author"]) > 0 and value["author"][0] == author_name:
                results.append({key: value})
        return results if results else None

    @staticmethod
    @logger
    def find_elements_by_title(title):
        with open("post_data.json","r") as post_json:
            data = json.load(post_json)
        filtered_posts = list(filter(lambda value: value["title"] == title, data.values()))
        for post in filtered_posts:
            print(post)

    @staticmethod
    @logger
    def change_content_by_title(title, new_content):
        with open("post_data.json", "r") as file:
            data = json.load(file)
        if title in data:
            data[title]["content"] = new_content
            data["update time"] = str(datetime.now())
            with open("post_data.json", "w") as file:
                json.dump(data, file, indent=1)
            print(f"The content for the post '{title}' has been updated.")
        else:
            print(f"The post with title '{title}' was not found in the JSON data.")

    @staticmethod
    def show_all_posts():
        with open("post_data.json","r") as file:
            posts = json.load(file)
            return posts


def main():
    print("1.register\n2.login")
    choice = int(input("please choose an option: "))
    if choice == 1:
        return register_for_main()
    elif choice == 2:
        return login_for_main()


def register_for_main():
    print("1.back to menu\n2.register")
    choice = int(input("if you already have an account back to menu and login: "))
    if choice == 1:
        return main()
    if choice == 2:
        name = input("please enter your name: ")
        password = input("please enter your password: ")
        user_register = User(name, password)
        user_register.register()
        if user_register.is_registerd:
            print("connecting to login page...")
            print(user_register.users)
            return login_for_main()
def login_for_main():
    global name_
    name_ = input("please enter your name: ")
    global password_
    password_ = input("please enter your password: ")
    user_login = User(name_,password_)
    user_login.login()
    print(user_login.users)
    if user_login.is_logged:
        return main()
    else:
        return second_main()

def  second_main():
    print("1.my activity\n2.search post\n3.show all posts\n4.exit")
    _choice = int(input("please choose an option: "))
    if _choice == 4:
        return main()
    if _choice == 3:
        make_blog = Blog("","")
        make_blog.show_all_posts()
        return second_main()
    if _choice == 2:
        print("1.search by author\n2.search by title")
        new_choice = int(input("please choose an option: "))
        if new_choice == 1:
            make_blog = Blog("","")
            author_name = input("Enter the author name: ")
            result = make_blog.find_elements_by_author(author_name)
            for item in result:
                print(item)
                return second_main()
        if new_choice == 2:
            make_blog = Blog("", "")
            title = input("please enter the title: ")
            make_blog.find_elements_by_title(title)
            return second_main()
    if _choice == 1:
        print("1.create post\n2.delete post\n3.edit post\n4.back to menu")
        choice_for_my_activity_option = int(input("please choose an option: "))
        if choice_for_my_activity_option == 1:
            title = input("please write the title: ")
            content = input("please enter the content: ")
            make_post_blog_class = Blog(title, content)
            make_post_blog_class.create_post()
            return second_main()
        if choice_for_my_activity_option == 2:
            author_name = input("Enter your username so we show you your posts: ")
            make_blog = Blog("", "")
            result = make_blog.find_elements_by_author(author_name)
            for item in result:
                print(item)
            key_to_delete = input("Enter the key you want to delete: ")
            result_generator = make_blog.delete_item(key_to_delete)
            next(result_generator)
            return second_main()
        if choice_for_my_activity_option == 3:
            myblog = Blog("","")
            title = input("please enter the title of post that you want to chane: ")
            new_content = input("please enter the new content")
            myblog.change_content_by_title(title,new_content)
            return second_main()

        if choice_for_my_activity_option == 4:
            return second_main()

main()



