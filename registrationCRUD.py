from flask import Flask, request, jsonify
import mysql
from databaseConnection import get_db_connection

app = Flask(__name__)



# TO INSERT NEW USER INTO THE DATABASE
@app.route('/addUser', methods=['POST'])
def add_user():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        fullname = request.json['FullName']
        email = request.json['Email']
        phonenumber = request.json['PhoneNumber']
        dateofbirth = request.json['DateOfBirth']
        gender = request.json['Gender']
        location = request.json['Location']
        
        cursor.execute('INSERT INTO registrationinfo (FullName, Email, PhoneNumber, DateOfBirth, Gender, Location) VALUES (%s, %s, %s, %s, %s, %s)', (fullname, email, phonenumber, dateofbirth, gender, location))
        conn.commit()
        
        user_id = cursor.lastrowid
        return jsonify({"message": "User data inserted successfully", "user_id": user_id}), 201
    
    except mysql.connector.Error as err: 
        app.logger.error(f"Database error: {err}")
        return jsonify({"message": "Data Insertion Unsuccessfull", "error": str(err)}), 500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# TO INSERT MULTIPLE USERS INTO THE DATABASE
@app.route('/addMultipleUsers', methods=['POST'])
def addMultiple_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        users = request.json
        
        if users:
            for user in users:
                cursor.execute('INSERT INTO registrationinfo (FullName, Email, PhoneNumber, DateOfBirth, Gender, Location) VALUES (%s, %s, %s, %s, %s, %s)', (user['FullName'], user['Email'], user['PhoneNumber'], user['DateOfBirth'], user['Gender'], user['Location']))
        if not users:
            return jsonify({"message": "No user data provided"}), 400
        conn.commit()
        
        return jsonify({"message": "User data's inserted successfully"}), 201
    
    except mysql.connector.Error as err: 
        if conn:
            conn.rollback()
        return jsonify({"message": "Data Insertion Unsuccessfull", "error": str(err)}), 500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# TO VIEW ALL USER DATA
@app.route('/viewAllUsers', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM registrationinfo')
        users = cursor.fetchall()
    
        if users:
            return jsonify({'message': 'Retrieve successful', 'users': users}), 200
        else:
            return jsonify({'message': 'No users found'}), 404

    except mysql.connector.Error as err:
        return jsonify({"message": "Data Retreival unsuccessfull", "error": str(err)}), 500 

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# TO VIEW SPECIFIC USER DATA
@app.route('/viewUser/<int:search_id>', methods=['GET'])
def getSpecific_User(search_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM registrationinfo where ID = %s', (search_id,))
        user = cursor.fetchone()
    
        if user:
            return jsonify({'message': 'User Available', 'user': user}), 200
        else:
            return jsonify({'message': 'No user found'}), 404

    except mysql.connector.Error as err:
        return jsonify({"message": "Data Retreival unsuccessfull", "error": str(err)}), 500 

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# TO UPDATE USER
@app.route('/updateUser/<int:user_id>', methods=['PUT'])
def update_User(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM registrationinfo where ID = %s', (user_id,))
        userDataBeforeUpdate = cursor.fetchone()
        if userDataBeforeUpdate:

            userUpdateData = request.json
            cursor.execute('UPDATE registrationinfo set FullName = %s, Email = %s, PhoneNumber = %s, DateOfBirth = %s, Gender = %s, Location = %s where ID = %s', (userUpdateData['FullName'], userUpdateData['Email'], userUpdateData['PhoneNumber'], userUpdateData['DateOfBirth'], userUpdateData['Gender'], userUpdateData['Location'], user_id))
            conn.commit()

            cursor.execute('SELECT * FROM registrationinfo where ID = %s', (user_id,))
            userDataAfterUpdate = cursor.fetchone()

            return jsonify({"message":"User Updation Successfull", "Data Before Update":userDataBeforeUpdate, "Data After Update" : userDataAfterUpdate}), 200

        else:
            return jsonify({'message': 'No user found'}), 404
    

    except mysql.connector.Error as err:
        return jsonify({"message": "Data Updation unsuccessfull", "error": str(err)}), 500 

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# TO REMOVE ALL USERS
@app.route('/removeAllUsers', methods=['DELETE'])
def remove_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('DELETE FROM registrationinfo')
        conn.commit()
    
        return jsonify({"message": "All rows deleted successfully and committed to the database."}), 200
    

    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        return jsonify({"message": "Removal unsuccessfull", "error": str(err)}), 500 

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# TO DELETE SPECIFIC USER DATA
@app.route('/removeUser/<int:user_id>', methods=['DELETE'])
def removeSpecific_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('DELETE FROM registrationinfo where ID = %s', (user_id,))
        conn.commit()
    
        return jsonify({"message": "User Removed Successfully"}), 200
    

    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        return jsonify({"message": "Removal unsuccessfull", "error": str(err)}), 500 

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(debug=True, port=5005)