import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        """Initialise l'application et le client de test avant chaque fonction"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Nettoie le contexte après chaque test"""
        self.app_context.pop()

    def test_create_user_success(self):
        """Vérifie la création réussie de Goofy et Donald"""
        # Test Goofy
        payload_goofy = {
            "first_name": "Goofy",
            "last_name": "Dog",
            "email": "goofy@disney.com",
            "pets": "DOG"
        }
        response = self.client.post('/api/v1/users/', json=payload_goofy)
        self.assertEqual(response.status_code, 201)

        # Test Donald
        payload_donald = {
            "first_name": "Donald",
            "last_name": "Duck",
            "email": "donald@disney.com",
            "pets": "OTHERS"
        }
        response = self.client.post('/api/v1/users/', json=payload_donald)
        self.assertEqual(response.status_code, 201)

    def test_email_duplicate(self):
        """Vérifie que l'on ne peut pas créer deux fois le même email"""
        user_data = {
            "first_name": "Donald",
            "last_name": "Duck",
            "email": "donald@disney.com",
            "pets": "OTHERS"
        }
        # Premier envoi : Succès
        self.client.post('/api/v1/users/', json=user_data)
        # Deuxième envoi : Échec attendu
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email already registered", response.get_data(as_text=True))

    def test_get_all_users(self):
        """Vérifie que la liste contient les utilisateurs créés"""
        # On crée un utilisateur pour être sûr que la liste n'est pas vide
        self.client.post('/api/v1/users/', json={"first_name": "Goofy", "last_name": "Dog", "email": "goofy@disney.com", "pets": "DOG"})
        
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) >= 1)

def test_get_user_by_id(self):
        """Vérifie la récupération d'un utilisateur spécifique par son ID"""
        # 1. On crée un utilisateur pour avoir un ID valide
        post_response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@unique.com",
            "pets": "CAT"
        })
        user_id = post_response.json['id'] # On récupère l'ID généré

        # 2. On tente de le récupérer via la route dédiée
        get_response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['email'], "test@unique.com")

def test_update_user(self):
        """Vérifie la mise à jour d'un utilisateur existant"""
        # 1. Création
        post_res = self.client.post('/api/v1/users/', json={
            "first_name": "Old", "last_name": "Name", "email": "old@test.com", "pets": "CAT"
        })
        user_id = post_res.json['id']

        # 2. Modification
        update_data = {
            "first_name": "New", "last_name": "Name", "email": "new@test.com", "pets": "DOG"
        }
        put_res = self.client.put(f'/api/v1/users/{user_id}', json=update_data)
        
        # 3. Assertions
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.json['first_name'], "New")
        self.assertEqual(put_res.json['email'], "new@test.com")

if __name__ == '__main__':
    unittest.main()