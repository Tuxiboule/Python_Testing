def test_integration_scenario(client, clubs):
    # Test the entire workflow of registration, booking, and points display

    # Step 1: Login a user and show the summary
    email = 'john@simplylift.co'
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 200
    # Check that the welcome page is displayed
    assert b'Welcome, john@simplylift.co' in response.data

    # Step 2: Perform booking for a competition
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': 1
    })
    assert response.status_code == 200
    #assert b'Great-booking complete!' in response.data

    # Step 3: logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

    # Step 4: Check points display page
    response = client.get('/points')
    for club in clubs:
        assert club['name'].encode("utf-8") in response.data
    assert response.status_code == 200
