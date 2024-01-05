'''Assembles/updates npoint bin of emails and MagicEden Ordinal URLs for monitoring offers.'''
import requests
import json


class UserManager:
    def __init__(self):
        self.npoint_bin = "https://api.npoint.io/4046dafca4a7c1e7753a"

    def pull_data(self):
        '''Retrieves current npoin bin data.'''
        response = requests.get(self.npoint_bin)

        if response.status_code == 200:
            print("\nData retrieved successfully.")
        else:
            print(
                f"\nFailed to retrieve data. Status code: {response.status_code}")
            print(response.text)

        data = json.loads(response.text)
        print(f"\nRetrieved data: {data}")
        return data

    def push_data(self, data_to_push):
        '''Pushes new data to npoint bin.'''
        response = requests.post(
            self.npoint_bin, data=data_to_push)

        if response.status_code == 200:
            print("\nData pushed successfully.")
        else:
            print(
                f"\nFailed to push data. Status code: {response.status_code}")
            print(response.text)

    def add_new_user(self, email: str, initial_url: str):
        '''Adds a new user and first URL to npoint bin.'''
        data = self.pull_data()

        is_new_user = True

        for user_profile in data:
            if user_profile["email"] == email:
                print("User already exists.")
                is_new_user = False

        if is_new_user:
            new_user = {email: [initial_url]}
            data.append(new_user)
            data_to_push = json.dumps(data)
            self.push_data(data_to_push)

    def remove_existing_user(self, email:str):
        data = self.pull_data()

        for user_profile in data:
            if user_profile["email"] == email:
                data.remove(user_profile)
                print(f"\nRemoved user profile: {user_profile}")
         
        print(f"\nUpdated data: {data}")
        self.push_data(data)

    def add_url(self, email: str, new_url: str):
        '''Adds a URL to user's list.'''
        data = self.pull_data()

        for index, user_profile in enumerate(data):
            if user_profile.get("email") == email:
                user_index = index
                data[user_index]["tracked_urls"].append(new_url)
                print(f"\nUpdated user profile: {data[user_index]}")

        data_to_push = json.dumps(data)
        self.push_data(data_to_push)


if __name__ == "__main__":
    manager = UserManager()
    manager.remove_existing_user("test2@gmail.com")
    # input = ("Make a selection:\n1. Add user\n2. Remove user\n3. Add URL to existing user\n4. Remove URL from existing user")