import csv

class MovieRecommendationSystem:
    def __init__(self):
        self.users = {}  # Dictionary to store user data

    def load_users_from_csv(self, csv_path):
        """Load users from a CSV file and populate the users dictionary."""

        try:
            with open(csv_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    user_id = row['user_id']
                    user_data = {key: value for key, value in row.items() if key != 'user_id'}
                    self._add_user(user_id, user_data)
            print("Users loaded successfully from CSV.")
        except FileNotFoundError:
            print(f"File {csv_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def _authenticate(self, user_id):
        """Check if a user is authenticated."""
        return user_id in self.users

    def _add_user(self, user_id, user_data): 
        """Add a new user to the system."""
        if user_id not in self.users:
            self.users[user_id] = user_data
            print(f"User {user_id} added.")
        else:
            print(f"User {user_id} already exists.")

    def _collect_user_preferences(self, user_id):
        """Collect user preferences for movie recommendations."""
        if not self._authenticate(user_id):
            print("User not authenticated.")
            return

        genres = ["Action", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Thriller"]
        print("Please select your favorite genres from the list below:")
        for i, genre in enumerate(genres, 1):
            print(f"{i}. {genre}")

        selected_genres = input("Enter the numbers of your favorite genres, separated by commas: ")
        selected_genres = [genres[int(i) - 1] for i in selected_genres.split(",") if i.isdigit() and 1 <= int(i) <= len(genres)]

        print("Please provide some additional information to improve recommendations.")

        keywords = input("Enter a few keywords related to your favorite genres, separated by commas: ").split(",")

        favorite_actors = input("Enter the names of your favorite actors, separated by commas (optional): ").split(",")
        favorite_movies = input("Enter the names of your favorite movies, separated by commas (optional): ").split(",")

        # create tags for the user
        tags = selected_genres + [keyword.strip() for keyword in keywords] + \
               [actor.replace(" ", "") for actor in favorite_actors if actor.strip()] + \
               [movie.replace(" ", "") for movie in favorite_movies if movie.strip()]

        self.users[user_id]['tags'] = " ".join(tags)
        print("User preferences collected successfully.")


    def get_started(self, user_id):
        """Get started with the recommendation system."""
        if self._authenticate(user_id):
            print(f"Welcome, {user_id}!")
        else:
            print("User not authenticated.")
            print("Registering user to get started.")
            self._add_user(user_id, {"num_of_ratings":0, "is_new_user": 1})

            # ask the new user to rate some movies or provide some information
            self._collect_user_preferences(user_id)
            
            # Save new user data to dim_users.csv
            try:
                with open('data_model/dim_users.csv', mode='a', encoding='utf-8', newline='') as file:
                    fieldnames = ['user_id', 'num_of_ratings', 'is_new_user', 'tags']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)

                    # Check if file is empty to write the header
                    if file.tell() == 0:
                        writer.writeheader()

                    user_data = self.users[user_id]
                    user_data['user_id'] = user_id
                    writer.writerow(user_data)
                    print("New user data saved.") ## saved to dim_users.csv
            except Exception as e:
                print(f"An error occurred while saving user data: {e}")

    def get_recommendations(self, user_id):
        """Get movie recommendations for a user."""
        if user_id in self.users:
            # Logic to generate recommendations for existing user
            return self._generate_recommendations(user_id)
        else:
            print(f"User {user_id} does not exist.")
            return []

    def _generate_recommendations(self, user_id):
        """Private method to generate recommendations."""
        # Placeholder logic for generating recommendations
        return ["Movie1", "Movie2", "Movie3"]