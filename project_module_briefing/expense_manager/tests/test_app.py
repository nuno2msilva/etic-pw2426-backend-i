import pytest
from django.urls import reverse
from app.models import Record, Category
from app.forms import RecordForm
from django.test import Client
from datetime import date
from decimal import Decimal
from django.db.models import Sum

# -------- FIXTURES --------

@pytest.fixture
def user(django_user_model):
    """Fixture to create a user for testing."""
    return django_user_model.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def client(user):
    """Fixture to create an authenticated client for testing."""
    client = Client()
    client.login(username='testuser', password='testpassword')
    return client

@pytest.fixture
def category(user):
    """Fixture to create a category for testing."""
    return Category.objects.create(user=user, name='Test Category')

# -------- CORE FUNCTIONALITY TESTS --------

@pytest.mark.django_db
def test_can_view_record_list(client, user):
    """Test that users can view their records list (200 status code)."""
    Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Test Item', volume='10', cost='20')
    url = reverse('records')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Test Item' in response.content.decode()

@pytest.mark.django_db
def test_can_edit_records(client, user):
    """Test that users can access the edit page for their records (200 status code)."""
    record = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Test Item', volume='10', cost='20')
    url = reverse('edit_record', args=[record.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert 'Test Item' in response.content.decode()

@pytest.mark.django_db
def test_can_delete_records(client, user):
    """Test that users can access the delete page for their records. (200 status code)"""
    record = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Test Item', volume='10', cost='20')
    url = reverse('delete_record', args=[record.pk])
    response = client.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    assert 'Test Item' in content
    assert 'Are you sure you want to delete' in content

@pytest.mark.django_db
def test_delete_record_functionality(client, user):
    """Test that deleting a record actually removes it from the database."""
    record = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Test Item', volume='10', cost='20')
    record_id = record.id
    url = reverse('delete_record', args=[record.pk])
    response = client.post(url)
    assert response.status_code == 302
    assert reverse('records') in response.url
    assert not Record.objects.filter(id=record_id).exists()

@pytest.mark.django_db
def test_records_page_shows_all_user_records(client, user):
    """Test that the records page displays all records for the current user."""
    record1 = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Test Item 1', volume='10', cost='20')
    record2 = Record.objects.create(user=user, type='Income', date='2024-01-02', item='Test Item 2', volume='12', cost='22')
    url = reverse('records')
    response = client.get(url)
    content = response.content.decode()
    assert 'Test Item 1' in content
    assert 'Test Item 2' in content
    assert '20.00' in content
    assert '22.00' in content

@pytest.mark.django_db
def test_budget_balance_calculated_correctly(client, user):
    """Test that the total budget balance (income minus expenses) is calculated correctly."""
    Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Test Item 1', volume='10', cost=Decimal('20.00'))
    Record.objects.create(user=user, type='Income', date='2024-01-02', item='Test Item 2', volume='12', cost=Decimal('30.00'))
    Record.objects.create(user=user, type='Expense', date='2024-01-03', item='Test Item 3', volume='15', cost=Decimal('10.00'))
    url = reverse('records')
    response = client.get(url)
    assert 'Your Wallet: 0.00' in response.content.decode()

@pytest.mark.django_db
def test_edit_record_functionality(client, user, category):
    """Test that editing a record actually updates it in the database."""
    record = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Original Item', volume='10', cost='20', category=category)
    url = reverse('edit_record', args=[record.pk])
    data = {
        'type': 'Income', 
        'date': '2024-02-15', 
        'item': 'Updated Item', 
        'volume': '5',
        'cost': '50.00',
        'category': category.id 
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert reverse('records') in response.url
    updated_record = Record.objects.get(id=record.id)
    assert updated_record.type == 'Income'
    assert updated_record.date.strftime('%Y-%m-%d') == '2024-02-15'
    assert updated_record.item == 'Updated Item'
    assert updated_record.volume == '5'
    assert float(updated_record.cost) == 50.00
    assert updated_record.category == category

# -------- CATEGORY MANAGEMENT TESTS --------

@pytest.mark.django_db
def test_can_create_record_with_new_category(client, user):
    """Test that users can create a new record with a new category in one step."""
    url = reverse('records')
    data = {
        'type': 'Expense',
        'date': '2024-01-01',
        'item': 'Test Item',
        'volume': '10',
        'cost': '20',
        'category': '',
        'new_category': 'New Category'
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after successful form submission
    record = Record.objects.filter(user=user, item='Test Item').first()
    assert record is not None
    assert record.category is not None
    assert record.category.name == 'New Category'
    assert Category.objects.filter(user=user, name='New Category').exists()

@pytest.mark.django_db
def test_can_create_record_with_existing_category(client, user, category):
    """Test that users can create a new record with an existing category."""
    url = reverse('records')
    data = {
        'type': 'Expense',
        'date': '2024-01-01',
        'item': 'Test Item',
        'volume': '10',
        'cost': '20',
        'category': category.id,
        'new_category': ''
    }
    response = client.post(url, data)
    assert response.status_code == 302
    record = Record.objects.filter(user=user, item='Test Item').first()
    assert record is not None
    assert record.category == category

@pytest.mark.django_db
def test_can_edit_record_to_use_new_category(client, user, category):
    """Test that users can edit a record to use a new category."""
    record = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Original Item', volume='10', cost='20', category=category)
    url = reverse('edit_record', args=[record.pk])
    data = {
        'type': 'Expense',
        'date': '2024-01-01',
        'item': 'Original Item',
        'volume': '10',
        'cost': '20',
        'category': '',  
        'new_category': 'Brand New Category'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    updated_record = Record.objects.get(id=record.id)
    assert updated_record.category is not None
    assert updated_record.category.name == 'Brand New Category'
    assert Category.objects.filter(user=user, name='Brand New Category').exists()

@pytest.mark.django_db
def test_category_deletion_when_last_record_deleted(client, user):
    """Test that a category is automatically deleted when its last record is deleted."""
    category = Category.objects.create(user=user, name='Temporary Category')
    record = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Temp Item', volume='1', cost='10', category=category)
    category_id = category.id
    url = reverse('delete_record', args=[record.pk])
    response = client.post(url)
    assert not Category.objects.filter(id=category_id).exists()
    assert not Record.objects.filter(id=record.id).exists()

@pytest.mark.django_db
def test_orphaned_categories_are_removed_from_database(client, user):
    """Test that categories with no associated records are deleted from the database."""
    category = Category.objects.create(user=user, name='Test Category')
    record1 = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Test Item 1', volume='10', cost='20', category=category)
    record2 = Record.objects.create(user=user, type='Expense', date='2024-01-02', item='Test Item 2', volume='10', cost='30', category=category)
    url = reverse('delete_record', args=[record1.pk])
    client.post(url)
    assert Category.objects.filter(id=category.id).exists()
    url = reverse('delete_record', args=[record2.pk])
    client.post(url)
    assert not Category.objects.filter(id=category.id).exists()

@pytest.mark.django_db
def test_category_preserved_when_other_records_exist(client, user):
    """Test that a category is NOT deleted when other records still use it."""
    category = Category.objects.create(user=user, name='Shared Category')
    record1 = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Item 1', volume='10', cost='20', category=category)
    record2 = Record.objects.create(user=user, type='Expense', date='2024-01-02', item='Item 2', volume='10', cost='30', category=category)
    url = reverse('delete_record', args=[record1.pk])
    client.post(url)
    assert Category.objects.filter(id=category.id).exists()
    assert not Record.objects.filter(id=record1.id).exists()
    assert Record.objects.filter(id=record2.id).exists()

@pytest.mark.django_db
def test_updates_clean_orphaned_categories(client, user):
    """Test that updating a record cleans up orphaned categories."""
    client.force_login(user)
    category1 = Category.objects.create(user=user, name="Category One")
    category2 = Category.objects.create(user=user, name="Category Two")
    print(f"Category1 ID: {category1.id}, Category2 ID: {category2.id}")
    record = Record.objects.create(
        user=user,
        type='Expense',
        date='2024-01-01',
        item='Test Item',
        volume='10',
        cost='20',
        category=category1
    )
    print(f"Initial record category ID: {record.category.id}")
    assert record.category.id == category1.id
    assert Category.objects.filter(user=user).count() == 2
    url = reverse('edit_record', args=[record.id])
    data = {
        'type': 'Expense',
        'date': '2024-01-01',
        'item': 'Test Item',
        'volume': '10',
        'cost': '20',
        'category': category2.id,
        'new_category': '' 
    }
    print(f"Updating record to use category ID: {category2.id}")
    response = client.post(url, data)
    assert response.status_code == 302
    record.refresh_from_db()
    print(f"After update, record category ID: {record.category.id}")
    assert record.category.id == category2.id
    remaining = Record.objects.filter(category_id=category1.id).count()
    print(f"Records still using category1: {remaining}")
    assert Category.objects.filter(id=category1.id).count() == 0

# -------- SECURITY TESTS --------

@pytest.mark.django_db
def test_users_cannot_access_others_records(client, user, django_user_model):
    """Test that users cannot access or modify records belonging to other users."""
    other_user = django_user_model.objects.create_user(username='otheruser', password='testpassword')
    record = Record.objects.create(user=other_user, type='Expense', date='2024-01-01', item='Test Item', volume='10', cost='20')
    url = reverse('edit_record', args=[record.pk])
    response = client.get(url)
    assert response.status_code == 404
    data = {
        'type': 'Expense',
        'date': '2024-01-01',
        'item': 'Hacked Item',
        'volume': '10',
        'cost': '20',
    }
    response = client.post(url, data)
    assert response.status_code == 404
    url = reverse('delete_record', args=[record.pk])
    response = client.post(url)
    assert response.status_code == 404
    unchanged_record = Record.objects.get(id=record.id)
    assert unchanged_record.item == 'Test Item'

@pytest.mark.django_db
def test_shared_category_names_dont_conflict(client, user, django_user_model):
    """Test that categories with the same name can exist for different users without interference."""
    other_user = django_user_model.objects.create_user(username='otheruser', password='testpassword')
    category1 = Category.objects.create(user=user, name='Shared Category')
    category2 = Category.objects.create(user=other_user, name='Shared Category')
    record1 = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Test Item', volume='10', cost='20', category=category1)
    record2 = Record.objects.create(user=other_user, type='Expense', date='2024-01-01', item='Test Item', volume='10', cost='20', category=category2)
    url = reverse('delete_record', args=[record1.pk])
    client.post(url)
    assert not Category.objects.filter(id=category1.id).exists()
    assert Category.objects.filter(id=category2.id).exists()
    client.logout()
    client.login(username='otheruser', password='testpassword')
    url = reverse('records')
    response = client.get(url)
    assert 'Shared Category' in response.content.decode()

@pytest.mark.django_db
def test_category_lists_are_user_specific(client, user, django_user_model):
    """Test that each user only sees their own categories in dropdown menus."""
    other_user = django_user_model.objects.create_user(username='otheruser', password='testpassword')
    user_category = Category.objects.create(user=user, name='Food')
    other_category = Category.objects.create(user=other_user, name='Transportation')
    shared_name_category = Category.objects.create(user=other_user, name='Food')
    Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Groceries', volume='1', cost='50', category=user_category)
    Record.objects.create(user=other_user, type='Expense', date='2024-01-01', item='Bus', volume='1', cost='5', category=other_category)
    Record.objects.create(user=other_user, type='Expense', date='2024-01-01', item='Restaurant', volume='1', cost='25', category=shared_name_category)
    url = reverse('records')
    response = client.get(url)
    content = response.content.decode()
    assert 'Food' in content
    assert 'Transportation' not in content
    client.logout()
    client.login(username='otheruser', password='testpassword')
    response = client.get(url)
    content = response.content.decode()
    assert 'Transportation' in content
    assert 'Food' in content
    new_category_name = 'Entertainment'
    data = {
        'type': 'Expense',
        'date': '2024-01-01',
        'item': 'Movie',
        'volume': '2',
        'cost': '30',
        'category': '',
        'new_category': new_category_name
    }
    response = client.post(url, data)
    assert Category.objects.filter(user=other_user, name=new_category_name).exists()
    assert not Category.objects.filter(user=user, name=new_category_name).exists()
    client.logout()
    client.login(username='testuser', password='testpassword')
    response = client.get(url)
    content = response.content.decode()
    assert new_category_name not in content

@pytest.mark.django_db
def test_users_can_only_delete_their_own_categories(client, user, django_user_model):
    """Test that users cannot delete categories belonging to other users."""
    other_user = django_user_model.objects.create_user(username='otheruser', password='testpassword')
    user_category = Category.objects.create(user=user, name="User's Category")
    other_category = Category.objects.create(user=other_user, name="Other's Category")
    user_record = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='User Item', volume='10', cost='20', category=user_category)
    other_record = Record.objects.create(user=other_user, type='Expense', date='2024-01-01', item='Other Item', volume='10', cost='20', category=other_category)
    url = reverse('delete_record', args=[other_record.pk])
    response = client.post(url)
    assert response.status_code == 404
    assert Record.objects.filter(id=user_record.id).exists()
    assert Record.objects.filter(id=other_record.id).exists()
    assert Category.objects.filter(id=user_category.id).exists()
    assert Category.objects.filter(id=other_category.id).exists()

# -------- AUTHENTICATION TESTS --------

@pytest.mark.django_db
def test_homepage_loads_correctly(client):
    """Test that the homepage loads successfully for all visitors (200 status code)."""
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_signup_page_accessible(client):
    """Test that new users can access the registration page (200 status code)."""
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_registration_creates_user(client):
    """Test that registration creates a new user."""
    url = reverse('register')
    data = {
        'username': 'newuser',
        'password1': 'complex_password123',
        'password2': 'complex_password123'
    }
    response = client.post(url, data)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    assert User.objects.filter(username='newuser').exists()
    assert response.status_code == 302
    assert reverse('login') in response.url

@pytest.mark.django_db
def test_login_page_accessible(client):
    """Test that the login page is accessible to unauthenticated users (200 status code)."""
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_functionality(client, django_user_model):
    """Test that users can log in."""
    django_user_model.objects.create_user(username='loginuser', password='testpassword')
    url = reverse('login')
    data = {
        'username': 'loginuser',
        'password': 'testpassword'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert reverse('records') in response.url

@pytest.mark.django_db
def test_logout_works_and_redirects(client):
    """Test that logging out works and redirects to the homepage."""
    url = reverse('logout')
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == '/'

@pytest.mark.django_db
def test_private_pages_protected_from_anonymous_users(client):
    """Test that private pages redirect unauthenticated users to login."""    
    client.logout()
    url = reverse('records')
    response = client.get(url)
    assert response.status_code == 302
    assert reverse('login') in response.url

# -------- DISPLAY FORMATTING TESTS --------

@pytest.mark.django_db
def test_transaction_type_capitalized_in_display(client, user):
    """Test that transaction types are capitalized when displayed."""
    record1 = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Test Expense', volume='10', cost='20')
    record2 = Record.objects.create(user=user, type='Income', date='2024-01-02', item='Test Income', volume='10', cost='30')
    url = reverse('records')
    response = client.get(url)
    content = response.content.decode()
    assert 'Expense' in content
    assert 'Income' in content

# -------- FORM VALIDATION TESTS --------

@pytest.mark.django_db
def test_form_accepts_valid_input(user):
    """Test that the record form accepts correctly formatted input."""
    form_data = {
        'type': 'Expense',
        'date': date(2024, 1, 1),
        'item': 'Test Item',
        'volume': '10',
        'cost': '20',
        'category': ''
    }
    form = RecordForm(data=form_data, user=user)
    assert form.is_valid()

@pytest.mark.django_db
def test_form_rejects_empty_fields(user):
    """Test that the record form rejects submissions with empty required fields."""
    form_data = {
        'type': '',
        'date': 'invalid',
        'item': '',
        'volume': '',
        'cost': '',
        'category': ''
    }
    form = RecordForm(data=form_data, user=user)
    assert not form.is_valid()

@pytest.mark.django_db
def test_form_validates_date_format(user):
    """Test that the form rejects incorrectly formatted dates."""
    form_data = {
        'type': 'Expense',
        'date': 'abc',
        'item': 'Test Item',
        'volume': '10',
        'cost': '20',
        'category': ''
    }
    form = RecordForm(data=form_data, user=user)
    assert not form.is_valid()
    assert 'date' in form.errors

@pytest.mark.django_db
def test_form_enforces_item_name_length_limit(user):
    """Test that the form enforces maximum length for item descriptions."""
    form_data = {
        'type': 'Expense',
        'date': date(2024, 1, 1),
        'item': 'Test Item' * 100,
        'volume': '10',
        'cost': '20',
        'category': ''
    }
    form = RecordForm(data=form_data, user=user)
    assert not form.is_valid()
    assert 'item' in form.errors

@pytest.mark.django_db
def test_form_requires_numeric_values_for_amount_fields(user):
    """Test that volume and cost fields must contain numeric values."""
    form_data = {
        'type': 'Expense',
        'date': date(2024, 1, 1),
        'item': 'Test Item',
        'volume': 'abc',
        'cost': 'xyz',
        'category': ''
    }
    form = RecordForm(data=form_data, user=user)
    assert not form.is_valid()
    assert 'cost' in form.errors

@pytest.mark.django_db
def test_form_requires_valid_transaction_type(user):
    """Test that the transaction type must be either 'Income' or 'Expense'."""
    form_data = {
        'type': 'invalid',
        'date': date(2024, 1, 1),
        'item': 'Test Item',
        'volume': '10',
        'cost': '20',
        'category': ''
    }
    form = RecordForm(data=form_data, user=user)
    assert not form.is_valid()
    assert 'type' in form.errors

@pytest.mark.django_db
def test_form_allows_decimal_costs(user):
    """Test that the form accepts decimal values for cost."""
    form_data = {
        'type': 'Expense',
        'date': date(2024, 1, 1),
        'item': 'Test Item',
        'volume': '10',
        'cost': '20.50',
        'category': ''
    }
    form = RecordForm(data=form_data, user=user)
    assert form.is_valid()

# -------- SORTING AND FILTERING TESTS --------

@pytest.mark.django_db
def test_records_can_be_sorted_by_date(client, user):
    """Test that records can be sorted by date."""
    record1 = Record.objects.create(user=user, type='Expense', date='2024-01-03', item='Later Item', volume='10', cost='20')
    record2 = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Early Item', volume='10', cost='30')
    url = reverse('records') + '?sort=date'
    response = client.get(url)
    content = response.content.decode()
    early_pos = content.find('Early Item')
    later_pos = content.find('Later Item')
    assert early_pos < later_pos
    url = reverse('records') + '?sort=-date'
    response = client.get(url)
    content = response.content.decode()
    early_pos = content.find('Early Item')
    later_pos = content.find('Later Item')
    assert later_pos < early_pos

@pytest.mark.django_db
def test_records_can_be_sorted_by_cost(client, user):
    """Test that records can be sorted by cost."""
    record1 = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Expensive Item', volume='10', cost='50')
    record2 = Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Cheap Item', volume='10', cost='10')
    url = reverse('records') + '?sort=cost'
    response = client.get(url)
    content = response.content.decode()
    cheap_pos = content.find('Cheap Item')
    expensive_pos = content.find('Expensive Item')
    assert cheap_pos < expensive_pos
    url = reverse('records') + '?sort=-cost'
    response = client.get(url)
    content = response.content.decode()
    cheap_pos = content.find('Cheap Item')
    expensive_pos = content.find('Expensive Item')
    assert expensive_pos < cheap_pos

@pytest.mark.django_db
def test_sort_by_item(client, user):
    """Test that records can be sorted by item name."""
    client.force_login(user)
    Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Zebra Food', volume='10', cost='20')
    Record.objects.create(user=user, type='Income', date='2024-01-02', item='Apple Juice', volume='10', cost='30')
    Record.objects.create(user=user, type='Expense', date='2024-01-03', item='Banana Bread', volume='10', cost='40')
    url = reverse('records') + '?sort=item'
    response = client.get(url)
    content = response.content.decode()
    apple_pos = content.find('Apple Juice')
    banana_pos = content.find('Banana Bread')
    zebra_pos = content.find('Zebra Food')
    assert apple_pos < banana_pos < zebra_pos, "Items should be sorted alphabetically (A-Z)"
    url = reverse('records') + '?sort=-item'
    response = client.get(url)
    content = response.content.decode()
    apple_pos = content.find('Apple Juice')
    banana_pos = content.find('Banana Bread')
    zebra_pos = content.find('Zebra Food')
    assert zebra_pos < banana_pos < apple_pos, "Items should be sorted in reverse alphabetical order (Z-A)"

# -------- ERROR HANDLING TESTS --------

@pytest.mark.django_db
def test_invalid_urls_show_404_page(client):
    """Test that navigating to non-existent URLs returns a 404 error page."""
    url = '/nonexistent_page/'
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_accessing_nonexistent_record_returns_404(client, user):
    """Test that attempting to access a non-existent record returns a 404."""
    url = reverse('edit_record', args=[9999])
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_user_input_is_title_cased(client, user):
    """Test that user input for item and category is capitalized for each word."""
    url = reverse('records')
    data = {
        'type': 'Expense',
        'date': '2024-01-01',
        'item': 'food for cat',
        'volume': '1',
        'cost': '15.00',
        'category': '',
        'new_category': 'pet supplies'
    }
    client.post(url, data)
    record = Record.objects.filter(user=user).latest('id')
    assert record.item == 'Food For Cat'
    assert record.category.name == 'Pet Supplies'
    assert Category.objects.filter(user=user, name='Pet Supplies').exists()

@pytest.mark.django_db
def test_user_input_capitalization_preserves_acronyms(client, user):
    """Test that capitalization preserves acronyms while capitalizing first letters."""
    category = Category.objects.create(user=user, name="tech & COMPUTER")
    assert category.name == "Tech & COMPUTER"
    record = Record.objects.create(
        user=user, 
        type='Expense', 
        date='2024-01-01',
        item='TV set for home',
        volume='1',
        cost='500.00',
        category=category
    )
    assert record.item == "TV Set For Home"

# -------- PURGE FUNCTIONALITY TEST --------

@pytest.mark.django_db
def test_purge_records_functionality(client, user):
    """Test that the purge functionality deletes all user records."""
    client.force_login(user)
    
    Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Test Item 1', volume='10', cost='20')
    Record.objects.create(user=user, type='Income', date='2024-01-02', item='Test Item 2', volume='10', cost='30')
    Record.objects.create(user=user, type='Expense', date='2024-01-03', item='Test Item 3', volume='10', cost='40')
    assert Record.objects.filter(user=user).count() == 3
    url = reverse('purge_records')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Warning' in response.content.decode()
    assert '3 records' in response.content.decode()
    response = client.post(url, follow=True)
    assert response.status_code == 200
    assert Record.objects.filter(user=user).count() == 0

@pytest.mark.django_db
def test_purge_removes_categories(client, user):
    """Test that purging records also removes orphaned categories."""
    client.force_login(user)
    category = Category.objects.create(user=user, name="Test Category")
    Record.objects.create(user=user, type='Expense', date='2024-01-01', item='Test Item', volume='10', cost='20', category=category)
    assert Record.objects.filter(user=user).count() == 1
    assert Category.objects.filter(user=user).count() == 1
    url = reverse('purge_records')
    response = client.post(url, follow=True)
    assert Record.objects.filter(user=user).count() == 0    
    assert Category.objects.filter(user=user).count() == 0