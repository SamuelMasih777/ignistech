from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .serializers import UserSerializer
from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
# from .models import Event


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not (username and password):
            return JsonResponse({'error': 'Username and password are required.'}, status=400)

        try:
            with connection.cursor() as cursor:
                sql_query = "INSERT INTO Users (username, password) VALUES (%s, %s)"
                cursor.execute(sql_query, [username, password])
                # Commit the transaction
                connection.commit()

                user_id = get_user_id_by_username(username)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': 'User registered successfully.'}, status=201)

    return JsonResponse({'error': 'Method not allowed.'}, status=405)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not (username and password):
            return JsonResponse({'error': 'Username and password are required.'}, status=400)

        try:
            with connection.cursor() as cursor:
                sql_query = "SELECT * FROM Users WHERE username = %s AND password = %s"
                cursor.execute(sql_query, [username, password])
                user = cursor.fetchone()

                if user:
                    # If the user is found, return success message or any other relevant data
                    return JsonResponse({'message': 'Login successful.'})
                else:
                    return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed.'}, status=405)


def signout(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def get_user_id_by_username(username):
    try:
        with connection.cursor() as cursor:
            sql_query = "SELECT user_id FROM Users WHERE username = %s"
            cursor.execute(sql_query, [username])
            user_id = cursor.fetchone()[0]  # Fetch the user_id from the query result
            if not user_id:
                return JsonResponse({'error': 'Not Found.'}, status=400)
            return user_id

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def create_event_for_user(request, username):
    if request.method == 'POST':
        try:
            # Retrieve user_id
            user_id = get_user_id_by_username(username)
            print(user_id)

            with connection.cursor() as cursor:
                event_name = request.POST.get('event_name')
                data = request.POST.get('data')
                # time = request.POST.get('time')
                location = request.POST.get('location')
                image = request.POST.get('image')
                is_liked = False  # Assuming is_liked is always False initially

                # Insert event for the user
                sql_insert_event = "INSERT INTO event (event_name, data,  location, image, is_liked, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_insert_event, [event_name, data, location, image, is_liked, user_id])
                connection.commit()

            return JsonResponse({'message': 'Event created successfully.'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed.'}, status=405)

@csrf_exempt
def fetch_all_events(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                # Execute SQL query
                cursor.execute("SELECT * FROM event")
                # Fetch all rows from the result
                events = cursor.fetchall()

                # Serialize events data
                serialized_events = []
                for event in events:
                    serialized_event = {
                        'event_name': event[1],  # Assuming event_name is in the second column
                        'data': event[2],        # Assuming data is in the third column
                        'time': event[3],        # Assuming time is in the fourth column
                        'location': event[4],    # Assuming location is in the fifth column
                        'image': event[5],       # Assuming image is in the sixth column
                        'is_liked': event[6],    # Assuming is_liked is in the seventh column
                        'user_id': event[7]      # Assuming user_id is in the eighth column
                    }
                    serialized_events.append(serialized_event)

            return JsonResponse({'events': serialized_events})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed.'}, status=405)
