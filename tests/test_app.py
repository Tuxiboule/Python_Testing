def test_index(client):
    """
    Test the index page.

    Args:
        client (FlaskClient): The Flask client for making requests.

    Returns:
        None
    """
    response = client.get('/')
    assert b'Welcome to the GUDLFT Registration Portal' in response.data
    assert response.status_code == 200


def test_show_summary(client):
    """
    Test the show_summary endpoint with email in the database and email not in the database.

    Args:
        client (FlaskClient): The Flask client for making requests.

    Returns:
        None
    """
    test_emails = ['example@email.com', 'john@simplylift.co', 'wrong_format_email']
    for email in test_emails:
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 200

        if b'Club not found for the provided email' not in response.data:
            assert email.encode("utf-8") in response.data


def test_book_point_place(client, clubs, competitions):
    """
    Test booking competition with various points/places available.

    Args:
        client (FlaskClient): The Flask client for making requests.
        clubs (list): List of clubs.
        competitions (list): List of competitions.

    Returns:
        None
    """
    # Right amount of places
    for club in clubs:
        for competition in competitions:
            place_to_buy = 3
            data = {'club': club['name'],
                    'competition': competition['name'],
                    'places': place_to_buy}
            response = client.post('/purchasePlaces', data=data)
            assert response.status_code == 200
            assert int(competition['numberOfPlaces']) >= 0
            assert int(club['points']) >= 0
    # Wrong amount of places
    for club in clubs:
        for competition in competitions:
            place_to_buy = int(club['points']) + 1
            data = {'club': club['name'],
                    'competition': competition['name'],
                    'places': place_to_buy}
            response = client.post('/purchasePlaces', data=data)
            assert response.status_code == 200
            assert b'There is not enough places' in response.data


def test_logout(client):
    """
    Test for a good working logout.

    Args:
        client (FlaskClient): The Flask client for making requests.

    Returns:
        None
    """
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data


def test_points(client, clubs):
    """
    Test for a good working points display.

    Args:
        client (FlaskClient): The Flask client for making requests.
        clubs (list): List of clubs.

    Returns:
        None
    """
    response = client.get('/points')
    for club in clubs:
        assert club['name'].encode("utf-8") in response.data
    assert response.status_code == 200


def test_flash_messages(client):
    """
    Test the display of flash messages in the Flask application.

    This test covers different scenarios, including the case where the club is not found for the provided email,
    the case where booking is successful, and the case where there are not enough places.

    Args:
        client (FlaskClient): The Flask client for making requests.

    Returns:
        None
    """
    # Test the case where the club is not found for the provided email
    response = client.post('/showSummary', data={'email': 'nonexistent@email.com'})
    assert response.status_code == 200
    assert b'Club not found for the provided email.' in response.data

    # Test the case where booking is successful
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': 1
    })
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    # Test the case where there are not enough places
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': 13
    })
    assert response.status_code == 200
    assert b"There is not enough places or" in response.data


def test_page_not_found(client):
    """
    Response test for a non-existing page.

    Args:
        client (FlaskClient): The Flask client for making requests.

    Returns:
        None
    """
    response = client.get('/nonexistingpage')
    assert response.status_code == 404
