from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
# model the class after the friend table from our database
class Friendship:
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.friend_id = data['friend_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.friend = None
# Now we use class methods to query our database
    @classmethod
    def get_all(cls): #not a useful method for this assignment, but leaving it here just in case
        query = "SELECT * FROM friendships;"
        results = connectToMySQL('friendships_schema').query_db(query)
        friendships = []
        if not results or len(results)<1:
            return False
        else:
            for friendship in results:
                friendships.append( cls(friendship) )
            return friendships
    @classmethod
    def get_friendship(cls,data): 
        query = "SELECT * FROM friendships WHERE user_id = %(user_id)s AND friend_id = %(friend_id)s;"
        results = connectToMySQL('friendships_schema').query_db(query,data)
        if not results or len(results)<1:
            return False
        else:
            return(cls(results[0]))  
    @classmethod
    def save(cls,user1,user2):
        if user.User.validate_for_friendship(user1,user2):
            data={'user_id': user1.id, 'friend_id': user2.id}   
            query = "INSERT INTO friendships ( user_id , friend_id , created_at, updated_at )\
                    VALUES ( %(user_id)s , %(friend_id)s , NOW() , NOW() ),\
                     ( %(friend_id)s, %(user_id)s, NOW(), NOW());"
            # data is a dictionary that will be passed into the save method from server.py
            return connectToMySQL('friendships_schema').query_db( query, data )
        else:
            return False
    @classmethod
    def update(cls, data ):
        query = "UPDATE friendships SET user_id = %(user_id)s , friend_id = %(friend_id)s, updated_at = NOW() WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('friendships_schema').query_db( query, data )
    @classmethod
    def remove(cls, data):
        # query = "SET SQL_SAFE_UPDATES = 0;"
        query = "DELETE FROM friendships WHERE\
             (user_id = %(user_id)s AND friend_id = %(friend_id)s)\
                 OR (friend_id = %(user_id)s AND user_id = %(friend_id)s));"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('friendships_schema').query_db( query, data )
    def get_friend(self): 
         data = {'id':int(self.friend_id)}
         self.friend = user.User.get_user_info(data)
         return self