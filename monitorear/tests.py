from django.test import TestCase

# Create your tests here.
    # Obtains the 'usuario_id' from the session variable and assigns it to 'usuario_id' variable.
def test_obtains_usuario_id(self):
    # Arrange
    request = RequestFactory().get('/')
    request.session = {'usuario_id': 1}
    view = ArView()

    # Act
    response = view.get(request)

    # Assert
    assert response.context_data['usuario_id'] == 1