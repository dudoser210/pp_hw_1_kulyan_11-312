from dataclasses import dataclass, field
from enum import Enum
import cmd
import pickle


class UserRole(Enum):
    USER = 0
    ADMIN = 1


@dataclass
class User:
    user_id: int
    login: str
    password: str
    role: UserRole
    room_id: int


@dataclass
class Room:
    room_id: int
    name: str
    users: list
    admin_id: int
    gifts: dict = field(default_factory=dict)
    preferences: dict = field(default_factory=dict)
    settings: dict
    status: Enum


def save_to_pickle(secret_santa, data):
    with open(secret_santa, 'wb') as file:
        pickle.dump(data, file)


def load_from_pickle(secret_santa):
    with open(secret_santa, 'rb') as file:
        data = pickle.load(file)
        return data


class SecretSantaSystem(cmd.Cmd):
    intro = "Добро пожаловать в тайного Санту! Введите 'help' для просмотра комманд. \n"
    prompt = "Введите команду>"

    def __init__(self):
        super().__init__()
        self.users = load_from_pickle("users.pkl")
        self.rooms = load_from_pickle("rooms.pkl")
        self.current_user = None

    def save_data(self):
        save_to_pickle("users.pkl", self.users)
        save_to_pickle("rooms.pkl", self.rooms)

    def do_login(self, arg):
        login, passwword = arg.split()
        for user in self.users:
            if user.login == login and user.password == password:
                self.current_user = user
                print("Вход выполнен успешно.")
                return
        print("Вход не выполнен. Неправильный логин или пароль.")

    def do_join_room(self, arg):
        room_id = int(arg)
        if self.current_user:
            room = self.get_room_by_id(room_id)
            if room:
                room.users.append(self.current_user.user_id)
                self.current_user.room_id = room_id
                self.save_data()
                print(f"Вы подключились к комнате{room.name}")
            else:
                print("Комната не найдена.")

class SecretSantaSystem(cmd.Cmd):

    def do_change_room_name(self, arg):
       if self.current_user.role == UserRole.ADMIN:
           room_id, new_name = arg.split()
           room = self.get_room_by_id(int(room_id))
           if room:
               room.name = new_name
               self.save_data()
               print(f"Room name changed to '{new_name}'.")
           else:
               print("Room not found.")
       else:
           print("You don't have permission to change the room name.")

    def do_change_room_settings(self, arg):
        if self.current_user.role == UserRole.ADMIN:
            room_id, min_cost, max_cost = arg.split()
            room = self.get_room_by_id(int(room_id))
            if room and room.status == 0:
                room.settings = {'min_gift_cost': int(min_cost), 'max_gift_cost': int(max_cost)}
                self.save_data()
                print(f"Room settings changed: min cost={min_cost}, max cost={max_cost}.")
            else:
                print("Room not found or not in state 0.")
        else:
            print("You don't have permission to change the room settings.")

    def do_add_user_to_room(self, arg):
        if self.current_user.role == UserRole.ADMIN:
            room_id, user_id = arg.split()
            room = self.get_room_by_id(int(room_id))
            user = next((u for u in self.users if u.user_id == int(user_id)), None)
            if room and user:
                room.users.append(user.user_id)
                self.save_data()
                print(f"User '{user.login}' added to the room.")
            else:
                print("Room or user not found.")
        else:
            print("You don't have permission to add a user to the room.")

    def do_remove_user_from_room(self, arg):
        if self.current_user.role == UserRole.ADMIN:
            room_id, user_id = arg.split()
            room = self.get_room_by_id(int(room_id))
            if room:
                if int(user_id) in room.users:
                    room.users.remove(int(user_id))
                    self.save_data()
                    print(f"User removed from the room.")
                else:
                    print("User not in the room.")
            else:
                print("Room not found.")
        else:
            print("You don't have permission to remove a user from the room.")

    def do_start_distribution(self, arg):
        if self.current_user.role == UserRole.ADMIN:
            room_id = int(arg)
            room = self.get_room_by_id(room_id)
            if room and room.status == 0:
                if len(room.users) == len(room.preferences):
                    room.status = 1
                    self.save_data()
                    print("User distribution started.")
                else:
                    print("Not all users have set their preferences.")
            else:
                print("Room not found or not in state 0.")
        else:
            print("You don't have permission to start user distribution.")

    def do_show_distribution(self, arg):
        if self.current_user.role == UserRole.ADMIN:
            room_id = int(arg)
            room = self.get_room_by_id(room_id)
            if room and room.status == 1:
                print("User distribution:")
                print(room.gifts)
                print("User preferences:")
                print(room.preferences)
            else:
                print("Room not found or not in state 1.")
        else:
            print("You don't have permission to show distribution.")

def do_finish_room(self, arg):
    "Finish the room and change its state to 2"
    if self.current_user.role == UserRole.ADMIN:
        room_id = int(arg)
        room = self.get_room_by_id(room_id)
        if room and room.status == 1:
            room.status = 2
            self.save_data()
            print("Room finished and state changed to 2.")
        else:
            print("Room not found or not in state 1.")
    else:
        print("You don't have permission to finish the room.")

def do_leave_room(self, arg):
        if self.current_user:
            room_id = self.current_user.room_id
            room = self.get_room_by_id(room_id)
            if room and self.current_user.user_id in room.users:
                room.users.remove(self.current_user.user_id)
                self.current_user.room_id = -1
                self.save_data()
                print("Вы покинули комнату.")
            else:
                print("Вы не находитесь в комнате.")

def do_set_preferences(self, arg):
    if self.current_user:
        preferences = arg
        room_id = self.current_user.room_id
        room = self.get_room_by_id(room_id)
        if room:
            user_preferences = room.preferences
            user_preferences[self.current_user.user_id] = preferences
            self.save_data()
            print("Список предпочтений составлен.")
        else:
            print("Вы не находитесь в комнате.")

    def do_distribute_gifts(self, arg):
        room_id = int(arg)
        room = self.get_room_by_id(room_id)
        if room and room.status == 0:
            room.status = 1
            self.save_data()
            print("Дарящие были распределены.")

    def get_room_by_id(self, room_id):
        for room in self.rooms:
            if room.room_id == room_id:
                return room
        return None

    def do_exit(self, arg):
        print("Покидаем тайного Санту...")
        return True

    def default(self, line):
        print(f"Комманда '{line}' не распознана. Введите 'help' для просмотра комманд.")


system = SecretSantaSystem()
system.cmdloop()
