# -*- coding: utf-8 -*-

import os
import sys
import unittest
from app import app, db
from models import User, News, Service, Category

class TestWDespachante(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
            self._create_test_data()
    
    def _create_test_data(self):
        with app.app_context():
            # Criar usuario admin
            admin = User(username='admin', email='admin@test.com', role='admin')
            admin.set_password('admin')
            db.session.add(admin)
            
            # Criar categoria
            category = Category(name='Test Category', slug='test-category')
            db.session.add(category)
            
            # Criar servico
            service = Service(
                name='Test Service',
                slug='test-service',
                summary='Test Summary',
                content='Test Content',
                featured=True,
                active=True
            )
            db.session.add(service)
            
            db.session.commit()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_login(self):
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main() 