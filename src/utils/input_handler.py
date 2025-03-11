class UserInputHandler:
    @staticmethod
    def get_user_input():
        game_id = input("Enter Game ID: ")
        clip_count = int(input("How many clips? "))
        return game_id, clip_count
