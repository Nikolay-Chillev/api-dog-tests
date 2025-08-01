import requests
import pytest

# API configuration
BASE_URL = "https://dog.ceo/api"

# Test data - using a reliable breed and sub-breed combination
TEST_BREED = "hound"
TEST_SUB_BREED = "afghan"

def test_get_all_breeds():
    """Make sure we can get a list of all dog breeds"""
    response = requests.get(f"{BASE_URL}/breeds/list/all")
    data = response.json()
    
    # Basic response validation
    assert response.status_code == 200, "API should respond with 200"
    assert data['status'] == 'success', "API status should be success"
    assert 'message' in data, "Response should include breeds data"
    
    # Check if we got some breeds back
    breeds = data['message']
    assert len(breeds) > 0, "Should return at least one dog breed"
    
    # Verify some common breeds exist
    for breed in ['beagle', 'poodle', 'labrador']:
        assert breed in breeds, f"{breed} should be in the list"

def test_get_random_breed_image():
    """Verify we can get a random image for a specific breed"""
    response = requests.get(f"{BASE_URL}/breed/{TEST_BREED}/images/random")
    data = response.json()
    
    # Check basic response
    assert response.status_code == 200, "Should get a successful response"
    assert data['status'] == 'success', "API should report success"
    
    # Validate the image URL
    img_url = data['message']
    assert img_url.startswith('http'), "Should return a valid URL"
    assert img_url.lower().endswith(('.jpg', '.jpeg', 'png')), "Should be an image URL"

def test_get_sub_breed_images():
    """Check if we can get images for a specific sub-breed"""
    response = requests.get(f"{BASE_URL}/breed/{TEST_BREED}/{TEST_SUB_BREED}/images")
    data = response.json()
    
    # Basic checks
    assert response.status_code == 200, "Request should succeed"
    assert data['status'] == 'success', "API should return success"
    
    # Should get a list of image URLs
    images = data['message']
    assert len(images) > 0, "Should return at least one image"
    
    # Check first image URL
    assert images[0].startswith('http'), "Should return valid image URLs"

def test_nonexistent_breed():
    """Verify the API returns 404 for non-existent breeds"""
    fake_breed = "notarealbreed123"
    response = requests.get(f"{BASE_URL}/breed/{fake_breed}/images/random")
    
    # Verify the error response
    assert response.status_code == 404, "Should return 404 for unknown breed"
    data = response.json()
    assert data['status'] == 'error', "Should return error status for unknown breed"

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
    
    # Keep the window open until the user presses Enter
    input("\nPress Enter to exit...")