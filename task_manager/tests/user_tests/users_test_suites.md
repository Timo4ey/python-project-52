# Test suites of task manager

---
### 1. User's test suit
1. Test Views
   1. Positive scenario
      1. localization
      2. 200 answer
 

4. Test Models
   1. Positive scenario
      1. Create a user
      *  Data: `{
            'first_name': 'Garry',
            'last_name': 'Galler',
            'username': 'garry_galler',
            'password1': 'secretpassword',
            'password2': 'secretpassword'
        }`


3. Test Forms
   1. Positive scenario
      1. Create a user full fields. is_valid() == True
      *  Data: `{
            'first_name': 'Garry',
            'last_name': 'Galler',
            'username': 'garry_galler',
            'password1': 'secretpassword',
            'password2': 'secretpassword'
        }`
   2. Negative scenario
      1. first_name over > 150
      1. first_name is empty
      1. last_name over > 150
      1. last_name is empty
      1. username over > 150
      1. username is empty
