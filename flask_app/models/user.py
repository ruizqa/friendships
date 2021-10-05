from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import friendship
from flask import flash
# model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.friendships=[]
# Now we use class methods to query our database
    @staticmethod
    def validate_user(data):
        if len(data['first_name'] )<1 or len(data['last_name'])<1:
            flash("The first name and last name must be at least 1 character long","user")
            return False
        return True

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('friendships_schema').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        if not results or len(results)<1:
            return False
        else:        
            for result in results:
                users.append( cls(result) )
            return users
    @classmethod
    def get_user_info(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL('friendships_schema').query_db(query,data)
        if not result or len(result)<1:
            return False
        else:
            return cls(result[0])
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users (first_name, last_name, created_at, updated_at) VALUES ( %(first_name)s,%(last_name)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('friendships_schema').query_db( query, data )
    def get_friendships(self):
        query= "SELECT * FROM friendships WHERE user_id = %(user_id)s;"
        data = {'user_id': int(self.id)}
        results = connectToMySQL('friendships_schema').query_db(query,data)
        if not results:
            return self

        for result in results:
            friendship_e = friendship.Friendship(result)
            
            friendship_e = friendship_e.get_friend()
            
            self.friendships.append(friendship_e)
            
        return self
    @classmethod
    def validate_for_friendship(cls,user1,user2):
        user1 = user1.get_friendships()
        user2 = user2.get_friendships()

        if user1.id == user2.id:
            return False
        for friendship in user1.friendships:
            if friendship.friend_id == user2.id:
                return False
        for friendship in user2.friendships:
            if friendship.friend_id == user1.id:
                return False
        return True 
    @classmethod
    def get_all_with_friendships(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('friendships_schema').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        if not results or len(results)<1:
            return False
        else:        
            for result in results:
                user_e = cls(result)
                user_e.get_friendships()
                users.append( user_e )
            return users
